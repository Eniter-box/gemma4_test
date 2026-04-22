import os
import subprocess
import runpod

MODEL = os.getenv("MODEL_NAME", "google/gemma-4-31B-it")
PORT = os.getenv("PORT", "8000")

def start():
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", MODEL,
        "--host", "0.0.0.0",
        "--port", str(PORT),
    ]

    # variables utiles
    # DTYPE, MAX_MODEL_LEN, GPU_MEMORY_UTILIZATION etc. peuvent être passées en env
    subprocess.Popen(cmd)

start()

def handler(job):
    # Ton endpoint Runpod répondra "READY"; ensuite tu appelles /v1/chat/completions
    return {"status": "READY", "model": MODEL, "openai_port": PORT}

runpod.serverless.start({"handler": handler})
