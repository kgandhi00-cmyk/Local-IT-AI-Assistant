# Local AI Assistant for IT Operations  
**Deploying a Self-Hosted LLM with Secure System Integration**

[![Python](https://img.shields.io/badge/Python-3.13.7-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Repo Status](https://img.shields.io/badge/Status-Phase%201-yellow)](README.md)

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Technology Stack](#technology-stack)  
4. [System Requirements](#system-requirements)  
5. [Setup Instructions](#setup-instructions)  
6. [Next Steps (Phase 2)](#next-steps-phase-2)  
7. [Notes](#notes)

---

## Project Overview

This project showcases my skills as an IT/Cybersecurity professional. The goal is to build a **self-hosted LLM** trained and prompt-tuned to assist with system administration tasks, including PowerShell scripting, log parsing, and local system management.  

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

## Setup Instructions

1. **Clone the repository**
```powershell
git clone https://github.com/<your-username>/LocalITAssistant.git
cd LocalITAssistant
