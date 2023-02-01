from PyQt5.QtWidgets import QWidget

from widgets.top_bar.tab_bar.window_management_buttons.Ui_window_management_buttons import Ui_window_management_buttons


class WindowManagementButtons(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        loadUi("rubicon_web/widgets/top_bar/tab_bar/window_management_buttons/window_management_buttons.ui", self)