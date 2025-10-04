# Local AI Assistant for IT Operations  
**Deploying a Self-Hosted LLM with Secure System Integration**

This is a personal project showcasing my skills as an IT/Cybersecurity professional. The goal is to build a **self-hosted LLM** trained and prompt-tuned to assist with system administration tasks, including but not limited to PowerShell scripting and log parsing.  

The assistant will be able to:  
- Parse and answer IT-related questions (e.g., “What PowerShell command resets a user password?”)  
- Generate or review scripts for system tasks  
- Safely query local system information  
- Be accessed securely via a local **web interface** or **CLI**

---

## Features

- **Local LLM deployment**: Provides AI assistance without requiring an internet connection  
- **Integration with system utilities**: Interacts with Windows tools and scripts  
- **Flexible interface**: CLI and web-based access via terminal or browser  
- **Custom prompt tuning**: Specialized for IT and sysadmin tasks  

---

## Technology Stack

- **Ollama** – LLM backend  
- **Docker Desktop** – Containerization  
- **Python** – Scripting and automation  
- **FastAPI** – API layer framework  
- **Gradio** – Web-based user interface  

---

## System Requirements

- **Operating System:** Windows 11  
- **RAM:** 16 GB minimum (32 GB recommended)  
- **GPU:** 8 GB VRAM (preferably higher)  
- **Disk Space:** ~10–30 GB for models and cache  

---

## Notes

- Sensitive information (e.g., API keys) is stored in a `.env` file, **NOT in code**  
- The repository includes `.gitignore` to exclude virtual environments, model caches, and secrets  
- This project is intended for **local, private use only**
