from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize

from widgets.top_bar.nav_bar.url_bar.url_bar import UrlBar


class NavBar(QWidget):
    def __init__(self, parent, *args, **kwargs):
        """Initializes the navigation bar"""
        super(NavBar, self).__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent()
        self.main_window.log("NavBar is being initialized", "OKAY", "nav_bar.py")
        
        self.setObjectName("nav_bar")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.setStyleSheet("""QWidget {
    border: 0px;
    background-color: rgb(21, 21, 21);
}
QPushButton {
    background-color: rgba(0, 0, 0, 0);
    color: /nav_bar_accent_color/;
    border: 0px;
    font: 24px \"dripicons-v2\";
    margin: 2px;
    padding: 2px;
}
QPushButton:hover {
    background-color: /nav_bar_hover_color/;
    border-radius: 10px;
}
QPushButton:pressed {
    padding-top: 4px;
    padding-left: 4px;
}
QLineEdit {
    background-color: /url_bar_bg_color/;
    border-radius: 13px;
    color: rgb(255, 255, 255);
    padding-left: 8px;
    padding-bottom: 2px;
    margin-top: 3px;
    margin-bottom: 3px;
    margin-left: 1px;
    margin-right: 1px;
    border: 2px solid /nav_bar_accent_color/;
}
QLineEdit:hover {
    background-color: /nav_bar_hover_color/;
}
QLineEdit:focus {
    background-color: /nav_bar_focus_color/;
}""")

        self.nav_bar_layout = QHBoxLayout(self)
        self.nav_bar_layout.setObjectName("nav_bar_layout")
        self.nav_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_bar_layout.setSpacing(0)
        
        self.back_button = QPushButton(self)
        self.back_button.setObjectName("back_button")
        self.back_button.setText("l")
        self.back_button.clicked.connect(
            lambda: self.main_window.tab_widgets.currentWidget().back()
        )
        self.nav_bar_layout.addWidget(self.back_button)
        
        self.forward_button = QPushButton(self)
        self.forward_button.setObjectName("forward_button")
        self.forward_button.setText("m")
        self.forward_button.clicked.connect(
            lambda: self.main_window.tab_widgets.currentWidget().forward()
        )
        self.nav_bar_layout.addWidget(self.forward_button)

        self.reload_and_stop_button = QPushButton(self)
        self.reload_and_stop_button.setObjectName("reload_and_stop_button")
        self.reload_and_stop_button.setText("Z")
        self.nav_bar_layout.addWidget(self.reload_and_stop_button)

        self.url_bar = UrlBar(self)
        self.nav_bar_layout.insertWidget(3, self.url_bar)

        self.new_tab_button = QPushButton(self)
        self.new_tab_button.setObjectName("new_tab_button")
        self.new_tab_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.new_tab_button.setText("")
        self.nav_bar_layout.addWidget(self.new_tab_button)

        self.main_window.log(
            "NavBar has been initialized", "SUCCESS", "nav_bar.py"
        )
