import sys

from PyQt5.QtWidgets import QApplication

from config import config
from widgets.mainwindow.mainwindow import MainWindow


app = QApplication(sys.argv)

window = MainWindow(config)
window.show()

app.exec()