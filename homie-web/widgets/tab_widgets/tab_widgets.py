from PyQt5.QtWidgets import QStackedWidget


class TabWidgets(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super(TabWidgets, self).__init__(*args, **kwargs)