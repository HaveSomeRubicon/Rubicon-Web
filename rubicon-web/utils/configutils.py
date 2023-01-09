import os


default_config = {
    "theme": "matte black",
    "default_url": "https://ecosia.org/",
    "show_window_management_buttons": False,
}

if os.name == "nt":
    user_config_dir = f"C:\\Users\\{os.getlogin()}\\.HaveSomeRubicon\\Rubicon-Web"
else:
    user_config_dir = f"/home/{os.getlogin()}/.config/Rubicon-Web/"
config_file_path = os.path.join(user_config_dir, "config.py")


def check_for_config():
    if not os.path.exists(user_config_dir):
        os.makedirs(user_config_dir)
        with open(config_file_path, "w") as config_file:
            config_file.write(str(default_config))


def get_config():
    check_for_config()
    with open(config_file_path, "r") as config_file:
        return eval(config_file.read())