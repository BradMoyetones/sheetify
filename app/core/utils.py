import sys
import os
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

def render_svg_icon(path, color_hex, size=24):
    renderer = QSvgRenderer(path)
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color_hex))
    painter.end()
    return QIcon(pixmap)

def get_resource_path(relative_path):
    """
    Obtiene la ruta absoluta a los recursos.
    """
    if hasattr(sys, '_MEIPASS'):
        # Ruta cuando la app está empaquetada (.exe / .app)
        return os.path.join(sys._MEIPASS, relative_path)
    
    # Ruta en desarrollo (buscamos desde la raíz del proyecto)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    return os.path.join(base_path, relative_path)