import os
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from ..top_bar.top_bar import TopBar
from ..tab_widgets.tab_widgets import TabWidgets


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
        self.default_qurl = QUrl(self.CONFIG["default_url"])
        
        self.tab_widgets = TabWidgets()
        self.main_layout.addWidget(self.tab_widgets)
        
        self.top_bar = TopBar(self)
        self.centralwidget_layout.insertWidget(0, self.top_bar)

        self.top_bar.nav_bar.default_tab()
        
        self.main_layout.setSizes([0])
        
        widgets_with_stylesheets = [self.centralwidget, self.top_bar.nav_bar, self.top_bar, self.top_bar.tab_bar]
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