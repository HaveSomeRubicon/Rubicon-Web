from PyQt5.QtWidgets import QStackedWidget


class TabWidgets(QStackedWidget):
    def __init__(self, parent, *args, **kwargs):
        super(TabWidgets, self).__init__(parent=parent, *args, **kwargs)
