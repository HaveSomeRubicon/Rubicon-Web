import sys

from PyQt5.QtWidgets import QApplication

from widgets.mainwindow.mainwindow import MainWindow
from utils.configutils import get_config


app = QApplication(sys.argv)

window = MainWindow(get_config())
window.show()

app.exec()