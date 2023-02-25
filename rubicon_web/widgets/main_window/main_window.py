import os
import sys
import time
from pathlib import PureWindowsPath, PurePosixPath

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QSizePolicy

from ..top_bar.top_bar import TopBar
from ..tab_widgets.tab_widgets import TabWidgets


class MainWindow(QMainWindow):
    def __init__(self, parent, application_directory, log_function, *args, **kwargs):
        """Initializes the main window"""
        super(MainWindow, self).__init__(parent=parent, *args, **kwargs)
        log_function("MainWindow is being initialized", "OKAY", "mainwindow.py")

        self.setWindowTitle("Rubicon Web")
        
        self.log = log_function
        
        self.APPLICATION_DIRECTORY = application_directory
        if os.name == "nt":
            self.PROFILE_DIRECTORY = f"C:\\Users\\{os.getlogin()}\\.HaveSomeRubicon\\Rubicon-Web"
        else:
            self.PROFILE_DIRECTORY = f"/home/{os.getlogin()}/.config/Rubicon-Web"
        self.WEB_ENGINE_PROFILE_DIRECTORIES = {key: (self.PROFILE_DIRECTORY + ("\\WebEngineView\\" if os.name == "nt" else "/WebEngineView/") + value) for key, value in {"cachePath": "cache", "persistentStoragePath": "persistentStorage", }.items()}
        self.CONFIGURATION_FILE_PATH = os.path.join(self.PROFILE_DIRECTORY, "configuration.py")
        self.THEMES_FILE_PATH = os.path.join(self.PROFILE_DIRECTORY, "themes.py")
        self.LAST_SESSION_PATH = os.path.join(self.PROFILE_DIRECTORY, "last_session.py")
        
        self.DEFAULT_QURL = QUrl(self.get_configuration()["default_url"])

        self.relative_to_abs_path = lambda file_path: os.path.join(self.APPLICATION_DIRECTORY, file_path)
        self.nt_to_posix_path = lambda file_path: "".join(str(PurePosixPath(PureWindowsPath(file_path))).split("\\")[1:])

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget_layout.setSpacing(0)
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QSplitter(self.central_widget)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.main_layout.setHandleWidth(0)
        self.main_layout.setSizes([0])

        self.central_widget_layout.addWidget(self.main_layout)
        self.tab_widgets = TabWidgets(self)
        self.main_layout.addWidget(self.tab_widgets)

        self.top_bar = TopBar(self)
        self.central_widget_layout.insertWidget(0, self.top_bar)

        WIDGETS_WITH_STYLESHEETS = [
            self.central_widget,
            self.top_bar.nav_bar,
            self.top_bar,
            self.top_bar.tab_bar,
        ]
        self.init_stylesheets(WIDGETS_WITH_STYLESHEETS)

        # Sets window geometry to the geometry from the last session
        if os.path.exists(self.LAST_SESSION_PATH):
            with open(self.LAST_SESSION_PATH, "r") as last_session_file:
                last_session = eval(last_session_file.read())
                self.setGeometry(*last_session["window_geometry"])
                if last_session["maximized"]:
                    self.showMaximized()
        
        self.log("MainWindow has been initialized", "SUCCESS", "mainwindow.py")

    def init_stylesheets(self, widgets):
        """Applies themes converts relative paths to absolute paths in stylesheets"""
        self.log("Initializing stylesheets", "OKAY", "mainwindow.py")
        for widget in widgets:
            widget.hide()
            widget_stylesheet = widget.styleSheet()

            # Apply themes
            for key in self.get_current_theme()["colors"].keys():
                widget_stylesheet = widget_stylesheet.replace(
                    "/" + key + "/", self.get_current_theme()["colors"][key]
                )

            # Convert relative to absolute paths
            split_stylesheet = widget_stylesheet.split("*")
            for index in range(1, len(split_stylesheet), 2):
                file_path = self.relative_to_abs_path(split_stylesheet[index])
                if os.name == "nt":
                    file_path = self.nt_to_posix_path(file_path)
                split_stylesheet[index] = file_path
                widget_stylesheet = "".join(split_stylesheet)

            widget.show()
            widget.setStyleSheet(widget_stylesheet)
        self.log("Finished initializing stylesheets", "SUCCESS", "mainwindow.py")

    def closeEvent(self, event):
        """Saves the current session to the last session file"""
        self.log("Mainwindow is closing", "OKAY", "mainwindow.py")
        self.check_for_profile_directory()
        with open(self.LAST_SESSION_PATH, "w") as last_session_file:
            last_session = {
                "last_open_urls": [],
                "last_open_tab_index": 0,
                "window_geometry": [
                    self.geometry().x(),
                    self.geometry().y(),
                    self.geometry().width(),
                    self.geometry().height(),
                ],
                "maximized": self.isMaximized(),
            }
            if self.get_configuration()["reopen_last_session"]:
                last_session["last_open_urls"] = self.tab_widgets.get_open_urls()
                last_session["last_open_tab_index"] = self.tab_widgets.currentIndex()
            else:
                last_session["last_open_urls"] = [self.default_qurl.toString()]
                last_session["last_open_tab_index"] = 0
            last_session_file.write(str(last_session))
            self.log(
                f"Saved current session to {self.LAST_SESSION_PATH}",
                "SUCCESS",
                "mainwindow.py",
            )
            self.log("Mainwindow has been closed", "SUCCESS", "mainwindow.py")
    
    def check_for_profile_directory(self):
        """Creates a profile directory if it doesn't exist"""
        if not os.path.exists(self.PROFILE_DIRECTORY):
            os.makedirs(self.PROFILE_DIRECTORY)
            self.log("Profile directory was missing. It has been recreated.", "OKAY", "main_window.py")

    def check_for_configuration(self):
        """Creates a configuration file if it doesn't exist"""
        DEFAULT_CONFIGURATION = {
            "theme": "matte black",
            "reopen_last_session": True,
            "default_url": "https://ecosia.org/",
            "search_url": "https://www.ecosia.org/search?q=%s",
            "show_window_management_buttons": False,
            "configuration_version": 1,
        }
        self.check_for_profile_directory()
        if not os.path.exists(self.CONFIGURATION_FILE_PATH):
            with open(self.CONFIGURATION_FILE_PATH, "w") as configuration_file:
                configuration_file.write(str(DEFAULT_CONFIGURATION))
            self.log("Config file was missing. It has been recreated.", "OKAY", "main_window.py")

    def get_configuration(self):
        """Returns configuration"""
        self.check_for_configuration()
        with open(self.CONFIGURATION_FILE_PATH, "r") as configuration_file:
            return eval(configuration_file.read())

    def check_for_themes(self):
        """Creates a themes file if it doesn't exist"""
        DEFAULT_THEMES = {
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
                "theme version": 1,
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
                "theme version": 1,
            },
        }
        self.check_for_profile_directory()
        if not os.path.exists(self.THEMES_FILE_PATH):
            with open(self.THEMES_FILE_PATH, "w") as themes_file:
                themes_file.write(str(DEFAULT_THEMES))
            self.log("Themes file was missing. It has been recreated.", "OKAY", "main_window.py")

    def get_themes(self):
        """Returns themes"""
        self.check_for_themes()
        with open(self.THEMES_FILE_PATH, "r") as themes_file:
            return eval(themes_file.read())
    
    def get_current_theme(self):
        return self.get_themes()[self.get_configuration()["theme"]]

    def check_for_web_engine_dirs(self):
        """Creates a web_engine_dirs if they don't exist"""
        for web_engine_dir in self.WEB_ENGINE_PROFILE_DIRECTORIES.values():
            if not os.path.exists(web_engine_dir):
                os.makedirs(web_engine_dir)
                self.log(f"{web_engine_dir} was missing. It has been recreated.", "OKAY", "main_window.py")

    def get_cache_dir(self):
        """Returns the web engine cache directory"""
        self.check_for_web_engine_dirs()
        return self.WEB_ENGINE_PROFILE_DIRECTORIES["cachePath"]

    def get_persistent_storage_dir(self):
        """Returns the persistent storage directory"""
        self.check_for_web_engine_dirs()
        return self.WEB_ENGINE_PROFILE_DIRECTORIES["persistentStoragePath"]