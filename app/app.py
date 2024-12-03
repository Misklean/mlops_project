from flask import Flask, request, send_file, jsonify
from diffusers import AutoPipelineForText2Image
import torch
from io import BytesIO

# Initialize the Flask app
app = Flask(__name__)

# Load the model
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
)
pipe.enable_model_cpu_offload()

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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
