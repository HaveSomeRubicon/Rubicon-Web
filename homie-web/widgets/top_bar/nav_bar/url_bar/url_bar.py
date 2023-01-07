from PyQt5.QtWidgets import QLineEdit, QSizePolicy


class UrlBar(QLineEdit):
    def __init__(self, main_window, *args, **kwargs):
        super(UrlBar, self).__init__(*args, **kwargs)
        
        self.main_window = main_window
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setPlaceholderText("Search or type a URL")