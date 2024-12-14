echo ===== Install Docker

sudo apt update -y
sudo apt install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo apt install docker-compose -y

sudo groupadd docker

sudo usermod -aG docker $USER

echo ===== Set Up GPU Support for Docker

if [ -f "$KEYRING_PATH" ]; then
    echo "File '$KEYRING_PATH' already exists. Skipping keyring setup."
else
    # Proceed with downloading and setting up the keyring if it doesn't exist
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o "$KEYRING_PATH" \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed "s#deb https://#deb [signed-by=$KEYRING_PATH] https://#g" | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
fi

sudo apt update -y
sudo apt install -y nvidia-container-toolkit

sudo systemctl restart docker

# =============================================

echo ===== Discord Bot Setup

echo DISCORD_TOKEN=$1 > ./discord_bot/.env

echo ===== HuggingFace Token

export HUGGINGFACE_TOKEN=$2

# =============================================

echo ===== Launch services

sudo docker-compose up --build

