'''import os
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
            return f"Command failed: {e.stderr.strip() if e.stderr else str(e)}"'''
import os
import json
import time
import logging
from dotenv import load_dotenv
import requests
import subprocess

load_dotenv()

# -------------------------
# Logging configuration
# -------------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)
logger = logging.getLogger(__name__)

# -------------------------
# Environment / Constants
# -------------------------
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

# -------------------------
# Ollama Client
# -------------------------
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
            logger.error(f"Failed to contact Ollama at {url}: {e}")
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
        logger.info(f"Generated response of length {len(''.join(full))} characters")
        return "".join(full).strip()


ollama = OllamaClient()

# -------------------------
# IT Assistant
# -------------------------
class ITAssistant:
    def __init__(self, client=ollama, system_prompt=SYSTEM_PROMPT):
        self.client = client
        self.system_prompt = system_prompt

        # Load safe actions from JSON file in the same folder as this script
        safe_actions_path = os.path.join(os.path.dirname(__file__), "safe_actions.json")
        if os.path.exists(safe_actions_path):
            with open(safe_actions_path, "r") as f:
                self.safe_actions = json.load(f)
            logger.info(f"Loaded {len(self.safe_actions)} safe actions from {safe_actions_path}")
        else:
            self.safe_actions = {}
            logger.warning(f"{safe_actions_path} not found. No safe actions loaded.")

    # -------------------------
    # LLM Interaction
    # -------------------------
    def build_prompt(self, user_question):
        return f"{self.system_prompt}\n\nUser: {user_question}\n\nAssistant:"

    def ask(self, question):
        logger.info(f"Asking question: {question}")
        response = self.client.generate(self.build_prompt(question))
        logger.info(f"Assistant response (truncated): {response[:100]}...")
        return response

    def generate_script(self, instruction, language="powershell"):
        logger.info(f"Generating {language} script for task: {instruction}")
        prompt = (
            f"{self.system_prompt}\n\n"
            f"Generate a {language} script for this task. Include comments and do NOT execute it:\n\n"
            f"Task: {instruction}\n\n"
            f"Return only the script inside code fences.\n"
        )
        response = self.client.generate(prompt)
        logger.info(f"Generated script length: {len(response)}")
        return response

    # -------------------------
    # Safe Action Management
    # -------------------------
    def list_safe_actions(self):
        logger.info(f"Listing safe actions: {list(self.safe_actions.keys())}")
        return list(self.safe_actions.keys())

    def get_action_command(self, action_name):
        cmd = self.safe_actions.get(action_name)
        if cmd:
            logger.info(f"Retrieved safe action '{action_name}': {cmd}")
        else:
            logger.warning(f"Attempted to retrieve unknown or unsafe action: '{action_name}'")
        return cmd

    def run_safe(self, action_name):
        """
        Execute a whitelisted action safely and return output as a string.
        """
        cmd = self.get_action_command(action_name)
        if not cmd:
            logger.warning(f"Run attempt on invalid action: '{action_name}'")
            return f"Error: '{action_name}' is not a recognized safe action."

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Executed safe action '{action_name}' successfully")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Safe action '{action_name}' failed: {e.stderr.strip() if e.stderr else str(e)}")
            return f"Command failed: {e.stderr.strip() if e.stderr else str(e)}"