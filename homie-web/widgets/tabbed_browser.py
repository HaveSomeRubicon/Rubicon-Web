import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QTabWidget

from widgets.web_engine import WebEngineView


class TabbedBrowser(QTabWidget):
    def __init__(self, main_window):
        super(TabbedBrowser, self).__init__()
        self.main_window = main_window
        
        self.setTabPosition(QTabWidget.North)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.close_current_tab)

        self.new_tabs = []

    def new_tab(self, qurl: QUrl = QUrl('https://ecosia.org/'), title: str = 'Loading...') -> WebEngineView:
        """
        Creates and adds a new tab to the tabs widget
        """
        # Create QWebEngineView
        browser = WebEngineView(self, self.main_window)
        browser.setAttribute(Qt.WA_DeleteOnClose, True)
        browser.setUrl(qurl)
        self.new_tabs.append(browser)
        
        # Create tab with browser widget and switch to it
        tab_index = self.addTab(browser, title)
        self.setCurrentIndex(tab_index)

        # Update url bar when url is changed
        browser.urlChanged.connect( lambda qurl, browser=browser:
            self.main_window.navbar.update_url_bar(qurl, browser) )
        
        # Update progress bar when browser loading progress changes
        browser.loadProgress.connect(self.main_window.load_progress_bar.update_progress_bar)
        
        # Set reload/stop button to stop when loading the page start
        browser.loadStarted.connect(self.tab_loading_started)
        
        # A function stored in a class which runs when web page finishes loading
        browser.loadFinished.connect(lambda: self.tab_loading_finished(tab_index, browser))

        # Return WebEngineView object
        return browser

    def tab_loading_started(self):
        self.main_window.navbar.reload_stop_button.setText("Stop")
        self.main_window.navbar.reload_stop_button.triggered.connect(lambda: self.currentWidget().stop())

    def tab_loading_finished(self, tab_index, browser):
        # Shorten tab title if its too long then set the tab title
        if len(browser.page().title()) >= 25:
            title = f"{browser.page().title()[:22]}..."
        else:
            title = browser.page().title()
        self.setTabText(tab_index, title)
        
        # Set tab icon
        self.setTabIcon(tab_index, browser.page().icon())
        
        # Set reload/stop button to reload
        self.main_window.navbar.reload_stop_button.setText("Reload") 
        self.main_window.navbar.reload_stop_button.triggered.connect(lambda: self.currentWidget().reload())
        
        # Select all url bar text if tab is new
        if browser in self.new_tabs:
            self.main_window.navbar.url_bar.selectAll()
            self.main_window.navbar.url_bar.setFocus()
            self.new_tabs.remove(browser)

    def close_current_tab(self, tab_index):
        if self.count() <= 1:
            print('MAHDI ADD self.main_window CLOSE CONFIRMATION TO close_current_tab FUNC WHEN THERES ONLY 1 TAB LEFT')
            sys.exit()
        else:
            browser = self.widget(tab_index)
            browser.close()
            self.removeTab(tab_index)