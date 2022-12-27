import os
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.uic import loadUi

from ..web_engine.web_engine import WebEngineView


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
    def __init__(self, config, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("homie-web/widgets/mainwindow/mainwindow.ui", self)
        
        self.config = config
        
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
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.tabMoved.connect(self.tab_moved)
        
        self.default_qurl = QUrl("https://ecosia.org/")
        self.default_tab = lambda: self.new_web_view_tab(self.default_qurl)
        self.default_tab()
        
        self.back_button.clicked.connect(lambda: self.web_views.currentWidget().back())

        self.forward_button.clicked.connect(lambda: self.web_views.currentWidget().forward())

        self.new_tab_button.clicked.connect(self.default_tab)
        
        self.main_layout.setSizes([0])
        
        self.setWindowTitle("Homie Web")

    def new_tab(self, widget, title: str = "Untitled tab", icon: QIcon = None, background: bool = True):
        if icon is not None:
            tab_index = self.tabs.addTab(icon, title)
        else:
            tab_index = self.tabs.addTab(title)
        self.web_views.addWidget(widget)
        
        if not background:
            self.tabs.setCurrentIndex(tab_index)
        
        self.web_views.widget(tab_index).setAttribute(Qt.WA_DeleteOnClose, True)
        
        return tab_index
    
    def new_web_view_tab(self, url: QUrl = None, background: bool = False):
        browser = WebEngineView(self)
        if url != None:
            browser.setUrl(url)
        tab_index = self.new_tab(browser, "Loading...", background = background)
        
        def browser_load_started():
            self.reload_and_stop_button.setText("9")
            self.reload_and_stop_button.clicked.connect(lambda: self.web_views.currentWidget().stop())
        
        def browser_load_finished():
            self.reload_and_stop_button.setText("Z")
            self.reload_and_stop_button.clicked.connect(lambda: self.web_views.currentWidget().reload())
            
            title = browser.page().title()
            icon = browser.page().icon()
            self.tabs.setTabText(tab_index, title)
            self.tabs.setTabIcon(tab_index, icon)
        
        browser.loadProgress.connect(browser_load_started)
        browser.loadFinished.connect(browser_load_finished)
        
        return tab_index
    
    def close_tab(self, tab_index):
        if self.tabs.count() <= 1:
            # TODO: Open a dialog to ask the user if they want to close entire web browser when all tabs are closed
            sys.exit()
        else:
            browser = self.web_views.widget(tab_index)
            browser.close()
            self.web_views.removeWidget(self.web_views.widget(tab_index))
            self.tabs.removeTab(tab_index)
    
    def tab_changed(self, tab_index):
        self.web_views.setCurrentIndex(tab_index)
    
    def tab_moved(self, to, _from):
        moved_tab_widget = self.web_views.widget(_from)
        self.web_views.removeWidget(moved_tab_widget)
        self.web_views.insertWidget(to, moved_tab_widget)