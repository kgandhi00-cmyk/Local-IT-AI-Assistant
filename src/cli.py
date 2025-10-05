from src.assistant import ITAssistant
import argparse
import json
import subprocess

assistant = ITAssistant()

def cmd_ask(args):
    print("Asking assistant...\n")
    resp = assistant.ask(args.question)
    print(resp)

def cmd_generate_script(args):
    print("Requesting generated script from assistant...\n")
    script = assistant.generate_script(args.instruction, language=args.lang)
    print(script)

def cmd_list_actions(args):
    actions = assistant.list_safe_actions()
    print("Available safe actions:")
    for a in actions:
        print(" -", a)

def cmd_execute_action(args):
    action = args.action
    cmd_list = assistant.get_action_command(action)
    if not cmd_list:
        print(f"Unknown or disallowed actions: {action}")
        return
    print(f"Executing safe actions: {action}")
    # run powershell cmd, capture output
    try:
        res = subprocess.run(cmd_list, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        print("Action timed out.")
        return
    if res.returncode != 0:
        print("Action failed (non-zero exit):", res.stderr)
        return
    # if JSON result; neat print
    try:
        parsed = json.loads(res.stdout)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print(res.stdout)

def main():
    parser = argparse.ArgumentParser(prog="itassistant")
    sub = parser.add_subparsers(dest="cmd")

    a = sub.add_parser("ask"); a.add_argument("question"); a.set_defaults(func=cmd_ask)
    b = sub.add_parser("gen-script"); b.add_argument("instruction"); b.add_argument("--lang", default="powershell"); b.set_defaults(func=cmd_generate_script)
    c = sub.add_parser("list-actions"); c.set_defaults(func=cmd_list_actions)
    d = sub.add_parser("run-action"); d.add_argument("action"); d.set_defaults(func=cmd_execute_action)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__=="__main__":
    main()