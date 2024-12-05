from flask import Flask, request, jsonify, send_file
from diffusers import AutoPipelineForText2Image
import torch
import logging
from io import BytesIO

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask app
app = Flask(__name__)

# Check if a GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
try:
    # Load the model
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # Use float16 for GPU, float32 for CPU
        variant="fp16" if torch.cuda.is_available() else None  # Variant only needed for GPU
    )

    if device == torch.device("cuda"):
        pipe.enable_model_cpu_offload()  # For memory optimization on GPU
    else:
        pipe.to("cpu")  # Move the model to CPU
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise


# Define the token
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGVtbyIsImlhdCI6MTY5MzY2NjY2Nn0._sCx6DJMKvhG6Dp9tcDw2q8P7TXqEwnCX7H8CfM0OsE"

@app.before_request
def require_token():
    """
    Middleware to check for the token in the request headers.
    """
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "Unauthorized. A valid token is required."}), 401

@app.route("/generate-image", methods=["POST"])
def generate_image():
    """
    Generate an image based on the given prompt.
    """
    try:
        # Parse the request JSON
        data = request.json
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate the image
        image = pipe(
            prompt=prompt,
            num_inference_steps=50,
            guidance_scale=7.5,
        ).images[0]

        # Convert the image to a byte stream
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Return the image as a file response
        return send_file(img_byte_arr, mimetype="image/png", as_attachment=False)

    except Exception as e:
        logging.error(f"Error during image generation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
