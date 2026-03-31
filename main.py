from app.core.style_engine import get_stylesheet
import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui.main_window import MainWindow
from app.core.theme_manager import ThemeManager
from app.core.utils import get_resource_path

def main():
    # Inicializar la aplicación de Qt
    app = QApplication(sys.argv)

    # Creamos el manager global (Esto para el tema de la app)
    # En caso de querer cambiar los colores de la app ir al archivo style_engine.py
    # en la carpeta core junto con el archivo tokens.py
    app.theme_manager = ThemeManager(app)
    app.setApplicationName("Sheetify")
    
    # Aplicamos tema inicial (Pronto se incluira el guardado local para recordar tema del usuario)
    app.setStyleSheet(get_stylesheet(is_dark=app.theme_manager.is_dark))
    app.setStyle("Fusion") 

    window = MainWindow()
    
    # 900x650 por defecto
    window.setMinimumSize(850, 600)
    
    # Icono de app (opcional)
    icon_path = get_resource_path(os.path.join('assets', 'sheetify_icon.png'))
    if os.path.exists(icon_path):
       window.setWindowIcon(QIcon(icon_path))
    else:
        print(f"No se encontró el icono en: {icon_path}")

    # Mostrar y arrancar el Event Loop
    window.show()
    
    # El sys.exit asegura que el proceso de Python se cierre correctamente cuando el usuario cierre la ventana
    sys.exit(app.exec())

if __name__ == "__main__":
    main()