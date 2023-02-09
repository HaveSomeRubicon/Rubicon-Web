from PyQt5.QtWidgets import QWidget

from widgets.top_bar.tab_bar.window_management_buttons.Ui_window_management_buttons import (
    Ui_window_management_buttons,
)


class WindowManagementButtons(QWidget, Ui_window_management_buttons):
    def __init__(self, parent, *args, **kwargs):
        """Initializes the window management buttons"""
        super(QWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parent().parent().parent().log(
            "WindowManagementButtons are being initialized",
            "OKAY",
            "window_management_buttons.py",
        )
        self.setupUi(self)
        self.parent().parent().parent().log(
            "WindowManagementButtons have been initialized",
            "OKAY",
            "window_management_buttons.py",
        )
