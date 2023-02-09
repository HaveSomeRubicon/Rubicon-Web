from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from widgets.top_bar.tab_bar.Ui_tab_bar import Ui_tab_bar
from widgets.top_bar.tab_bar.tabs.tabs import Tabs
from widgets.top_bar.tab_bar.window_management_buttons.window_management_buttons import WindowManagementButtons


class TabBar(QWidget, Ui_tab_bar):
    def __init__(self, parent, main_window, *args, **kwargs):
        super(TabBar, self).__init__(parent=parent, *args, **kwargs)
        self.parent().parent().log("TabBar is being initialized", "OKAY", "tab_bar.py")
        self.setupUi(self)
        
        self.main_window = main_window

        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.tabs = Tabs(self, self.main_window)
        self.tab_bar_layout.addWidget(self.tabs)
        
        if self.main_window.CONFIG["show_window_management_buttons"]:
            self.window_management_buttons = WindowManagementButtons(self)
            self.tab_bar_layout.addWidget(self.window_management_buttons)
        self.parent().parent().log("TabBar has been initialized", "SUCCESS", "tab_bar.py")