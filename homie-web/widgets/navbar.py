import validators
from urllib.parse import quote_plus

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QLineEdit, QToolBar, QAction


class UrlBar(QLineEdit):
    def __init__(self, parent=None):
        super(UrlBar, self).__init__(parent)

        self.focused = False

        #self.textChanged.connect(textChanged)

    def selectAll(self):
        super(UrlBar, self).selectAll()
        if not self.focused:
            self.focused = True

    def deselect(self):
        super(UrlBar, self).deselect()
        if self.focused:
            self.focused = False
    
    def mousePressEvent(self, event, parent=None) -> None:
        super(UrlBar, self).mousePressEvent(event)
        if not self.focused:
            self.selectAll()
    
    def focusOutEvent(self, event) -> None:
        super(UrlBar, self).focusOutEvent(event)
        if self.focused:
            self.deselect()

    def text_changed(self, text):
        self.setText(text.replace(' ', '+'))


class NavBar(QToolBar):
    def __init__(self, main_window, parent=None):
        super(NavBar, self).__init__(parent)
        self.main_window = main_window

        # Add back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(lambda: self.main_window.tabbed_browser.currentWidget().back())
        self.addAction(back_button)

        # Add forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(lambda: self.main_window.tabbed_browser.currentWidget().forward())
        self.addAction(forward_button)

        # Add reload button
        self.reload_stop_button = QAction('Reload', self)
        self.reload_stop_button.triggered.connect(lambda: self.main_window.tabbed_browser.currentWidget().reload())
        self.addAction(self.reload_stop_button)

        # Add home button
        home_button = QAction('Home', self)
        home_button.triggered.connect(lambda: self.set_url())
        self.addAction(home_button)

        # Add url bar
        self.url_bar = UrlBar()
        self.url_bar.returnPressed.connect(self.set_url)
        self.addWidget(self.url_bar)

        # Add a new tab button to the toolbar
        new_tab_button = QAction('+', self)
        new_tab_button.triggered.connect(lambda: self.main_window.tabbed_browser.new_tab())
        self.addAction(new_tab_button)
    
    def update_url_bar(self, qurl, browser=None):
        # Check if signal is from the current tab
        if not browser == self.main_window.tabbed_browser.currentWidget():
            return

        # Update the url bar
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)
    
    def set_url(self):
        # Get url bar text
        url_bar_text = self.url_bar.text()
        print(f"Url bar text: {url_bar_text}")

        # Convert url bar text to QUrl with scheme set too http
        qurl = QUrl(url_bar_text)
        print(f"qurl: {qurl}")
        qurl.setScheme("http")
        print(f"qurl http scheme: {qurl}")
        if not qurl.toString().startswith("http://") or not qurl.toString().startswith("https://"):
            if qurl.toString().startswith("http:") and qurl.toString().startswith("https:"):
                qurl = QUrl(qurl.toString().replace("http:", "http://", 1))
        print(f"qurl http: -> https:// : {qurl}")
        
        # Search for url bar text with Ecosia if the url bar text isn't a valid url
        if validators.url(qurl.toString()) != True:
            search_query = url_bar_text
            print(f"search_query 1: {search_query}")
            search_query = quote_plus(search_query)
            print(f"search_query 2: {search_query}")
            search_query.replace(':', '%3A')
            print(f"search_query 3: {search_query}")
            search_query = f"https://www.ecosia.org/search?q={search_query}"
            print(f"search_query 4: {search_query}")
            qurl = QUrl(search_query)
            print(f"search_query qurl: {qurl}")

        # Set current tab web engine's qurl to the new qurl
        self.main_window.tabbed_browser.currentWidget().setUrl(qurl)
        
        # Focus tab web engine view
        self.main_window.tabbed_browser.currentWidget().setFocus()