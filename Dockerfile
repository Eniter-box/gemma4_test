FROM vllm/vllm-openai:latest

# Dépendances souvent nécessaires pour modèles récents
RUN pip install -U "transformers>=4.50.0" "accelerate" "huggingface_hub" "safetensors"

# Handler Runpod (le “worker” serverless)
RUN pip install -U runpod

WORKDIR /app
COPY handler.py /app/handler.py

CMD ["python", "-u", "handler.py"]