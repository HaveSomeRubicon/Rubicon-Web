import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir

from widgets.mainwindow.mainwindow import MainWindow
from utils import configutils


def main():
    app = QApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        app_dir = sys._MEIPASS
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    window = MainWindow(configutils, app_dir)
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()