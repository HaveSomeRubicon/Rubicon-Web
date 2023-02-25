from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent, *args, **kwargs):
        super(WebEnginePage, self).__init__(parent=parent, *args, **kwargs)

    def triggerAction(
        self, action: "QWebEnginePage.WebAction", checked: bool = False
    ) -> None:
        if action == QWebEnginePage.OpenLinkInNewWindow:
            self.parent.createWindow(QWebEnginePage.WebWindowType.WebBrowserTab)

        return super().triggerAction(action, checked)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass


class WebEngineView(QWebEngineView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.main_window = self.parent().parent().parent().parent()

        self.loadProgress.connect(self.load_started)
        self.loadFinished.connect(self.load_finished)
        self.urlChanged.connect(self.url_changed)

        self.setPage(WebEnginePage(self))

    def createWindow(
        self, window_type: QWebEnginePage.WebWindowType
    ) -> "QWebEngineView":
        if window_type == QWebEnginePage.WebWindowType.WebBrowserTab:
            return self.parent().widget(
                self.main_window.top_bar.tab_bar.tabs.new_web_view_tab()
            )
        elif window_type == QWebEnginePage.WebWindowType.WebBrowserBackgroundTab:
            return self.parent().widget(
                self.main_window.top_bar.tab_bar.tabs.new_web_view_tab(background=True)
            )

        return super().createWindow(window_type)

    def load_started(self):
        if self == self.parent().currentWidget():
            self.main_window.top_bar.nav_bar.reload_and_stop_button.setText("9")
            self.main_window.top_bar.nav_bar.reload_and_stop_button.clicked.connect(
                lambda: self.parent().currentWidget().stop()
            )

    def load_finished(self):
        tab_index = self.parent().indexOf(self)

        self.main_window.top_bar.nav_bar.reload_and_stop_button.setText("Z")
        self.main_window.top_bar.nav_bar.reload_and_stop_button.clicked.connect(
            lambda: self.parent().currentWidget().reload()
        )

        TAB_TITLE = self.page().title()
        TAB_ICON = self.page().icon()
        self.main_window.top_bar.tab_bar.tabs.setTabText(tab_index, TAB_TITLE)
        self.main_window.top_bar.tab_bar.tabs.setTabIcon(tab_index, TAB_ICON)

    def url_changed(self, qurl):
        if not self.parent().count() < 1:
            if self == self.parent().currentWidget():
                self.main_window.top_bar.nav_bar.url_bar.update_url(qurl, self)
