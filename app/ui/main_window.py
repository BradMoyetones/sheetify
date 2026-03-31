from app.core.utils import render_svg_icon, get_resource_path
import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFrame, QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize

from app.ui.views.dashboard import ConversionView

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sheetify")
        self.resize(1100, 750)
        self.is_expanded = True
        self.sidebar_buttons = []
        
        # Acceso al manager global
        self.theme_manager = QApplication.instance().theme_manager
        self.theme = self.theme_manager.get_current_tokens()

        # Conectamos la señal del manager a nuestro método de actualización (Esto para actualizar iconos y estilos)
        self.theme_manager.theme_changed.connect(self.update_ui_theme)

        self.setup_ui()
        self.setup_animations()

    def update_ui_theme(self, new_tokens):
        """Esta función se ejecuta sola cuando alguien pulsa el botón"""
        self.theme = new_tokens
        self.btn_theme.setText("  Dark" if self.theme_manager.is_dark else "  Light")
        
        # Actualizamos todos los iconos de la sidebar
        self.btn_toggle.setIcon(render_svg_icon(get_resource_path("assets/menu.svg"), self.theme['muted_fg']))
        self.btn_theme.setIcon(render_svg_icon(get_resource_path("assets/moon.svg" if self.theme_manager.is_dark else "assets/sun.svg"), self.theme['muted_fg']))
        

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0) # El margen lo da el wrapper
        main_layout.setSpacing(0)

        # --- SIDEBAR ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        
        self.btn_toggle = QPushButton("  Menu")
        self.btn_toggle.setObjectName("toggle_btn")
        self.btn_toggle.setIcon(render_svg_icon(get_resource_path("assets/menu.svg"), self.theme['muted_fg']))
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        # Se crea el boton para cambiar tema
        self.btn_theme = QPushButton("  Dark" if self.theme_manager.is_dark else "  Light")
        self.btn_theme.setIcon(render_svg_icon(get_resource_path("assets/moon.svg" if self.theme_manager.is_dark else "assets/sun.svg"), self.theme['muted_fg']))
        self.btn_theme.clicked.connect(self.theme_manager.toggle_theme)
        
        sidebar_layout.addWidget(self.btn_toggle)
        self.add_sidebar_button(sidebar_layout, "Procesar", "assets/file.svg")
        self.add_sidebar_button(sidebar_layout, "Configuración", "assets/settings.svg")
        sidebar_layout.addWidget(self.btn_theme) # Se agrega el boton para cambiar tema al layout
        sidebar_layout.addStretch()

        # --- CONTENT WRAPPER (Efecto Inset) ---
        # Este es el contenedor que se ve como una "caja" con bordes redondeados
        self.content_wrapper = QFrame()
        self.content_wrapper.setObjectName("content_wrapper")
        wrapper_layout = QVBoxLayout(self.content_wrapper)
        wrapper_layout.setContentsMargins(1, 1, 1, 1) # Margen interno mínimo

        self.pages = QStackedWidget()
        self.pages.addWidget(ConversionView()) # Tu vista refactorizada
        self.pages.addWidget(QWidget()) # Config placeholder
        
        wrapper_layout.addWidget(self.pages)

        # Ensamblaje final con padding para el efecto "flotante"
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_wrapper)
        
        # Le damos un margen al wrapper para que no toque los bordes de la ventana
        main_layout.setContentsMargins(0, 10, 10, 10) 

    def add_sidebar_button(self, layout, text, icon_path):
        btn = QPushButton(f"  {text}")
        btn.setIcon(render_svg_icon(get_resource_path(icon_path), self.theme['muted_fg']))
        btn.setIconSize(QSize(18, 18))
        btn.setProperty("original_text", f"  {text}")
        btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn)
        self.sidebar_buttons.append(btn)

    def setup_animations(self):
        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def toggle_sidebar(self):
        if self.is_expanded:
            target_width = 70
            self.btn_toggle.setText("")
            for btn in self.sidebar_buttons: btn.setText("")  # noqa: E701
            # Al colapsar, podemos hacer que el radio sea mayor o igual
            self.content_wrapper.setStyleSheet("border-radius: 16px;") 
        else:
            target_width = 200
            self.btn_toggle.setText("  Ocultar")
            for btn in self.sidebar_buttons: btn.setText(btn.property("original_text"))  # noqa: E701

        self.anim.setStartValue(self.sidebar.width())
        self.anim.setEndValue(target_width)
        self.anim.start()
        self.sidebar.setFixedWidth(target_width)
        self.is_expanded = not self.is_expanded