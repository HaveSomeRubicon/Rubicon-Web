from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from widgets.top_bar.nav_bar.Ui_nav_bar import Ui_nav_bar
from widgets.top_bar.nav_bar.url_bar.url_bar import UrlBar


class NavBar(QWidget, Ui_nav_bar):
    def __init__(self, main_window, *args, **kwargs):
        super(NavBar, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.main_window = main_window
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.url_bar = UrlBar(self.main_window)
        self.nav_bar_layout.insertWidget(3, self.url_bar)
        
        self.default_tab = lambda: self.main_window.top_bar.tab_bar.tabs.new_web_view_tab(self.main_window.default_qurl)
        
        self.back_button.clicked.connect(lambda: self.main_window.tab_widgets.currentWidget().back())
        self.forward_button.clicked.connect(lambda: self.main_window.tab_widgets.currentWidget().forward())
        self.new_tab_button.clicked.connect(self.default_tab)