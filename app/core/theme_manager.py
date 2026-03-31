# app/core/theme_manager.py
from PySide6.QtCore import QObject, Signal
from app.core.tokens import tokens
from app.core.style_engine import get_stylesheet

class ThemeManager(QObject):
    theme_changed = Signal(dict)

    def __init__(self, app_instance):
        super().__init__()
        self.app = app_instance
        self.is_dark = True  # Estado inicial
        self.tokens = tokens.DARK if self.is_dark else tokens.LIGHT

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.tokens = tokens.DARK if self.is_dark else tokens.LIGHT
        
        # 1. Actualizamos el Stylesheet global de la App
        self.app.setStyleSheet(get_stylesheet(is_dark=self.is_dark))
        
        # 2. Notificamos a los componentes (para iconos o estilos inline)
        self.theme_changed.emit(tokens.DARK if self.is_dark else tokens.LIGHT)

    def get_current_tokens(self):
        return self.tokens