import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QTabBar, QSizePolicy
from PyQt5.QtGui import QIcon

from ....web_engine.web_engine import WebEngineView


class Tabs(QTabBar):
    def __init__(self, main_window, *args, **kwargs):
        super(Tabs, self).__init__(*args, **kwargs)
        
        self.main_window = main_window
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.tab_widgets = self.main_window.tab_widgets
        
        self.setDrawBase(False)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)
        self.tabMoved.connect(self.tab_moved)

    def tab_changed(self, tab_index):
        self.tab_widgets.setCurrentIndex(tab_index)
    
    def tab_moved(self, to, _from):
        moved_tab_widget = self.tab_widgets.widget(_from)
        self.tab_widgets.removeWidget(moved_tab_widget)
        self.tab_widgets.insertWidget(to, moved_tab_widget)

    def new_tab(self, widget, title: str = "Untitled tab", url_bar_text: str = None, icon: QIcon = None, background: bool = True):
        if icon is not None:
            tab_index = self.addTab(icon, title)
        else:
            tab_index = self.addTab(title)
        self.tab_widgets.addWidget(widget)
        
        if not background:
            self.setCurrentIndex(tab_index)
        
        self.tab_widgets.widget(tab_index).setAttribute(Qt.WA_DeleteOnClose, True)
        
        if not url_bar_text == None:
            self.mainwindow.top_bar.nav_bar.url_bar.update_text(url_bar_text)
        
        return tab_index

    def new_web_view_tab(self, qurl: QUrl = None, background: bool = False):
        browser = WebEngineView(self.main_window)
        if qurl != None:
            browser.setUrl(qurl)
        tab_index = self.new_tab(browser, "Loading...", background = background)
        
        def browser_load_started():
            self.main_window.top_bar.nav_bar.reload_and_stop_button.setText("9")
            self.main_window.top_bar.nav_bar.reload_and_stop_button.clicked.connect(lambda: self.tab_widgets.currentWidget().stop())
        
        def browser_load_finished():
            self.main_window.top_bar.nav_bar.reload_and_stop_button.setText("Z")
            self.main_window.top_bar.nav_bar.reload_and_stop_button.clicked.connect(lambda: self.tab_widgets.currentWidget().reload())
            
            title = browser.page().title()
            icon = browser.page().icon()
            self.setTabText(tab_index, title)
            self.setTabIcon(tab_index, icon)
        
        browser.loadProgress.connect(browser_load_started)
        browser.loadFinished.connect(browser_load_finished)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.main_window.top_bar.nav_bar.url_bar.update_url(qurl, browser))
        
        return tab_index
    
    def close_tab(self, tab_index):
        if self.count() <= 1:
            # TODO: Open a dialog to ask the user if they want to close entire web browser when all tabs are closed
            sys.exit()
        else:
            browser = self.tab_widgets.widget(tab_index)
            browser.close()
            self.tab_widgets.removeWidget(self.tab_widgets.widget(tab_index))
            self.removeTab(tab_index)