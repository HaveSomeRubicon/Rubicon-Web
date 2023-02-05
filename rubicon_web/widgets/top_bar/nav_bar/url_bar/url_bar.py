import os
import urllib.parse
import validators

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QLineEdit, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView

from widgets.web_engine.web_engine import WebEngineView


class UrlBar(QLineEdit):
    def __init__(self, parent, main_window, *args, **kwargs):
        super(UrlBar, self).__init__(parent=parent, *args, **kwargs)
        self.parent().parent().parent().log("UrlBar is being initialized", "NOTICE", "url_bar.py")
        
        self.main_window = main_window
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setPlaceholderText("Search or type a URL")
        
        self.selected = False

        self.returnPressed.connect(self.change_url)
        self.parent().parent().parent().log("UrlBar has been initialized", "SUCCESS", "url_bar.py")
    
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
            qurl = QUrl(self.main_window.CONFIG["search_url"].replace("%s", url))
        
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