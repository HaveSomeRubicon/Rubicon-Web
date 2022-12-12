import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.uic import loadUi


themes = {
    "matte black": {
        "colors": {
            "bg_color": "rgb(35, 35, 35)",
            "main_bar_bg_color": "rgb(21, 21, 21)",
            "main_bar_accent_color": "rgb(255, 255, 255)",
            "main_bar_hover_color": "rgba(202, 202, 202, 30)",
            "main_bar_focus_color": "rgb(10, 10, 10)",
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
            "main_bar_bg_color": "rgb(255, 45, 45)",
            "main_bar_accent_color": "rgb(255, 255, 255)",
            "main_bar_hover_color": "rgba(255, 200, 200, 50)",
            "main_bar_focus_color": "rgb(255, 69, 69)",
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
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("homie-web/widgets/mainwindow/mainwindow.ui", self)
        
        self.THEME = themes["red"]
        widgets_with_stylesheets = [self.centralwidget, self.navbar, self.main_bar, self.tab_bar, self.window_management_buttons]
        for widget in widgets_with_stylesheets:
            widget.hide()
            widget_stylesheet = widget.styleSheet()
            for key in self.THEME["colors"].keys():
                widget_stylesheet = widget_stylesheet.replace('/' + key + '/', self.THEME["colors"][key])
            widget.setStyleSheet(widget_stylesheet)
            widget.show()
        
        self.web_views = QStackedWidget()
        self.main_layout.addWidget(self.web_views)
        
        self.tabs.setDrawBase(False)
        self.tabs.setMovable(True)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.tabMoved.connect(self.tab_moved)
        
        self.setWindowTitle("Homie Web")

    def new_tab(self, widget, title: str = "Untitled tab", icon: QIcon = None):
        if icon is not None:
            self.tabs.addTab(icon, title)
        else:
            self.tabs.addTab(title)
        self.web_views.addWidget(widget)
        
        widget.setAttribute(Qt.WA_DeleteOnClose, True)
    
    def tab_changed(self, tab_index):
        self.web_views.setCurrentIndex(tab_index)
    
    def tab_moved(self, to, _from):
        moved_tab_widget = self.web_views.widget(_from)
        self.web_views.removeWidget(moved_tab_widget)
        self.web_views.insertWidget(to, moved_tab_widget)