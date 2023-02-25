import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDir

from logger import log
from widgets.main_window.main_window import MainWindow


def main():
    """This function starts Rubicon Web"""
    log("Rubicon Web is starting", "OKAY", "rubicon_web.py")
    application = QApplication(sys.argv)
    log("QApplication was successfully created", "SUCCESS", "rubicon_web.py")
        
    # Sets application_directory to the directory containing Rubicon Web files
    if getattr(sys, "frozen", False):
        APPLICATION_DIRECTORY = sys._MEIPASS
    else:
        APPLICATION_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    
    main_window = MainWindow(None, APPLICATION_DIRECTORY, log)
    main_window.show()

    main_window.log("QApplication is executing", "OKAY", "rubicon_web.py")
    application.exec()
    main_window.log("QApplication has closed", "OKAY", "rubicon_web.py")
    main_window.log("Rubicon Web has closed", "OKAY", "rubicon_web.py")

if __name__ == "__main__":
    main()
