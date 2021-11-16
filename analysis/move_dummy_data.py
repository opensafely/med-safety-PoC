from argparse import ArgumentParser
from pathlib import Path
import os, sys

parser = ArgumentParser(description="Move dummy data")

parser.add_argument(
    "--origin",
    help="Defining the path of the files to be moved",
)

parser.add_argument(
    "--destination",
    help="Defining where the files should be moved to",
    type=Path
)

options = parser.parse_args()

def existing_directory(value):
    path = Path(value)
    if not path.exists():
        raise ValueError(f"{value} does not exit")
    return path

try:
    existing_directory(options.destination)
except ValueError:
    print(f"The destination directory '{options.destination}' does not exist")
    sys.exit()

# mv_command = f"cp {options.origin} {options.destination}"

# print(f"Executing [{mv_command}]")
# os.system(mv_command)

rename_command_list = [f"for f in {options.destination}/*.csv",
                        'do echo mv "$f" "${f/input_/data_}"',
                        'done']
rename_command = "; ".join(rename_command_list)

print(f"Executing [{rename_command}]")
os.system(rename_command)

