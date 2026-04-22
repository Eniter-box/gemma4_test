import os
import subprocess
import time
import requests
import json
import runpod

MODEL = os.getenv("MODEL_NAME", "google/gemma-4-31B-it")
PORT = os.getenv("PORT", "8000")
API_URL = f"http://localhost:{PORT}/v1/chat/completions"

def start():
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", MODEL,
        "--host", "0.0.0.0",
        "--port", str(PORT),
        "--gpu-memory-utilization", "0.9",
        "--max-model-len", "8192",
        "--dtype", "bfloat16",
    ]
    subprocess.Popen(cmd)
    # Attendre que vLLM soit prêt
    wait_for_server()

def wait_for_server(max_retries=30, retry_delay=2):
    """Attendre que vLLM soit opérationnel"""
    for attempt in range(max_retries):
        try:
            response = requests.get(f"http://localhost:{PORT}/health", timeout=5)
            if response.status_code == 200:
                print(f"✓ vLLM server ready after {attempt * retry_delay}s")
                return True
        except:
            pass
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    raise RuntimeError("vLLM server failed to start")

start()

def handler(job):
    try:
        job_input = job["input"]
        
        # Extraire les paramètres
        messages = job_input.get("messages", [])
        temperature = job_input.get("temperature", 1.0)
        max_tokens = job_input.get("max_tokens", 1024)
        top_p = job_input.get("top_p", 0.95)
        
        if not messages:
            return {"error": "messages field is required"}
        
        # Appeler vLLM via OpenAI API
        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
        }
        
        response = requests.post(API_URL, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        return result
        
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Handler error: {str(e)}"}

runpod.serverless.start({"handler": handler})
