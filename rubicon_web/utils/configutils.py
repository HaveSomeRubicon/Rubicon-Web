import os
from utils.logger import log


default_config = {
    "theme": "matte black",
    "reopen_last_session": True,
    "default_url": "https://ecosia.org/",
    "search_url": "https://www.ecosia.org/search?q=%s",
    "show_window_management_buttons": False,
    "config_version": 1,
}
default_themes = {
    "matte black": {
        "colors": {
            "bg_color": "rgb(35, 35, 35)",
            "nav_bar_bg_color": "rgb(21, 21, 21)",
            "nav_bar_accent_color": "rgb(255, 255, 255)",
            "nav_bar_hover_color": "rgba(202, 202, 202, 30)",
            "nav_bar_focus_color": "rgb(10, 10, 10)",
            "url_bar_bg_color": "rgb(21, 21, 21)",
            "tab_bar_bg_color": "rgb(21, 21, 21)",
            "tab_bg_color": "rgb(21, 21, 21)",
            "tab_bar_accent_color": "rgb(255, 255, 255)",
            "tab_font_color": "rgb(255, 255, 255)",
            "tab_hover_color": "rgba(202, 202, 202, 30)",
            "tab_focus_color": "rgb(10, 10, 10)",
        },  
        "theme version": 1
    },
    "red": {
        "colors": {
            "bg_color": "rgb(255, 98, 98)",
            "nav_bar_bg_color": "rgb(255, 45, 45)",
            "nav_bar_accent_color": "rgb(255, 255, 255)",
            "nav_bar_hover_color": "rgba(255, 200, 200, 50)",
            "nav_bar_focus_color": "rgb(255, 69, 69)",
            "url_bar_bg_color": "rgb(255, 45, 45)",
            "tab_bar_bg_color": "rgb(255, 69, 69)",
            "tab_bg_color": "rgb(255, 69, 69)",
            "tab_bar_accent_color": "rgb(255, 255, 255)",
            "tab_font_color": "rgb(255, 255, 255)",
            "tab_hover_color": "rgba(255, 200, 200, 50)",
            "tab_focus_color": "rgb(255, 45, 45)",
        },
        "theme version": 1
    }
}

# profile_dir is the directory which contains config files, themes and other import files that Rubicon Web uses
if os.name == "nt":
    profile_dir = f"C:\\Users\\{os.getlogin()}\\.HaveSomeRubicon\\Rubicon-Web"
else:
    profile_dir = f"/home/{os.getlogin()}/.config/Rubicon-Web"
log(f"Set profile_dir to {profile_dir}", "SUCCESS", "configutils.py")
# web_engine_profile_dirs contains files that QWebEngineView uses
web_engine_profile_dirs = {key: (profile_dir + ("\\WebEngineView\\" if os.name == "nt" else "/WebEngineView/") + value) for key, value in {"cachePath": "cache", "persistentStoragePath": "persistentStorage"}.items()}
log(f"Set web_engine_profile_dirs to {web_engine_profile_dirs}", "SUCCESS", "configutils.py")
# This is the path to the config file
config_file_path = os.path.join(profile_dir, "config.py")
log(f"Set config_file_path to {config_file_path}", "SUCCESS", "configutils.py")
# This is the path to the themes file
theme_file_path = os.path.join(profile_dir, "theme.py")
log(f"Set theme_file_path to {theme_file_path}", "SUCCESS", "configutils.py")
# This is the path to the last session file
last_session_path = os.path.join(profile_dir, "last_session.py")
log(f"Set last_session_path to {last_session_path}", "SUCCESS", "configutils.py")

def check_for_profile_dir():
    """Creates a profile directory if it doesn't exist"""
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
        log("Profile directory was missing. It has been recreated.", "NOTICE", "configuitls.py")


def check_for_config():
    """Creates a config file if it doesn't exist"""
    check_for_profile_dir()
    if not os.path.exists(config_file_path):
        with open(config_file_path, "w") as config_file:
            config_file.write(str(default_config))
        log("Config file was missing. It has been recreated.", "NOTICE", "configuitls.py")


def get_config():
    """Returns config"""
    check_for_config()
    with open(config_file_path, "r") as config_file:
        return eval(config_file.read())


def check_for_theme():
    """Creates a themes file if it doesn't exist"""
    check_for_profile_dir()
    if not os.path.exists(theme_file_path):
        with open(theme_file_path, "w") as theme_file:
            theme_file.write(str(default_themes))
        log("Themes file was missing. It has been recreated.", "NOTICE", "configuitls.py")


def get_themes():
    """Returns themes"""
    check_for_theme()
    with open(theme_file_path, "r") as theme_file:
        return eval(theme_file.read())


def check_for_web_engine_dirs():
    """Creates a web_engine_dirs if they don't exist"""
    for web_engine_dir in web_engine_profile_dirs.values():
        if not os.path.exists(web_engine_dir):
            os.makedirs(web_engine_dir)
            log(f"{web_engine_dir} was missing. It has been recreated.", "NOTICE", "configuitls.py")


def get_cache_dir():
    """Returns the web engine cache directory"""
    check_for_web_engine_dirs()
    return web_engine_profile_dirs["cachePath"]


def get_persistent_storage_dir():
    """Returns the persistent storage directory"""
    check_for_web_engine_dirs()
    return web_engine_profile_dirs["persistentStoragePath"]