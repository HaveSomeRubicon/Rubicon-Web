import os
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..tabs.tabs import Tabs
from ..tab_widgets.tab_widgets import TabWidgets
from ..window_management_buttons.window_management_buttons import WindowManagementButtons


themes = {
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


class MainWindow(QMainWindow):
    def __init__(self, config, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("homie-web/widgets/mainwindow/mainwindow.ui", self)
        
        self.CONFIG = config
        
        self.THEME = themes[self.CONFIG["theme"]]
        
        self.tab_widgets = TabWidgets()
        self.main_layout.addWidget(self.tab_widgets)
        
        self.tabs = Tabs(self)
        self.tab_bar_layout.addWidget(self.tabs)
        
        self.window_management_buttons = WindowManagementButtons()
        self.tab_bar_layout.addWidget(self.window_management_buttons)
        
        self.default_qurl = QUrl("https://ecosia.org/")
        self.default_tab = lambda: self.tabs.new_web_view_tab(self.default_qurl)
        self.default_tab()
        
        self.back_button.clicked.connect(lambda: self.tab_widgets.currentWidget().back())

        self.forward_button.clicked.connect(lambda: self.tab_widgets.currentWidget().forward())

        self.new_tab_button.clicked.connect(self.default_tab)
        
        self.main_layout.setSizes([0])
        
        widgets_with_stylesheets = [self.centralwidget, self.nav_bar, self.top_bar, self.tab_bar, self.window_management_buttons]
        self.init_stylesheets(widgets_with_stylesheets)
        
        self.setWindowTitle("Homie Web")
    
    def init_stylesheets(self, widgets):
        for widget in widgets:
            widget.hide()
            widget_stylesheet = widget.styleSheet()
            for key in self.THEME["colors"].keys():
                widget_stylesheet = widget_stylesheet.replace('/' + key + '/', self.THEME["colors"][key])
            widget.setStyleSheet(widget_stylesheet)
            widget.show()