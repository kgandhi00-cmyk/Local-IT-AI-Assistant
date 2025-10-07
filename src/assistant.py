'''import os
import json
import time
from dotenv import load_dotenv
import requests

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
API_KEY = os.getenv("ASSISTANT_API_KEY") # optional, for FASTAPI auth

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT",
    "You are a helpful, safety and security conscious IT assistant. "
    "Always clearly explain commands as if you are speaking to entry level IT professionals, never execute destructive or malicious actions, "
    "and never run any code or scripts without explicit user confirmation. "
    "Use the most recent or up to date information sources possible, unless these do not work. "
    "When asked to generate scripts, produce readable, commented PowerShell or Bash code."
)

class OllamaClient:
    def __init__(self, base_url=OLLAMA_URL, model=MODEL_NAME):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _generate_payload(self, prompt, max_tokens=2048):
        # adjust payload fields if Ollama expects different keys in the future
        return {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens
        }
    def generate(self, prompt, timeout=120):
        """Non-streaming friendly helper: returns reconstructed response text."""
        url = f"{self.base_url}/api/generate"
        payload = self._generate_payload(prompt)
        try:
            resp = requests.post(url, json=payload, stream=True, timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Failed to contact Ollama at {url}: {e}") from e
        
        full=[]
        # Ollama returns newline-delimited JSON, one token/chunk per line
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            # accumulate any "response" fields
            r = obj.get("response")
            if r:
                full.append(r)
            if obj.get("done") is True:
                break
        return "".join(full).strip()
ollama = OllamaClient()

class ITAssistant:
    def __init__(self, client=ollama, system_prompt=SYSTEM_PROMPT):
        self.client = client
        self.system_prompt = system_prompt
        # mapping safe actions -> command list to run (powershell)
        self.safe_actions = {
            "list_processes": ["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-Process | Select-Object -First 200 | ConvertTo-Json"],
            "list_services": ["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-Service | Select-Object -First 200 | ConvertTo-Json"],
            "disk_usage": ["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-PSDrive -PSProvider FileSystem | Select-Object -Property Name,Used,Free,Root | ConvertTo-Json"],
            "computer_info": ["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-ComputerInfo | Select-Object -Property CsName,OsName,OsVersion,OsBuildNumber,OsArchitecture | ConvertTo-Json"]
        }

    def build_prompt(self, user_question):
        # Combine system prompt & user question
        return f"{self.system_prompt}\n\nUser: {user_question}\n\nAssistant:"
    
    def ask(self, question):
        prompt = self.build_prompt(question)
        return self.client.generate(prompt)
    
    def generate_script(self, instruction, language="powershell"):
        prompt= (
            f"{self.system_prompt}\n\n"
            f"Generate a {language} script for this task. Include comments and do NOT execute it:\n\n"
            f"Task: {instruction}\n\n"
            f"Return only the script inside code fences.\n"
        )
        return self.client.generate(prompt)
    def list_safe_actions(self):
        return list(self.safe_actions.keys())
    
    def get_action_command(self, action_name):
        return self.safe_actions.get(action_name)'''
import os
import json
import time
from dotenv import load_dotenv
import requests
import subprocess

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
API_KEY = os.getenv("ASSISTANT_API_KEY")  # optional, for FASTAPI auth

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful, safety and security conscious IT assistant. "
    "Always clearly explain commands as if you are speaking to entry level IT professionals, never execute destructive or malicious actions, "
    "and never run any code or scripts without explicit user confirmation. "
    "Use the most recent or up to date information sources possible, unless these do not work. "
    "When asked to generate scripts, produce readable, commented PowerShell or Bash code."
)

class OllamaClient:
    def __init__(self, base_url=OLLAMA_URL, model=MODEL_NAME):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _generate_payload(self, prompt, max_tokens=2048):
        return {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens
        }

    def generate(self, prompt, timeout=120):
        """Non-streaming helper: returns reconstructed response text."""
        url = f"{self.base_url}/api/generate"
        payload = self._generate_payload(prompt)
        try:
            resp = requests.post(url, json=payload, stream=True, timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Failed to contact Ollama at {url}: {e}") from e

        full = []
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            r = obj.get("response")
            if r:
                full.append(r)
            if obj.get("done") is True:
                break
        return "".join(full).strip()


ollama = OllamaClient()


class ITAssistant:
    def __init__(self, client=ollama, system_prompt=SYSTEM_PROMPT):
        self.client = client
        self.system_prompt = system_prompt

        # Load safe actions from JSON file in the same folder as this script
        safe_actions_path = os.path.join(os.path.dirname(__file__), "safe_actions.json")
        if os.path.exists(safe_actions_path):
            with open(safe_actions_path, "r") as f:
                self.safe_actions = json.load(f)
        else:
            self.safe_actions = {}
            print(f"Warning: {safe_actions_path} not found. No safe actions loaded.")

    def build_prompt(self, user_question):
        return f"{self.system_prompt}\n\nUser: {user_question}\n\nAssistant:"

    def ask(self, question):
        prompt = self.build_prompt(question)
        return self.client.generate(prompt)

    def generate_script(self, instruction, language="powershell"):
        prompt = (
            f"{self.system_prompt}\n\n"
            f"Generate a {language} script for this task. Include comments and do NOT execute it:\n\n"
            f"Task: {instruction}\n\n"
            f"Return only the script inside code fences.\n"
        )
        return self.client.generate(prompt)

    def list_safe_actions(self):
        return list(self.safe_actions.keys())

    def get_action_command(self, action_name):
        """Return the command string for a given safe action, or None if not found."""
        return self.safe_actions.get(action_name)
    
    def run_safe(self, action_name):
        """
        Execute a whitelisted action safely and return output as a string.
        """
        cmd = self.get_action_command(action_name)
        if not cmd:
            return f"Error: '{action_name}' is not a recognized safe action."

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.stderr.strip() if e.stderr else str(e)}"