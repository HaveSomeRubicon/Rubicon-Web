from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QLineEdit, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView

from widgets.web_engine.web_engine import WebEngineView


class UrlBar(QLineEdit):
    def __init__(self, main_window, *args, **kwargs):
        super(UrlBar, self).__init__(*args, **kwargs)
        
        self.main_window = main_window
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setPlaceholderText("Search or type a URL")
        
        self.focused = False

        self.returnPressed.connect(self.change_url)
    
    def update_url(self, qurl: QUrl, browser: WebEngineView or QWebEngineView):
        if browser == self.main_window.tab_widgets.currentWidget():
            self.setText(qurl.toString())
    
    def change_url(self):
        self.main_window.tab_widgets.currentWidget().setUrl(QUrl(self.text()))
    
    def mousePressEvent(self, event) -> None:
        super(UrlBar, self).mousePressEvent(event)
        if self.focused == False:
            self.selectAll()
            self.focused = True
    
    def focusOutEvent(self, event) -> None:
        super(UrlBar, self).focusOutEvent(event)
        self.focused = False