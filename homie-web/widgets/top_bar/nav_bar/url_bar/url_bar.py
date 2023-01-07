from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QLineEdit, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView

from widgets.web_engine.web_engine import WebEngineView


class UrlBar(QLineEdit):
    def __init__(self, main_window, *args, **kwargs):
        super(UrlBar, self).__init__(*args, **kwargs)
        
        self.main_window = main_window
        
        self.focused = False
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setPlaceholderText("Search or type a URL")
    
    def update_text(self, text):
        self.setText(text)
    
    def update_url(self, qurl: QUrl, browser: WebEngineView or QWebEngineView):
        if browser == self.main_window.tab_widgets.widget(self.main_window.top_bar.tab_bar.tabs.currentIndex()):
            self.update_text(qurl.toString())
    
    def mousePressEvent(self, event) -> None:
        super(UrlBar, self).mousePressEvent(event)
        print("MousePressEvent" + str(self.focused))
        if self.focused == False:
            self.selectAll()
            self.focused = True
    
    def focusOutEvent(self, event) -> None:
        super(UrlBar, self).focusOutEvent(event)
        print("FocusOutEvent" + str(self.focused))
        self.focused = False