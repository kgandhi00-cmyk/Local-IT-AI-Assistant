import os
import json
from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from dotenv import load_dotenv
from src.assistant import ITAssistant
import logging

load_dotenv()
API_KEY = os.getenv("ASSISTANT_API_KEY") # set in .env locally
PORT = int(os.getenv("API_PORT", 8000))

app = FastAPI(title="Local IT Assistant API")
assistant =ITAssistant()

logging.basicConfig(filename="logs/api.log", level=logging.INFO, format="%(asctime)s %(message)s")

def check_api_key(x_api_key: str = Header(None)):
    if API_KEY and x_api_key !=API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
class AskRequest(BaseModel):
    question: str

class ScriptRequest(BaseModel):
    instruction: str
    language: str = "powershell"

class ActionRequest(BaseModel):
    action: str

@app.post("/ask")
def ask(req: AskRequest, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    logging.info("ASK: %s", req.question)
    resp = assistant.ask(req.question)
    logging.info("RESP: %s", resp[:300])
    return {"answer": resp}

@app.post("/generate_script")
def generate_script(req: ScriptRequest, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    logging.info("GEN_SCRIPT: %s", req.instruction)
    script = assistant.generate_script(req.instruction, language=req.language)
    return {"script": script}

@app.post("/run_action")
def run_action(req: ActionRequest, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    cmd = assistant.get_action_command(req.action)
    if not cmd:
        raise HTTPException(status_code=400, detail="Unknown or disallowed action")
    # run cmd (same as CLI)
    import subprocess, json
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Action timed out")
    if res.returncode != 0:
        raise HTTPException(statust_code=500, detail=f"Action failed: {res.stderr}")
    try:
        parsed = json.loads(res.stdout)
        return {"result": parsed}
    except Exception:
        return {"result": res.stdout}
    
@app.get("/health")
def health():
    return {"status": "ok"}