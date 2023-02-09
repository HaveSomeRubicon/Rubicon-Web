import os
import time


if os.name == "nt":
    profile_dir = f"C:\\Users\\{os.getlogin()}\\.HaveSomeRubicon\\Rubicon-Web"
else:
    profile_dir = f"/home/{os.getlogin()}/.config/Rubicon-Web"
if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)
log_file_path = os.path.join(profile_dir, "logs.txt")

def log(message, type, source_file):
    formatted_time = time.strftime("%m/%d/%Y %H:%M:%S")
    formatted_message = f"[{type.upper()} {formatted_time} {source_file}] {message}"
    print(formatted_message)
    with open(log_file_path, "a") as log_file:
        log_file.write(formatted_message)

# This is the path to the log file
log(f"Set log_file_path to {log_file_path}", "SUCCESS", "configutils.py")