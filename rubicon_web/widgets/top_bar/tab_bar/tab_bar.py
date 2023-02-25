from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from widgets.top_bar.tab_bar.Ui_tab_bar import Ui_tab_bar
from widgets.top_bar.tab_bar.tabs.tabs import Tabs
from widgets.top_bar.tab_bar.window_management_buttons.window_management_buttons import WindowManagementButtons


class TabBar(QWidget, Ui_tab_bar):
    def __init__(self, parent, *args, **kwargs):
        super(TabBar, self).__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent()
        self.main_window.log("TabBar is being initialized", "OKAY", "tab_bar.py")
        self.setupUi(self)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.tabs = Tabs(self)
        self.tab_bar_layout.addWidget(self.tabs)

        if self.main_window.get_configuration()["show_window_management_buttons"]:
            self.window_management_buttons = WindowManagementButtons(self)
            self.tab_bar_layout.addWidget(self.window_management_buttons)
        self.main_window.log("TabBar has been initialized", "SUCCESS", "tab_bar.py")
