from PySide6.QtWidgets import QPushButton

class Button(QPushButton):
    def __init__(self, text, variant="primary", parent=None):
        super().__init__(text, parent)
        self.setProperty("class", variant)