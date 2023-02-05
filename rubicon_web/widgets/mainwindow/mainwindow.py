import os
import sys
from pathlib import PureWindowsPath, PurePosixPath

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow

from ..mainwindow.Ui_mainwindow import Ui_MainWindow
from ..top_bar.top_bar import TopBar
from ..tab_widgets.tab_widgets import TabWidgets


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent, configutils, log_function, app_dir, *args, **kwargs):
        log_function("MainWindow is being initialized", "NOTICE", "mainwindow.py")
        super(MainWindow, self).__init__(parent=parent, *args, **kwargs)
        self.setupUi(self)
        
        
        self.configutils = configutils
        self.log = log_function
        self.app_dir = app_dir
        self.profile_dir = configutils.profile_dir
        self.CONFIG = configutils.get_config()
        self.THEME = configutils.get_themes()[self.CONFIG["theme"]]
        self.default_qurl = QUrl(self.CONFIG["default_url"])

        self.relative_to_abs_path = lambda file_path: os.path.join(self.app_dir, file_path)
        self.nt_to_posix_path = lambda file_path: ''.join(str(PurePosixPath(PureWindowsPath(file_path))).split("\\")[1:])
        
        self.tab_widgets = TabWidgets(self)
        self.main_layout.addWidget(self.tab_widgets)
        
        self.top_bar = TopBar(self, self)
        self.centralwidget_layout.insertWidget(0, self.top_bar)

        self.main_layout.setSizes([0])
        
        widgets_with_stylesheets = [self.centralwidget, self.top_bar.nav_bar, self.top_bar, self.top_bar.tab_bar]
        self.init_stylesheets(widgets_with_stylesheets)
        
        if os.path.exists(self.configutils.last_session_path):
            with open(self.configutils.last_session_path, "r") as last_session_file:
                last_session = eval(last_session_file.read())
                self.setGeometry(*last_session["window_geometry"])
                if last_session["maximized"]:
                    self.showMaximized()
        
        self.setWindowTitle("Rubicon Web")
        self.log("MainWindow has been initialized", "SUCCESS", "mainwindow.py")
    
    def init_stylesheets(self, widgets):
        self.log("Initializing stylesheets", "NOTICE", "mainwindow.py")
        for widget in widgets:
            widget.hide()
            widget_stylesheet = widget.styleSheet()
            
            for key in self.THEME["colors"].keys():
                widget_stylesheet = widget_stylesheet.replace('/' + key + '/', self.THEME["colors"][key])

            split_stylesheet = widget_stylesheet.split('*')
            for index in range(1, len(split_stylesheet), 2):
                file_path = self.relative_to_abs_path(split_stylesheet[index])
                if os.name == 'nt':
                    file_path = self.nt_to_posix_path(file_path)
                split_stylesheet[index] = file_path
                widget_stylesheet = ''.join(split_stylesheet)

            widget.show()
            widget.setStyleSheet(widget_stylesheet)
        self.log("Finished initializing stylesheets", "SUCCESS", "mainwindow.py")
    
    def closeEvent(self, event):
        self.log("Mainwindow is closing", "NOTICE", "mainwindow.py")
        self.configutils.check_for_profile_dir()
        with open(self.configutils.last_session_path, "w") as last_session_file:
            last_session = {
                "last_open_urls": [], 
                "last_open_tab_index": 0, 
                "window_geometry": [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()], 
                "maximized": self.isMaximized(),
            }
            if self.CONFIG["reopen_last_session"]:
                last_session["last_open_urls"] = self.tab_widgets.get_open_urls()
                last_session["last_open_tab_index"] = self.tab_widgets.currentIndex()
            else:
                last_session["last_open_urls"] = [self.default_qurl.toString()]
                last_session["last_open_tab_index"] = 0
            last_session_file.write(str(last_session))
            self.log(f"Saved current session to {self.configutils.last_session_path}", "SUCCESS", "mainwindow.py")
            self.log("Mainwindow has been closed", "SUCCESS", "mainwindow.py")