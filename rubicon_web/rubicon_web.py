import sys

from PyQt5.QtWidgets import QApplication

from widgets.mainwindow.mainwindow import MainWindow
from utils.configutils import get_config
from utils.themeutils import get_theme


def main():
    app = QApplication(sys.argv)
    
    window = MainWindow(get_config(), get_theme())
    window.show()
    
    app.exec()


if __name__ == "__main__":
    main()