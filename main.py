import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui.main_window import MainWindow

def main():
    # Inicializar la aplicación de Qt
    app = QApplication(sys.argv)
    app.setApplicationName("CSV to Excel Pro")
    
    app.setStyle("Fusion") 

    window = MainWindow()
    
    # 900x650 por defecto
    window.setMinimumSize(850, 600)
    
    # Icono de app (opcional)
    # icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'app_icon.png')
    # if os.path.exists(icon_path):
    #    window.setWindowIcon(QIcon(icon_path))

    # Mostrar y arrancar el Event Loop
    window.show()
    
    # El sys.exit asegura que el proceso de Python se cierre correctamente cuando el usuario cierre la ventana
    sys.exit(app.exec())

if __name__ == "__main__":
    main()