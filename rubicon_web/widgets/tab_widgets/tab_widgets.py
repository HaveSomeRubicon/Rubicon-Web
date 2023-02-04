from PyQt5.QtWidgets import QStackedWidget


class TabWidgets(QStackedWidget):
    def __init__(self, parent, *args, **kwargs):
        super(TabWidgets, self).__init__(parent=parent, *args, **kwargs)

    def get_open_urls(self):
        return [self.widget(index).url().toString() for index in range(self.count())]