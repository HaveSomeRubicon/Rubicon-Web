import sys

from PyQt5.QtWidgets import QApplication

from widgets.mainwindow.mainwindow import MainWindow
from utils import configutils


def main():
    app = QApplication(sys.argv)
    
    window = MainWindow(configutils)
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()