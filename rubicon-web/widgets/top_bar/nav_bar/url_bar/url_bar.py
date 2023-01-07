import os
import urllib.parse
import validators

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
        
        self.selected = False

        self.returnPressed.connect(self.change_url)
    
    def update_url(self, qurl: QUrl, browser: WebEngineView or QWebEngineView):
        if browser == self.main_window.tab_widgets.currentWidget():
            self.setText(qurl.toString())
            self.setCursorPosition(0)
    
    def change_url(self):
        url = self.text().strip()
        
        if validators.url(QUrl.fromUserInput(url).toString()):
            qurl = QUrl.fromUserInput(url)
        elif os.path.exists(url):
            qurl = QUrl.fromLocalFile(url)
        else:
            qurl = QUrl(f"https://www.ecosia.org/search?q={urllib.parse.quote(url)}")
        
        self.main_window.tab_widgets.currentWidget().setFocus(True)
        self.main_window.tab_widgets.currentWidget().setUrl(qurl)

    def selectAll(self) -> None:
        self.selected = True
        return super().selectAll()
    
    def deselect(self) -> None:
        self.selected = False
        return super().deselect()
    
    def mousePressEvent(self, event) -> None:
        super(UrlBar, self).mousePressEvent(event)
        if self.selected == False:
            self.selectAll()
    
    def focusOutEvent(self, event) -> None:
        super(UrlBar, self).focusOutEvent(event)
        self.deselect()