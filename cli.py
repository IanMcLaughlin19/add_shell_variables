import argparse
import os
import bash_cli_tool
from bash_cli_tool import append_or_replace_to_shell_profile
parser = argparse.ArgumentParser(prog="CLI variables", description="Add permanent variables to shell")
parser.add_argument("command", help="command for file", type=str)
parser.add_argument("key", help="key to be added", type=str)
parser.add_argument("value", help="value to be added", type=str)
args = parser.parse_args()
if args.command == "set":
    append_or_replace_to_shell_profile(args.key, args.value)
    os.system("exec bash")