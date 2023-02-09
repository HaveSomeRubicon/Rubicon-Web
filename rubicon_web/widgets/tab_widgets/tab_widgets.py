from PyQt5.QtWidgets import QStackedWidget


class TabWidgets(QStackedWidget):
    def __init__(self, parent, *args, **kwargs):
        """Initializes the stacked widget which will contain the web views"""
        super(TabWidgets, self).__init__(parent=parent, *args, **kwargs)
        self.parent().log(
            "TabWidgets has succesfully been initialized", "SUCCESS", "tab_widgets.py"
        )

    def get_open_urls(self):
        """Returns a list of all open URLs"""
        return [self.widget(index).url().toString() for index in range(self.count())]
