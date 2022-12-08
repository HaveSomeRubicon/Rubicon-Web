import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi

from widgets.mainwindow.mainwindow import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()