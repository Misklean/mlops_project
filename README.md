# AI Image Generation Web Service

This project demonstrates how to use and deploy an AI-based image generation model as a web service. The service generates images based on text prompts and is designed to be lightweight and fast for real-time applications.

## Overview

The web service uses the **Stability AI's SDXL Turbo** model, available on Hugging Face: [`stabilityai/sdxl-turbo`](https://huggingface.co/stabilityai/sdxl-turbo). This model was chosen because:

- It is efficient and optimized for smaller hardware requirements.
- Other models are too large or take too much time during inference, making them impractical for this deployment.

The service is built using **Flask** to provide a REST API for generating images based on user-provided input.

---

## Features

- **Text-to-Image Generation**: Accepts a prompt (text description) and generates a corresponding image.
- **Streamlined Output**: Converts the generated image into a byte stream and sends it as the API response in PNG format.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- A GPU with CUDA support (optional but recommended for faster inference)

### Install Dependencies

1. Install the required Python libraries:
   ```bash
   pip install flask torch diffusers transformers accelerate
   ```

---

## Usage

### Step 1: Start the Web Service

Run the Flask application:
```bash
python app.py
```

This will start the service at `http://127.0.0.1:5000`.

---

### Step 2: Send a Request

Send a POST request to the `/generate-image` endpoint with a JSON body that includes the prompt, number of inference steps, and guidance scale. For example:

**curl Example**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"prompt":"A cinematic shot a 3 maneki neko in South America."}' \
     http://127.0.0.1:5000/generate-image --output result.png
```

This will generate an image and save it as `result.png`.

---

## How It Works

1. The web service accepts a POST request containing:
   - `prompt`: A text description for the desired image.

2. The Flask app uses the SDXL Turbo model to generate the image based on the prompt.

3. The generated image is converted into a byte stream and returned as the response in PNG format.

---

## Limitations

- This service is restricted to the **`stabilityai/sdxl-turbo`** model due to its smaller size and faster inference time. Other models may exceed the limits of typical deployment environments.
- Inference time may vary based on hardware. A GPU is highly recommended for efficient performance.
---

### Happy Generating! 🚀