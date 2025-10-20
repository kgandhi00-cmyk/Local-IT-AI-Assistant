import requests
import json

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3", "prompt": "Explain DHCP in one sentence."},
)

# Ollama streams multiple JSON lines, so we combine them
full_response = ""
for line in response.text.splitlines():
    try:
        data = json.loads(line)
        full_response += data.get("response", "")
    except json.JSONDecodeError:
        continue

print(full_response)