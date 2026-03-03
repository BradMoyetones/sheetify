import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtSvg import QSvgRenderer

from app.ui.views import ConversionView

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procesador de Datos a Excel")
        self.resize(1100, 750)

        self.is_expanded = True
        self.sidebar_buttons = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(200)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(8)

        # Usar colores SVG consistentes con temas oscuros
        self.btn_toggle = QPushButton("  Ocultar")
        self.btn_toggle.setObjectName("toggle_btn")
        self.btn_toggle.setIcon(self.get_colored_icon(resource_path("assets/menu.svg"), "#94a3b8")) # Ajustado
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.btn_toggle)

        self.add_sidebar_button(sidebar_layout, "Procesar", "assets/file.svg")
        self.add_sidebar_button(sidebar_layout, "Configuración", "assets/settings.svg")

        sidebar_layout.addStretch()

        # --- CONTENT STACK ---
        self.pages = QStackedWidget()
        self.pages.setObjectName("content")

        self.conversion_page = ConversionView()
        self.config_page = QWidget() 

        self.pages.addWidget(self.conversion_page)
        self.pages.addWidget(self.config_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        # Navegación
        self.sidebar_buttons[0].clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.sidebar_buttons[1].clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.apply_styles()
    
    def add_sidebar_button(self, layout, text, icon_path):
        btn = QPushButton(f"  {text}")
        icon = self.get_colored_icon(resource_path(icon_path), "#94a3b8") # Ajustado a gris pizarra
        btn.setIcon(icon) 
        btn.setIconSize(QSize(18, 18))
        btn.setProperty("original_text", f"  {text}") 
        btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn)
        self.sidebar_buttons.append(btn)

    def toggle_sidebar(self):
        width_start = self.sidebar.width()
        if self.is_expanded:
            width_end = 65
            self.btn_toggle.setText("")
            for btn in self.sidebar_buttons:
                btn.setText("")
        else:
            width_end = 200
            self.btn_toggle.setText("  Ocultar")
            for btn in self.sidebar_buttons:
                btn.setText(btn.property("original_text"))

        self.anim.setStartValue(width_start)
        self.anim.setEndValue(width_end)
        self.anim.start()
        self.sidebar.setMaximumWidth(width_end)
        self.is_expanded = not self.is_expanded
    
    def get_colored_icon(self, svg_path, color_hex):
        renderer = QSvgRenderer(svg_path)
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color_hex))
        painter.end()
        return QIcon(pixmap)

    def apply_styles(self):
        # QSS ajustado para ser elegante, moderno y compatible visualmente (estética "Dark Mode / Premium Soft")
        self.setStyleSheet("""
            QWidget { 
                font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif; 
                font-size: 13px; 
                color: #e2e8f0; /* Texto base claro para fondos oscuros */
            }
            
            /* -- SIDEBAR -- */
            #sidebar { 
                background-color: #0f172a; /* Slate 900 profundo */
                border-right: 1px solid #1e293b; 
            }
            #sidebar QPushButton {
                background-color: transparent; 
                color: #94a3b8; /* Texto inactivo */
                text-align: left; 
                padding: 12px 16px; 
                border: none;
                border-radius: 8px; 
                font-weight: 500;
                margin: 0px 8px;
            }
            #sidebar QPushButton:hover { 
                background-color: #1e293b; 
                color: #f8fafc; /* Texto activo brillante */
            }
            
            /* -- CONTENIDO PRINCIPAL -- */
            #content { 
                background-color: #1e293b; /* Fondo general oscuro pero más claro que sidebar */
            }
            
            /* Etiquetas genéricas (para evitar que se pierdan en el fondo) */
            QLabel {
                color: #f8fafc;
            }

            /* -- BOTONES PRIMARIOS (Premium Emerald/Teal en lugar de azul Boostrap) -- */
            #primary_button {
                background-color: #0ea5e9; /* Sky 500 - Un azul moderno, vibrante pero no básico */
                color: white;
                padding: 10px 20px; 
                border-radius: 6px;
                font-weight: 600; 
                border: none;
            }
            #primary_button:hover { 
                background-color: #0284c7; /* Sky 600 */
            }
            #primary_button:disabled { 
                background-color: #334155; 
                color: #64748b; 
            }

            QPushButton {
                background-color: #0ea5e9; /* Sky 500 - Un azul moderno, vibrante pero no básico */
                color: white;
                padding: 6px 12px; 
                border-radius: 6px;
                font-weight: 600; 
                border: none;
            }
            
            /* -- BOTONES DE PELIGRO -- */
            #btn_danger {
                background-color: transparent;
                color: #ef4444; 
                border: 1px solid #7f1d1d; 
                border-radius: 6px; 
                padding: 6px 12px;
                font-weight: 500;
            }
            #btn_danger:hover { 
                background-color: #7f1d1d; 
                color: #fef2f2;
            }

            /* -- CONTENEDORES / CARDS -- */
            #file_item, #zip_group {
                background-color: #27384e; /* Slate 800 ligeramente aclarado */
                border: 1px solid #334155; 
                border-radius: 8px;
                margin-bottom: 8px;
            }
            #zip_header {
                background-color: #1e293b;
                border-bottom: 1px solid #334155;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            
            /* -- INPUTS -- */
            QLineEdit {
                padding: 10px; 
                border: 1px solid #475569;
                border-radius: 6px; 
                background-color: #0f172a; /* Fondo de input muy oscuro */
                color: #f8fafc;
                selection-background-color: #0ea5e9;
            }
            QLineEdit:focus { 
                border: 1px solid #0ea5e9; 
            }
            QLineEdit::placeholder {
                color: #64748b;
            }
            
            /* -- OPCIONES GLOBALES (Frame inferior) -- */
            #options_frame {
                background-color: #27384e;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 15px;
            }
            
            #scroll_area { 
                border: none; 
                background-color: transparent; 
            }
            
            /* Scrollbars elegantes para modo oscuro */
            QScrollBar:vertical {
                border: none;
                background: #1e293b;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #475569;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QCheckBox { color: #f8fafc; spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 1px solid #475569; background-color: #0f172a; }
            QCheckBox::indicator:checked { background-color: #0ea5e9; border: 1px solid #0ea5e9; }
            
            QRadioButton { color: #f8fafc; spacing: 8px; }
            QRadioButton::indicator { width: 18px; height: 18px; border-radius: 9px; border: 1px solid #475569; background-color: #0f172a; }
            QRadioButton::indicator:checked { background-color: #0ea5e9; border: 1px solid #0ea5e9; }
        """)