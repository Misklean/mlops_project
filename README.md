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
- Docker
- A GPU with CUDA support (optional but recommended for faster inference)
- NVIDIA drivers installed on the host machine

---

### Step 1: Set Up GPU Support for Docker (Optional)

If you want to enable GPU support, follow these steps to install the NVIDIA Container Toolkit:

1. **Add the NVIDIA package repository:**

   ```bash
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
     && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
       sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
       sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   ```

2. **Update the package list and install the toolkit:**

   ```bash
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   ```

3. **Restart the Docker daemon:**

   ```bash
   sudo systemctl restart docker
   ```

---

### Step 2: Start the Web Service

1. **Build the Docker image:**

   ```bash
   docker build -t flask-ai-image-generation .
   ```

2. **Run the Docker container:**

   ```bash
   docker run --gpus all -p 5000:5000 flask-ai-image-generation
   ```

   If you don't have a GPU or don't want to use one, run the container without the GPU flag:

   ```bash
   docker run -p 5000:5000 flask-ai-image-generation
   ```

This will start the service at `http://127.0.0.1:5000`.

---

### Step 3: Send a Request

Send a POST request to the `/generate-image` endpoint with a JSON body that includes the prompt, number of inference steps, and guidance scale. For example:

**curl Example**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"prompt":"A cinematic shot of 3 maneki neko in South America."}' \
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

## Happy Generating! 🚀