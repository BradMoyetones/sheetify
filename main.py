import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui.main_window import MainWindow

def main():
    # 1. Inicializar la aplicación de Qt
    app = QApplication(sys.argv)
    app.setApplicationName("CSV to Excel Pro")
    
    # 2. Configurar el estilo visual (Opcional pero recomendado para Windows)
    # Esto ayuda a que los iconos y fuentes se vean nítidos en pantallas High DPI
    app.setStyle("Fusion") 

    # 3. Instanciar la ventana principal
    window = MainWindow()
    
    # 4. Ajustes de ventana
    # 900x650 es un tamaño ideal para este tipo de herramientas de escritorio
    window.setMinimumSize(850, 600)
    
    # Si tienes un icono de app (opcional):
    # icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'app_icon.png')
    # if os.path.exists(icon_path):
    #    window.setWindowIcon(QIcon(icon_path))

    # 5. Mostrar y arrancar el Event Loop
    window.show()
    
    # El sys.exit asegura que el proceso de Python se cierre 
    # correctamente cuando el usuario cierre la ventana.
    sys.exit(app.exec())

if __name__ == "__main__":
    main()