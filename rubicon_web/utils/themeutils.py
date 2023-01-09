import os


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

if os.name == "nt":
    user_theme_dir = f"C:\\Users\\{os.getlogin()}\\.HaveSomeRubicon\\Rubicon-Web"
else:
    user_theme_dir = f"/home/{os.getlogin()}/.config/Rubicon-Web/"
theme_file_path = os.path.join(user_theme_dir, "themes.py")


def check_for_theme():
    if not os.path.exists(user_theme_dir):
        os.makedirs(user_theme_dir)
    with open(theme_file_path, "w") as theme_file:
        theme_file.write(str(default_themes))


def get_theme():
    check_for_theme()
    with open(theme_file_path, "r") as theme_file:
        return eval(theme_file.read())