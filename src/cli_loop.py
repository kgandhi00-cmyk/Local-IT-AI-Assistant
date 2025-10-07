from src.assistant import ITAssistant
import json

assistant = ITAssistant()

def main():
    print("Welcome to the Local IT Assistant interactive CLI!")
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
  ask <question>           - Ask a question to the assistant
  gen-script <task>        - Generate a PowerShell script for a task
  list-actions             - Show whitelisted safe actions
  run-action <action>      - Execute a whitelisted safe action
  help                     - Show this help text
  exit / quit              - Exit the CLI
            """)
            continue

        parts = cmd.split(" ", 1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        try:
            if command == "ask" and arg:
                print(assistant.ask(arg))
            elif command == "gen-script" and arg:
                script = assistant.generate_script(arg)
                print(script)
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
            else:
                print("Unknown command or missing argument. Type 'help' for commands.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()