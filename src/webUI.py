import gradio as gr
import requests
from dotenv import load_dotenv
import os

# Load .env from parent folder
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

API_URL = "http://127.0.0.1:8000/ask"
API_KEY = os.getenv("ASSISTANT_API_KEY")  # matches your .env

def ask_assistant(message, chat_history):
    """
    Send the latest user message to the /ask endpoint,
    and append the response to chat_history for multi-turn chat.
    """
    if not API_KEY:
        return "Error: ASSISTANT_API_KEY not found in .env", chat_history

    headers = {"x-api-key": API_KEY}  # Correct header for your backend
    payload = {"question": message}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "No response returned.")
    except Exception as e:
        answer = f"Error: {e}"

    chat_history.append((message, answer))
    return "", chat_history

with gr.Blocks() as demo:
    gr.Markdown("## 💬 Llama 3 IT Assistant")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask a question...")
    submit = gr.Button("Send")

    submit.click(ask_assistant, [msg, chatbot], [msg, chatbot])
    msg.submit(ask_assistant, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0", server_port=7860)