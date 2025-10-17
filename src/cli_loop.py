from src.assistant import ITAssistant
import json
import os
import datetime

assistant = ITAssistant()

# File where conversation history will be logged
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FOLDER = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_FOLDER, exist_ok=True)  # create folder if it doesn't exist

LOG_FILE = os.path.join(LOG_FOLDER, "conversation_log.txt")

# Keep in-memory context for the current session
conversation_history = []

def log_message(role, message):
    """Append messages to a text log for recordkeeping."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role.upper()}: {message}\n")
    conversation_history.append({"role": role, "content": message})


def build_context_prompt(user_input):
    """Combine past messages into a context-aware prompt."""
    context = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history[-5:]]  # last 5 exchanges
    )
    return f"{context}\nUser: {user_input}\nAssistant:"


def main():
    print("Welcome to the Local IT Assistant interactive CLI with memory!")
    print("Type 'help' for commands, 'exit' to quit.\n")

    while True:
        cmd = input(">>> ").strip()
        if not cmd:
            continue
        if cmd.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif cmd.lower() == "help":
            print("""
Commands:
  ask <question>           - Ask a question to the assistant (with conversation context)
  gen-script <task>        - Generate a PowerShell script for a task
  list-actions             - Show whitelisted safe actions
  run-action <action>      - Execute a whitelisted safe action
  show-log                 - Display this session's chat log
  clear-memory             - Clear the in-memory conversation context
  help                     - Show this help text
  exit / quit              - Exit the CLI
            """)
            continue

        parts = cmd.split(" ", 1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        try:
            if command == "ask" and arg:
                prompt = build_context_prompt(arg)
                response = assistant.client.generate(prompt)
                print(response)
                log_message("user", arg)
                log_message("assistant", response)

            elif command == "gen-script" and arg:
                script = assistant.generate_script(arg)
                print(script)
                log_message("user", f"Generated script for: {arg}")
                log_message("assistant", script)

            elif command == "list-actions":
                actions = assistant.list_safe_actions()
                print("Available safe actions:")
                for a in actions:
                    print(" -", a)

            elif command == "run-action" and arg:
                output = assistant.run_safe(arg)
                try:
                    parsed = json.loads(output)
                    print(json.dumps(parsed, indent=2))
                except Exception:
                    print(output)
                log_message("user", f"Executed safe action: {arg}")
                log_message("assistant", output)

            elif command == "show-log":
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r", encoding="utf-8") as f:
                        print(f.read())
                else:
                    print("No log file found yet.")

            elif command == "clear-memory":
                conversation_history.clear()
                print("Conversation memory cleared.")

            else:
                print("Unknown command or missing argument. Type 'help' for commands.")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()