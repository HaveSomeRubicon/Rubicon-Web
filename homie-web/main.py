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


class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Homie Web Test')
        self.setWindowIcon(QIcon("assets/png/Homie Web Logo.png"))

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

        # Add back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_button)

        # Add forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_button)

        # Add reload button
        self.reload_stop_button = QAction('Reload', self)
        self.reload_stop_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(self.reload_stop_button)

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

        # Open new tab on start
        self.new_tab()
        
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
        
        # Set reload/stop button to stop when loading the page start
        def load_started():
            self.reload_stop_button.setText("Stop")
            self.reload_stop_button.triggered.connect(lambda: self.tabs.currentWidget().stop())
        browser.loadStarted.connect(load_started)
        
        # A function stored in a class which runs when web page finishes loading
        class LoadFinishedFunction:
            def __init__(self2):
                self2.tab_is_new = True
        
            def load_finished(self2, i=tab_index, browser=browser):
                # Shorten tab title if its too long then set the tab title
                if len(browser.page().title()) >= 15:
                    title = f"{browser.page().title()[:12]}..."
                else:
                    title = browser.page().title()
                self.tabs.setTabText(tab_index, title)
                # Set tab icon
                self.tabs.setTabIcon(tab_index, browser.page().icon())
                # Set reload/stop button to reload
                self.reload_stop_button.setText("Reload") 
                self.reload_stop_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
                # Select all url bar text if tab is new
                if self2.tab_is_new:
                    self.url_bar.selectAll()
                    self.url_bar.setFocus()
                    self2.tab_is_new = False
        load_finished_func = LoadFinishedFunction()
        browser.loadFinished.connect(lambda: load_finished_func.load_finished())

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
    
    def update_url_bar(self, qurl, browser=None):
        # Check if signal is from the current tab
        if not browser == self.tabs.currentWidget():
            return

        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Homie Web")

window = MainWindow()
window.show()

app.exec()