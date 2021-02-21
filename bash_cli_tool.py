import os
import sys

def get_path_to_profile():
    home_dir = os.environ["HOME"]
    shell = os.environ["SHELL"]
    if "bash" in shell:
        #bash_profile = home_dir + "/.bash_profile"
        bashrc = home_dir + "/.bashrc"
        #if os.path.exists(bash_profile):
        #    return bash_profile
        if os.path.exists(bashrc):
            return bashrc
        else:
            raise AssertionError("No .bashrc or .bash_profile file found in HOME directory: " + home_dir)
    elif "zsh" in shell:
        zsh_profile = home_dir + "/.zprofile"
        zshrc = home_dir + "./zshrc"
        if os.path.exists(zsh_profile):
            return zsh_profile
        elif os.path.exists(zsh_profile):
            return zshrc
        else:
            raise AssertionError("No .zprofile or zshrc file found in Home directory: " + home_dir)
    else:
        AssertionError("Unsupported shell type: {0} expected either bash or zsh".format(shell))

PATH_TO_PROFILE = get_path_to_profile()

def append_or_replace_to_shell_profile(key: str, value: str):
    append_or_replace_var_text(key, value, PATH_TO_PROFILE)

def append_or_replace_var_text(key:str, value: str, path_to_profile: str) -> None:
    """
    Will add environment variables to a text file. If already exists will replace them
    :param key: variable name to add
    :param value: value for variables
    :param path_to_bash_profile: path to file to add to
    :return: None
    """
    var_in_text = variable_in_text(key, path_to_profile)
    if var_in_text[0]:
        line_number=var_in_text[1]
        replace_variable(line_number, key, value, path_to_profile)
        return
    add_variable_to_text(key, value, path_to_profile)

def variable_in_text(key: str, path_to_file: str) -> tuple:
    """
    Tells whether or not the variable is the file. Looks for export as indicating a variable
    :param key: name of var
    :param path_to_file: path to the file
    :return: tuple in format (true/false, line_number)
    """
    file = open(path_to_file, 'r')
    bash_copy = file.readlines()
    file.close()
    for line_number in range(len(bash_copy)):
        line=bash_copy[line_number]
        if line == "\n":
            continue
        line_split = line.split(" ")
        if line_split[0] == "export":
            line_key = line_split[1].split("=")[0]
            if line_key == key:
                return True, line_number
    return False, 0

def replace_variable(line_number: int, key: str, value: str, path_to_file: str) -> None:
    """
    replace variable in file
    :param line_number: line number var on
    :param key: key for var
    :param value: value for key
    :param path_to_file: path to file
    :return: None
    """
    file = open(path_to_file, 'r')
    file_lines = file.readlines()
    file.close()
    del file_lines[line_number]
    new_file = open(path_to_file, 'w+')
    for line in file_lines:
        new_file.write(line)
    new_file.close()
    add_variable_to_text(key, value, path_to_file)

def add_variable_to_text(key: str, value: str, path_to_file):
    """
    Appends variabel to end of file
    :param key: variable name
    :param value: variable value
    :param path_to_file: path to file
    :return: None
    """
    file = open(path_to_file, 'a')
    file.write("\n")
    if " " in value:
        new_line='export {0}="{1}"'.format(key, value)
    else:
        new_line = 'export {0}={1}'.format(key, value)
    file.write(new_line)
    file.write("\n")
    file.close()

if __name__ == "__main__":
    path = r"c\Users\ianm1\PycharmProjects\CLI_tool_project\test.txt"
    linux_path = "/c/Users/ianm1/PycharmProjects/CLI_tool_project/test.txt"
    append_or_replace_var_text("test3", "new value", linux_path)