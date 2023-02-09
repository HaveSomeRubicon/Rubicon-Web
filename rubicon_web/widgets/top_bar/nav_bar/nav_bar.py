from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from widgets.top_bar.nav_bar.Ui_nav_bar import Ui_nav_bar
from widgets.top_bar.nav_bar.url_bar.url_bar import UrlBar


class NavBar(QWidget, Ui_nav_bar):
    def __init__(self, parent, main_window, *args, **kwargs):
        """Initializes the navigation bar"""
        super(NavBar, self).__init__(parent=parent, *args, **kwargs)
        self.parent().parent().log("NavBar is being initialized", "OKAY", "nav_bar.py")
        self.setupUi(self)
        
        self.main_window = main_window
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.url_bar = UrlBar(self, self.main_window)
        self.nav_bar_layout.insertWidget(3, self.url_bar)
        
        self.back_button.clicked.connect(lambda: self.main_window.tab_widgets.currentWidget().back())
        self.forward_button.clicked.connect(lambda: self.main_window.tab_widgets.currentWidget().forward())
        self.parent().parent().log("NavBar has been initialized", "SUCCESS", "nav_bar.py")