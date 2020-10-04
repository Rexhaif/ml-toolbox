#!/usr/bin/env python
import os
import argparse as ap

from notebook.auth import passwd


def replace_password_line(hashed_password: str, config_file: str):
    with open(config_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if "c.NotebookApp.password " in lines[i]:
            lines[i] = f"c.NotebookApp.password = '{hashed_password}'"

    with open(config_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + os.linesep)


if __name__ == "__main__":
    parser = ap.ArgumentParser(prog='hashpwd.py', description="Helper script for changing jupyter notebook password")
    parser.add_argument("-p", "--path", type=str, required=False, default=f"{os.environ['HOME']}/.jupyter/jupyter_notebook_config.py")
    parser.add_argument("--password", type=str, required=True)

    args: ap.Namespace = parser.parse_args()
    hashed_password = passwd(args.password)
    print("Your hashed password is: ", hashed_password)
    print("Writing it to the config file: ", args.path)
    replace_password_line(hashed_password, args.path)


