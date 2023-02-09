import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir

from widgets.mainwindow.mainwindow import MainWindow
from utils import configutils
from utils.logger import log


def main():
    """This function starts Rubicon Web"""
    log("Rubicon Web is starting", "OKAY", "rubicon_web.py")
    app = QApplication(sys.argv)
    log("QApplication was successfully created", "SUCCESS", "rubicon_web.py")

    # Sets app_dir to the directory containing Rubicon Web files
    if getattr(sys, "frozen", False):
        app_dir = sys._MEIPASS
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    log(f"Set app_dir to {app_dir}", "SUCCESS", "rubicon_web.py")

    window = MainWindow(None, configutils, log, app_dir)
    window.show()

    log("QApplication is executing", "OKAY", "rubicon_web.py")
    app.exec()
    log("QApplication has closed", "OKAY", "rubicon_web.py")
    log("Rubicon Web has closed", "OKAY", "rubicon_web.py")


if __name__ == "__main__":
    main()
