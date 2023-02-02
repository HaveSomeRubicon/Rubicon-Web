from PyQt5.QtWidgets import QWidget

from widgets.top_bar.tab_bar.window_management_buttons.Ui_window_management_buttons import Ui_window_management_buttons


class WindowManagementButtons(QWidget, Ui_window_management_buttons):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)