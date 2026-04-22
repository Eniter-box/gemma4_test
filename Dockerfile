FROM vllm/vllm-openai:latest

# Dépendances souvent nécessaires pour modèles récents
RUN pip install --no-cache-dir -U "transformers>=4.50.0" "accelerate" "huggingface_hub" "safetensors"

# Handler Runpod (le "worker" serverless) et requests pour OpenAI API
RUN pip install --no-cache-dir -U runpod requests

WORKDIR /app
COPY handler.py /app/handler.py

CMD ["python", "-u", "handler.py"]