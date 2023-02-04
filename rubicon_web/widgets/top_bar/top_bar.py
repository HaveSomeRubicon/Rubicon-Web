from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from widgets.top_bar.tab_bar.tab_bar import TabBar
from widgets.top_bar.nav_bar.nav_bar import NavBar


class TopBar(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super(TopBar, self).__init__(*args, **kwargs)
        
        self.main_window = main_window
        
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        self.top_bar_layout = QVBoxLayout()
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.setSpacing(0)
        self.setLayout(self.top_bar_layout)
        
        self.tab_bar = TabBar(self.main_window)
        self.top_bar_layout.addWidget(self.tab_bar)
        
        self.nav_bar = NavBar(self.main_window)
        self.nav_bar.new_tab_button.clicked.connect(self.tab_bar.tabs.default_tab)
        self.top_bar_layout.addWidget(self.nav_bar)