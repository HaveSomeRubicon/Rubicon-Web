#! /bin/env python3
import sys
import validators
from urllib.parse import quote_plus

from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QFocusEvent, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QTabWidget,
    QAction,
    QLineEdit,
    QWidget,
    QGridLayout,
    QProgressBar
)


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None, *args, **kwargs):
        super(WebEnginePage, self).__init__(parent, *args, **kwargs)
        
        self.parent = parent

    def triggerAction(self, action: 'QWebEnginePage.WebAction', checked: bool = False) -> None:
        if action == QWebEnginePage.OpenLinkInNewWindow:
            self.parent.createWindow(QWebEnginePage.WebWindowType.WebBrowserTab)

        return super().triggerAction(action, checked)


class WebEngineView(QWebEngineView):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.setPage(WebEnginePage(self))
    
    def createWindow(self, window_type: QWebEnginePage.WebWindowType) -> 'QWebEngineView':
        if window_type == QWebEnginePage.WebWindowType.WebBrowserTab:
            return window.new_tab()
        return super().createWindow(type)


class UrlBar(QLineEdit):
    def __init__(self, parent=None):
        super(UrlBar, self).__init__(parent)
        self.focused = False

    def mousePressEvent(self, event, parent=None) -> None:
        super(UrlBar, self).mousePressEvent(event)
        if not self.focused:
            self.selectAll()
            self.focused = True
    
    def focusOutEvent(self, event) -> None:
        super(UrlBar, self).focusOutEvent(event)
        self.deselect()
        self.focused = False
    
    def setFocus(self):
        super(UrlBar, self).setFocus()
        if not self.focused:
            self.selectAll()
            self.focused = True


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Homie Web Test')

        # Create a toolbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Create layout
        main_layout = QGridLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0,0,0,0)

        # Create tabs widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        main_layout.addWidget(self.tabs)

        # Add close tab button to every tab 
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # Open new tab on start
        self.new_tab()
        
        # Add back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_button)

        # Add forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_button)

        # Add reload button
        reload_button = QAction('Reload', self)
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_button)

        # Add home button
        home_button = QAction('Home', self)
        home_button.triggered.connect(lambda: self.tabs.currentWidget().home())
        navbar.addAction(home_button)

        # Add url bar
        self.url_bar = UrlBar()
        self.url_bar.returnPressed.connect(self.set_url)
        navbar.addWidget(self.url_bar)

        # Add a new tab button to the toolbar
        new_tab_button = QAction('+', self)
        new_tab_button.triggered.connect(lambda: self.new_tab())
        navbar.addAction(new_tab_button)

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Set the tabs widget as central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def new_tab(self, qurl: QUrl = QUrl('https://ecosia.org/'), title: str = 'Loading...') -> WebEngineView:
        """
        Creates and adds a new tab to the tabs widget
        """
        # Create QWebEngineView
        browser = WebEngineView(self.tabs)
        browser.setAttribute(Qt.WA_DeleteOnClose, True)
        browser.setUrl(qurl)
        
        # Create tab with browser widget and switch to it
        tab_index = self.tabs.addTab(browser, title)
        self.tabs.setCurrentIndex(tab_index)

        # Update url bar when url is changed
        browser.urlChanged.connect( lambda qurl, browser=browser:
            self.update_url_bar(qurl, browser) )
        
        def update_progress_bar(progress: int):
            self.progress_bar.setValue(progress)
            if progress == 100:
                self.progress_bar.hide()
            else:
                self.progress_bar.show()
        browser.loadProgress.connect(update_progress_bar)
        
        # Set tab title and icon when page finishes loading
        def load_finished(_, i=tab_index, browser=browser):
            # Shorten tab title if its too long then set the tab title
            if len(browser.page().title()) >= 15:
                title = f"{browser.page().title()[:12]}..."
            else:
                title = browser.page().title()
            self.tabs.setTabText(tab_index, title)
            # Set tab icon
            self.tabs.setTabIcon(tab_index, browser.page().icon())
            # Focus url bar
            self.url_bar.setFocus()
        browser.loadFinished.connect(load_finished)


        # Return WebEngineView object
        return browser

    def close_current_tab(self, tab_index):
        if self.tabs.count() <= 1:
            print('MAHDI ADD WINDOW CLOSE CONFIRMATION TO close_current_tab FUNC WHEN THERES ONLY 1 TAB LEFT')
            sys.exit()
        else:
            browser = self.tabs.widget(tab_index)
            browser.close()
            self.tabs.removeTab(tab_index)
            # browser.setUrl(QUrl('about:blank'))
            # def load_finished():
            #     self.tabs.removeTab(tab_index)
            # browser.loadFinished.connect(load_finished)

    def set_url(self):
        url_bar_text = self.url_bar.text()

        qurl = QUrl(url_bar_text)
        qurl.setScheme("http")
        qurl = QUrl(qurl.toString().replace("http:", "http://", 1))
        
        # Search for url bar text if the url bar text isn't a valid url
        if validators.url(qurl.toString()) != True:
            search_query = url_bar_text
            search_query = quote_plus(search_query)
            search_query.replace(':', '%3A')
            search_query = f"https://www.ecosia.org/search?q={search_query}"
            qurl = QUrl(search_query)

        # Set current tab web engine's qurl to the new qurl
        self.tabs.currentWidget().setUrl(qurl)
        self.tabs.currentWidget().setFocus()

            
    # def set_url1(self):
    #     url_bar_text = self.url_bar.text()
        
    #     # Get QUrl from url bar
    #     qurl = QUrl(url_bar_text)
        
    #     # Set qurl_http to QUrl from url bar text with the scheme set as http
    #     qurl_http = QUrl(url_bar_text)
    #     qurl_http.setScheme('http')
        
    #     # Set qurl_http to the string version of qurl_http
    #     qurl_http_string = qurl_http.toString()

    #     # Add the 2 slashes after the colon in http: or https: if they arent there
    #     if not qurl_http_string.startswith('https://') or not qurl_http_string.startswith('http://'):
    #         if qurl_http_string.startswith('http:') or qurl_http_string.startswith('https:'):
    #             qurl_http_string = qurl_http_string.replace(':', '://', 1)
        
    #     # Update qurl_http to include the fixes made to qurl_http_string
    #     qurl_http = QUrl(qurl_http_string)

    #     # Set scheme to http if no scheme was given
    #     if qurl.scheme() == "":
    #         # Set qurl scheme to http if it works
    #         if validators.url(qurl_http_string) == True:
    #             qurl.setScheme('http')
    #         else:
    #             # Search for url bar text in Ecosia if the text in url bar isnt a valid url
    #             if validators.url(qurl_http_string) != True:
    #                 # Convert url bar text to safe characters
    #                 safe_query = url_bar_text
    #                 safe_query = quote_plus(safe_query)
    #                 safe_query.replace(':', '%3A')
    #                 # Put search query in search url
    #                 search_url = f"https://www.ecosia.org/search?q={safe_query}"
    #                 qurl = QUrl(search_url)

    #     # Set current tabs page to the qurl
    #     self.tabs.currentWidget().setUrl(qurl)
    
    def update_url_bar(self, qurl, browser=None):
        # Check if signal is from the current tab
        if not browser == self.tabs.currentWidget():
            return

        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Homie Web")
app.setWindowIcon(QIcon("images/png/Homie Web Logo.png"))

window = MainWindow()
window.show()

app.exec()