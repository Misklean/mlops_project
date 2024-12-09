# AI Image Generation Web Service and Discord Bot

This project demonstrates how to use and deploy an AI-based image generation model as a web service and integrate it with a Discord bot. The service generates images based on text prompts and is designed to be lightweight and fast for real-time applications.

## Overview

The web service uses the **Stability AI's SDXL Turbo** model, available on Hugging Face: [`stabilityai/sdxl-turbo`](https://huggingface.co/stabilityai/sdxl-turbo). This model was chosen because:

- It is efficient and optimized for smaller hardware requirements.
- Other models are too large or take too much time during inference, making them impractical for this deployment.

In addition to the web service, this project includes a **Discord bot** that allows users to interact with the image generation API directly from Discord. Users can mention the bot with a prompt, and it will generate and send back an image based on their input.

---

## Features

### Web Service
- **Text-to-Image Generation**: Accepts a prompt (text description) and generates a corresponding image.  
- **Streamlined Output**: Converts the generated image into a byte stream and sends it as the API response in PNG format.  
- **Secure Web Service**: Implements authentication using a token-based system to ensure that only authorized users can access the service.

### Discord Bot
- **Real-Time Interaction**: Generate images directly from Discord by mentioning the bot and providing a text prompt.  
- **Seamless Integration**: The bot interacts with the web service to retrieve and send back the generated image.  
- **Easy Deployment**: Set up the bot with minimal configuration using a `.env` file.

---

## Installation

### You can install and launch this on a new VM using the command:
```bash
# <Here goes the command>
```

---

### We use a Docker Compose to launch the application, but the GPU is needed for optimal performance:
'''bash
docker-compose up
'''

### Prerequisites

- Python 3.8 or higher
- Docker
- A GPU with CUDA support (optional but recommended for faster inference)
- NVIDIA drivers installed on the host machine
- A Discord account and bot token

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

### Step 2: Discord Bot Setup

**Create a `.env` file** in the `discord_bot` directory:  
   Add your Discord bot token to the `.env` file:

   ```plaintext
   DISCORD_TOKEN=<Your_Discord_Bot_Token>
   ```

---

### Step 3: Launch services

You can easily launch the two services using Docker Compose. To do so, run the following command:

```bash
docker-compose up --build
```

---

## How It Works

### Web Service
1. The web service accepts a POST request containing:
   - `prompt`: A text description for the desired image.
2. The Flask app uses the SDXL Turbo model to generate the image based on the prompt.
3. The generated image is converted into a byte stream and returned as the response in PNG format.

### Discord Bot
1. When a user mentions the bot in a message on Discord with a text prompt, the bot extracts the prompt.
2. The bot sends the prompt to the web service's `/generate-image` endpoint using a POST request.
3. The bot receives the generated image in PNG format and sends it back to the user in Discord, tagging them.

---

### Example Usage

#### Web Service:
Send a POST request to the `/generate-image` endpoint with a JSON body that includes the prompt, number of inference steps, and guidance scale. For example:

**curl Example**:
```bash
curl -X POST http://127.0.0.1:5000/generate-image \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGVtbyIsImlhdCI6MTY5MzY2NjY2Nn0._sCx6DJMKvhG6Dp9tcDw2q8P7TXqEwnCX7H8CfM0OsE" \
-H "Content-Type: application/json" \
-d '{"prompt": "A majestic mountain under a pink sunset"}' --output result.png
```

#### Discord Bot:
1. Mention the bot in a Discord channel with your prompt:
   ```
   @ImageGenBot A majestic mountain under a pink sunset
   ```
2. The bot will respond with the generated image.

---

## Limitations

- The web service is restricted to the **`stabilityai/sdxl-turbo`** model due to its smaller size and faster inference time. Other models may exceed the limits of typical deployment environments.
- Inference time may vary based on hardware. A GPU is highly recommended for efficient performance.

---

## Happy Generating! 🚀