from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None, *args, **kwargs):
        super(WebEnginePage, self).__init__(parent, *args, **kwargs)
        
        self.parent = parent

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
        
        self.setPage(WebEnginePage(self))
    
    def createWindow(self, window_type: QWebEnginePage.WebWindowType) -> 'QWebEngineView':
        if window_type == QWebEnginePage.WebWindowType.WebBrowserTab:
            return self.main_window.tab_widgets.widget(self.main_window.top_bar.tab_bar.tabs.new_web_view_tab())
        elif window_type == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab:
            return self.main_window.tab_widgets.widget(self.main_window.top_bar.tab_bar.tabs.new_web_view_tab(background = True))
        
        return super().createWindow(window_type)