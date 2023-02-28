from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize


class WindowManagementButtons(QWidget):
    def __init__(self, parent, *args, **kwargs):
        """Initializes the window management buttons"""
        super(QWidget, self).__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent().parent()
        self.main_window.log("WindowManagementButtons are being initialized", "OKAY", "window_management_buttons.py")
        
        self.setObjectName("window_management_buttons")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        self.setStyleSheet("QWidget {\n"
"    border: 0px;\n"
"}")

        self.window_management_buttons_layout = QHBoxLayout(self)
        self.window_management_buttons_layout.setObjectName("window_management_buttons_layout")
        self.window_management_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.window_management_buttons_layout.setSpacing(0)
        
        self.maximize_button = QPushButton(self)
        self.maximize_button.setObjectName("mazimize_button")
        self.maximize_button.setText("")
        maximize_button_icon = QIcon()
        maximize_button_icon.addPixmap(QPixmap("png/maximize button icon.png"), QIcon.Normal, QIcon.Off)
        self.maximize_button.setIcon(maximize_button_icon)
        self.maximize_button.setIconSize(QSize(23, 23))
        self.window_management_buttons_layout.addWidget(self.maximize_button)
        
        self.minimize_button = QPushButton(self)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setText("")
        minimize_button_icon = QIcon()
        minimize_button_icon.addPixmap(QPixmap("png/minimize button icon.png"), QIcon.Normal, QIcon.Off)
        self.minimize_button.setIcon(minimize_button_icon)
        self.minimize_button.setIconSize(QSize(23, 23))
        self.window_management_buttons_layout.addWidget(self.minimize_button)
        
        self.close_button = QPushButton(self)
        self.close_button.setObjectName("close_button")
        self.close_button.setText("")
        close_button_icon = QIcon()
        close_button_icon.addPixmap(QPixmap("png/close button icon.png"), QIcon.Normal, QIcon.Off)
        self.close_button.setIcon(close_button_icon)
        self.close_button.setIconSize(QSize(23, 23))
        self.window_management_buttons_layout.addWidget(self.close_button)
        
        self.main_window.log("WindowManagementButtons have been initialized", "OKAY", "window_management_buttons.py")
