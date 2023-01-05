from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class WindowManagementButtons(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        loadUi("homie-web/widgets/top_bar/tab_bar/window_management_buttons/window_management_buttons.ui", self)