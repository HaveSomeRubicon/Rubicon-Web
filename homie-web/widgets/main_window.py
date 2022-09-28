import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

from widgets.navbar import NavBar
from widgets.tabbed_browser import TabbedBrowser
from widgets.load_progress_bar import LoadProgressBar


basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Homie Web Test')
        self.setWindowIcon(QIcon(os.path.join(basedir, "assets/png/Homie Web Logo.png")))

        # Create the navbar and show it
        self.navbar = NavBar(self)
        self.addToolBar(self.navbar)

        # Create layout
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        # Create and add tabbed browser to layout
        self.tabbed_browser = TabbedBrowser(self)
        self.main_layout.addWidget(self.tabbed_browser)

        # Create and add load progress bar to layout
        self.load_progress_bar = LoadProgressBar()
        self.main_layout.addWidget(self.load_progress_bar)

        # Open new tab on start
        self.tabbed_browser.new_tab()
        
        # Set the tabs widget as central widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)