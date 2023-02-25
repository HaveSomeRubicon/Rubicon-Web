import os
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QTabBar, QSizePolicy
from PyQt5.QtGui import QIcon

from ....web_engine.web_engine import WebEngineView


class Tabs(QTabBar):
    def __init__(self, parent, *args, **kwargs):
        """Initializes the tabs"""
        super(Tabs, self).__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent().parent()

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.tab_widgets = self.main_window.tab_widgets

        self.default_tab = lambda: self.new_web_view_tab(self.main_window.DEFAULT_QURL)

        if self.main_window.get_configuration()["reopen_last_session"] and os.path.exists(self.main_window.LAST_SESSION_PATH):
            with open(self.main_window.LAST_SESSION_PATH, "r") as last_session_file:
                LAST_SESSION = eval(last_session_file.read())
                for url in LAST_SESSION["last_open_urls"]:
                    BACKGROUND = (False if LAST_SESSION["last_open_urls"].index(url) == 0 else True)
                    self.new_web_view_tab(QUrl(url), BACKGROUND)
            self.setCurrentIndex(LAST_SESSION["last_open_tab_index"])
            self.update_url(LAST_SESSION["last_open_tab_index"])
        else:
            self.default_tab()

        self.setDrawBase(False)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.update_url)
        self.tabMoved.connect(self.tab_moved)

    def update_url(self, tab_index):
        """This function updates the URL bar when the current tab is changed"""
        self.tab_widgets.setCurrentIndex(tab_index)
        if not self.main_window.tab_widgets.count() < 1:
            current_web_view = self.tab_widgets.currentWidget()
            self.parent().parent().nav_bar.url_bar.update_url(
                current_web_view.url(), current_web_view
            )

    def tab_moved(self, to, _from):
        """Reorders widgets in the stacked widget containing all the web views when the order of the tabs is changed"""
        MOVED_TAB_WIDGET = self.tab_widgets.widget(_from)
        self.tab_widgets.removeWidget(MOVED_TAB_WIDGET)
        self.tab_widgets.insertWidget(to, MOVED_TAB_WIDGET)

    def new_web_view_tab(self, qurl: QUrl = None, background: bool = False):
        """Creates a new tab containing a web view"""
        browser = WebEngineView(self.main_window.tab_widgets)
        if qurl != None:
            browser.setUrl(qurl)
        TAB_INDEX = self.addTab("Loading...")
        self.tab_widgets.addWidget(browser)

        if not background:
            self.setCurrentIndex(TAB_INDEX)
            self.update_url(TAB_INDEX)

        self.tab_widgets.widget(TAB_INDEX).setAttribute(Qt.WA_DeleteOnClose, True)

        return TAB_INDEX

    def close_tab(self, tab_index):
        """Closes a tab and quits Rubicon Web if theres no more tabs left"""
        if self.count() <= 1:
            # TODO: Open a dialog to ask the user if they want to close entire web browser when all tabs are closed
            sys.exit()
        else:
            browser = self.tab_widgets.widget(tab_index)
            browser.close()
            self.tab_widgets.removeWidget(self.tab_widgets.widget(tab_index))
            self.removeTab(tab_index)
