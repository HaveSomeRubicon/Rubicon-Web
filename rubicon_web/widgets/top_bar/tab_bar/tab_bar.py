from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt

from widgets.top_bar.tab_bar.tabs.tabs import Tabs
from widgets.top_bar.tab_bar.window_management_buttons.window_management_buttons import WindowManagementButtons


class TabBar(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(TabBar, self).__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent()
        self.main_window.log("TabBar is being initialized", "OKAY", "tab_bar.py")

        self.setObjectName("tab_bar")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.setStyleSheet("""QWidget {
    background-color: /tab_bar_bg_color/;
}
QTabBar {
    background: /tab_bar_bg_color/;
    border: 0px;	
    color: white;
}
QTabBar::tab {
    background: /tab_bg_color/;
    border: 2px solid /tab_bar_accent_color/;
    border-radius: 6px;
    padding: 4px;
    margin: 2px;
    color: /tab_font_color/;
}
QTabBar::tab:hover {
    background-color: /tab_hover_color/;
}
QTabBar::tab:selected {
    background: /tab_focus_color/;
}
QTabBar::close-button {
    image: url(*widgets/top_bar/tab_bar/tabs/svg/close tab button icon.svg*);
}""")

        self.tab_bar_layout = QHBoxLayout(self)
        self.tab_bar_layout.setObjectName("tab_bar_layout")
        self.tab_bar_layout.setContentsMargins(2, 4, 2, 2)
        self.tab_bar_layout.setSpacing(0)

        self.tabs = Tabs(self)
        self.tab_bar_layout.addWidget(self.tabs)

        if self.main_window.get_configuration()["show_window_management_buttons"]:
            self.window_management_buttons = WindowManagementButtons(self)
            self.tab_bar_layout.addWidget(self.window_management_buttons)
        
        self.main_window.log("TabBar has been initialized", "SUCCESS", "tab_bar.py")
