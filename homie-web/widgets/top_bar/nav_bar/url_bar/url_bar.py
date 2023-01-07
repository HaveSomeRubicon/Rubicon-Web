from PyQt5.QtWidgets import QLineEdit, QSizePolicy


class UrlBar(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(UrlBar, self).__init__(*args, **kwargs)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setPlaceholderText("Search or type a URL")