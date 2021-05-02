import argparse
import os
from bash_cli_tool import append_or_replace_var_text, get_path_to_profile, delete_var_in_txt
import subprocess

def create_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="CLI variables", description="Add permanent variables to shell")
    parser.add_argument("-k", "--key", required=False, help="Key for the environemnt variable. Will be saved in all caps "
                                                              "by default.")
    parser.add_argument("-v", "--value", required=False, help="Value for the environment variable")
    parser.add_argument("-c", "--caps", required=False, default="T", choices=["T", "F"],
                        help="Whether or not the variable will be saved in all caps. Allowed choices: 'T', 'F'. Will be 'T',"
                             "or True by default")
    parser.add_argument("-p", "--profile", required=False, default=get_path_to_profile(check_file=False),
                        help="path to the profile file, either .bashrc or .zshrc")
    parser.add_argument("-r", "--remove", required=False, help="Removes the variable matching that key from profile, "
                                                               "Will default to all caps by default.")
    return parser

parser = create_parse()
args = parser.parse_args()

def validate_arguments(args):
    """
    Validates the input. Will raise ValueError on these occasions:
    * Either -k and -v or -r are suppled as args
    * Checks that the profile is a valid path
    """
    profile = args.profile
    if not os.path.exists(profile):
        raise ValueError(f"Profile path: {args.profile} must be a valid file path")
    if not (args.key and args.value) or args.remove:
        raise ValueError("Must provide key and value flags or remove flag")

def main(args):
    validate_arguments(args)
    if (args.key and args.value):
        key = args.key
        if args.caps != "F":
            key = key.upper()
        print(f"this is getting executed! {args.profile}")
        append_or_replace_var_text(key, args.value, args.profile)
    if args.remove:
        print(f"remove is getting executed with profile: {args.profile}")
        delete_var_in_txt(args.remove, args.profile)
    subprocess.run(f"source {args.profile}", shell=True)

if __name__ == '__main__':
    main(args)