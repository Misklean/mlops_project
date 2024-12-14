FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "$HUGGINGFACE_TOKEN" | huggingface-cli login --token

COPY . /app/

EXPOSE 5000

CMD ["python3", "app.py"]
