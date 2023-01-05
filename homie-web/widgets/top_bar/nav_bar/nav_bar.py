from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class NavBar(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super(NavBar, self).__init__(*args, **kwargs)
        loadUi("homie-web/widgets/top_bar/nav_bar/nav_bar.ui", self)
        
        self.main_window = main_window
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.default_tab = lambda: self.main_window.top_bar.tab_bar.tabs.new_web_view_tab(self.main_window.default_qurl)
        
        self.back_button.clicked.connect(lambda: self.main_window.tab_widgets.currentWidget().back())
        self.forward_button.clicked.connect(lambda: self.main_window.tab_widgets.currentWidget().forward())
        self.new_tab_button.clicked.connect(self.default_tab)