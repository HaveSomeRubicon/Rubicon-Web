import os
import time


if os.name == "nt":
    PROFILE_DIRECTORY = f"C:\\Users\\{os.getlogin()}\\.HaveSomeRubicon\\Rubicon-Web"
else:
    PROFILE_DIRECTORY = f"/home/{os.getlogin()}/.config/Rubicon-Web"
LOG_FILE_PATH = os.path.join(PROFILE_DIRECTORY, "logs.txt")

def log(message, type, source_file):
    type = type.upper()
    formatted_time = time.strftime("%m/%d/%Y %H:%M:%S")
    formatted_message = f"[{type} {formatted_time} {source_file}] {message}"

    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(formatted_message)

    ansi_color_codes = {
        "OKAY": "",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
    }
    if type in list(ansi_color_codes.keys()):
        ansi_color_code = ansi_color_codes[type]
    else:
        ansi_color_code = ""
    ansi_end_code = "\033[0m"
    
    print(ansi_color_code, formatted_message, ansi_end_code)