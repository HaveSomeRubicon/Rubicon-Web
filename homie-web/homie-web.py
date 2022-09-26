#! /bin/env python3
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget

from widgets.navbar import NavBar
from widgets.tabbed_browser import TabbedBrowser
from widgets.load_progress_bar import LoadProgressBar
from widgets.main_window import MainWindow


app = QApplication(sys.argv)
app.setApplicationName("Homie Web")

window = MainWindow()
window.show()

app.exec()