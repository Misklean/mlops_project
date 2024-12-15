import torch
import logging
import threading
from io import BytesIO
from flask import Flask, request, jsonify, send_file
from diffusers import AutoPipelineForText2Image
from PIL import Image

# Initialize the Flask app
app = Flask(__name__)

# Logging configuration
logger = logging.getLogger(__name__)

# API Token
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGVtbyIsImlhdCI6MTY5MzY2NjY2Nn0._sCx6DJMKvhG6Dp9tcDw2q8P7TXqEwnCX7H8CfM0OsE"

# Thread-safe model manager to handle concurrent image generation requests
class ModelManager:
    _instance = None
    _lock = threading.Lock()

    # Make the class a singleton
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ModelManager, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.pipe = None
        self.device = None
        self.generation_lock = threading.Lock()
        self.load_model()

    # Load the image generation model with robust error handling and GPU support
    def load_model(self):
        try:
            # Check if a GPU is available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")

            # Load the model with explicit configuration
            self.pipe = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo",
                variant="fp16",
                torch_dtype=torch.float16 if self.device.type == 'cuda' else torch.float32
            )

            # Move model to device with explicit memory management
            self.pipe = self.pipe.to(self.device)
            
            # Additional optimizations
            self.pipe.enable_attention_slicing()
            if self.device.type == 'cuda':
                self.pipe.enable_model_cpu_offload()
            
            logger.info("Model initialized successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.pipe = None
            raise

    # Thread-safe image generation method
    def generate_image(self, prompt):
        if self.pipe is None:
            raise RuntimeError("Model not initialized")

        # Use a lock to prevent concurrent model access
        with self.generation_lock:
            try:
                # Use context manager for potential memory management
                with torch.no_grad():
                    # Ensure we use a new generator for each call
                    generator = torch.Generator(device=self.device).manual_seed(torch.random.seed())
                    
                    result = self.pipe(
                        prompt=prompt,
                        num_inference_steps=50,
                        guidance_scale=7.5,
                        generator=generator,
                        height=512,
                        width=512
                    )

                # Ensure we have an image
                if not result.images:
                    logger.error("No images were generated")
                    raise RuntimeError("Image generation failed")

                # Take the first image and ensure it's in RGB mode
                image = result.images[0].convert("RGB")
                return image

            except Exception as e:
                logger.error(f"Error during image generation: {e}", exc_info=True)
                raise

# Create a singleton instance of ModelManager
model_manager = ModelManager()

# Middleware to check for the token in the request headers.
@app.before_request
def require_token():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "Unauthorized. A valid token is required."}), 401

# Generate an image based on the given prompt with improved concurrency handling
@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        # Parse the request JSON
        data = request.json
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate image using thread-safe model manager
        image = model_manager.generate_image(prompt)

        # Convert the image to a byte stream
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Return the image as a file response
        return send_file(img_byte_arr, mimetype="image/png", as_attachment=False)

    except RuntimeError as cuda_error:
        logger.error(f"CUDA Error during image generation: {cuda_error}")
        return jsonify({
            "error": "GPU processing error. Try reducing image complexity or inference steps.",
            "details": str(cuda_error)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error during image generation: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Configure Flask for multi-threaded operations
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
