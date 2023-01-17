from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class WebEnginePage(QWebEnginePage):
    def __init__(self, main_window, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)
        self.main_window = main_window

    def triggerAction(self, action: 'QWebEnginePage.WebAction', checked: bool = False) -> None:
        if action == QWebEnginePage.OpenLinkInNewWindow:
            self.parent.createWindow(QWebEnginePage.WebWindowType.WebBrowserTab)

        return super().triggerAction(action, checked)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass


class WebEngineView(QWebEngineView):
    def __init__(self, main_window, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.main_window = main_window

        self.loadProgress.connect(self.load_started)
        self.loadFinished.connect(self.load_finished)
        self.urlChanged.connect(lambda qurl: self.main_window.top_bar.nav_bar.url_bar.update_url(qurl, self))
        
        self.setPage(WebEnginePage(self.main_window))
    
    def createWindow(self, window_type: QWebEnginePage.WebWindowType) -> 'QWebEngineView':
        if window_type == QWebEnginePage.WebWindowType.WebBrowserTab:
            return self.main_window.tab_widgets.widget(self.main_window.top_bar.tab_bar.tabs.new_web_view_tab())
        elif window_type == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab:
            return self.main_window.tab_widgets.widget(self.main_window.top_bar.tab_bar.tabs.new_web_view_tab(background = True))
        
        return super().createWindow(window_type)
    
    def load_started(self):
        self.main_window.top_bar.nav_bar.reload_and_stop_button.setText("9")
        self.main_window.top_bar.nav_bar.reload_and_stop_button.clicked.connect(lambda: self.tab_widgets.currentWidget().stop())
    
    def load_finished(self):
        tab_index = self.main_window.tab_widgets.indexOf(self)
        
        self.main_window.top_bar.nav_bar.reload_and_stop_button.setText("Z")
        self.main_window.top_bar.nav_bar.reload_and_stop_button.clicked.connect(lambda: self.tab_widgets.currentWidget().reload())
        
        title = self.page().title()
        icon = self.page().icon()
        self.main_window.top_bar.tab_bar.tabs.setTabText(tab_index, title)
        self.main_window.top_bar.tab_bar.tabs.setTabIcon(tab_index, icon)