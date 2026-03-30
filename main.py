import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui.main_window import MainWindow

def get_resource_path(relative_path):
    """ Obtiene la ruta absoluta a los recursos, compatible con PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    # Inicializar la aplicación de Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Sheetify")
    
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