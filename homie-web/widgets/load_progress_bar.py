from PyQt5.QtWidgets import QProgressBar


class LoadProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super(LoadProgressBar, self).__init__(parent)
        
        self.setFixedHeight(15)
        self.setTextVisible(False)

    def update_progress_bar(self, progress: int):
        self.setValue(progress)
        if progress == 100:
            self.hide()
        else:
            self.show()