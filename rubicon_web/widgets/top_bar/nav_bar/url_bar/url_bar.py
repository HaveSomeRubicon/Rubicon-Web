import os
import urllib.parse
import validators

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QLineEdit, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView

from widgets.web_engine.web_engine import WebEngineView


class UrlBar(QLineEdit):
    def __init__(self, parent, *args, **kwargs):
        """Initializes the URL bar"""
        super(UrlBar, self).__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent().parent()
        self.main_window.log(
            "UrlBar is being initialized", "OKAY", "url_bar.py"
        )

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setPlaceholderText("Search or type a URL")

        self.selected = False

        self.returnPressed.connect(self.change_url)
        self.main_window.log(
            "UrlBar has been initialized", "SUCCESS", "url_bar.py"
        )

    def update_url(self, qurl: QUrl, browser: WebEngineView or QWebEngineView):
        """Updates the current text in the URL bar"""
        if browser == self.main_window.tab_widgets.currentWidget():
            self.setText(qurl.toString())
            self.setCursorPosition(0)

    def change_url(self):
        """This function is called when the user hits return after typing in a URL or search query"""
        url = self.text().strip()

        if validators.url(QUrl.fromUserInput(url).toString()):
            qurl = QUrl.fromUserInput(url)
        elif os.path.exists(url):
            qurl = QUrl.fromLocalFile(url)
        else:
            qurl = QUrl(self.main_window.get_configuration()["search_url"].replace("%s", url))

        self.main_window.tab_widgets.currentWidget().setFocus(True)
        self.main_window.tab_widgets.currentWidget().setUrl(qurl)

    def selectAll(self) -> None:
        """Selects all the text in the URL bar"""
        self.selected = True
        return super().selectAll()

    def deselect(self) -> None:
        """Deselects all the text in the URL bar"""
        self.selected = False
        return super().deselect()

    def mousePressEvent(self, event) -> None:
        """Selects all text when the URL bar is clicked"""
        super(UrlBar, self).mousePressEvent(event)
        if self.selected == False:
            self.selectAll()

    def focusOutEvent(self, event) -> None:
        """Deselects all text when the URL bar loses focus"""
        super(UrlBar, self).focusOutEvent(event)
        self.deselect()
