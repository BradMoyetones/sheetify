# app/ui/components/zip_group.py
import os
import zipfile
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from app.ui.components.file_item import FileItem  # Fíjate cómo importa su hermano

class ZipGroup(QFrame):
    remove_requested = Signal(object)
    
    def __init__(self, zip_path, parent=None):
        super().__init__(parent)
        self.zip_path = zip_path
        self.items = [] # Para almacenar referencias a los CSVs internos
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("zip_group")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Header del ZIP
        header = QWidget()
        header.setObjectName("zip_header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        zip_name = os.path.basename(zip_path)
        self.lbl_title = QLabel(f"[Archivo Comprimido] {zip_name}")
        self.lbl_title.setStyleSheet("font-weight: bold;")
        
        self.btn_toggle = QPushButton("Colapsar Contenido")
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.clicked.connect(self.toggle_content)
        
        self.btn_remove_zip = QPushButton("Eliminar ZIP Completo")
        self.btn_remove_zip.setObjectName("destructive")
        self.btn_remove_zip.setCursor(Qt.PointingHandCursor)
        self.btn_remove_zip.clicked.connect(lambda: self.remove_requested.emit(self))
        
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_toggle)
        header_layout.addWidget(self.btn_remove_zip)
        self.layout.addWidget(header)
        
        # Contenedor para los CSVs internos
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(15, 5, 15, 15)
        self.layout.addWidget(self.content_container)
        
        self.load_zip_contents()

    def load_zip_contents(self):
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as z:
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if not csv_files:
                    lbl = QLabel("No se encontraron archivos CSV dentro de este ZIP.")
                    self.content_layout.addWidget(lbl)
                    return
                
                for csv_file in csv_files:
                    item = FileItem(path=None, file_type='zip_item', zip_path=self.zip_path, internal_path=csv_file)
                    item.remove_requested.connect(self.remove_internal_item)
                    self.content_layout.addWidget(item)
                    self.items.append(item)
        except Exception as e:
            err = QLabel(f"Error al leer ZIP: {e}")
            self.content_layout.addWidget(err)

    def toggle_content(self, checked):
        self.content_container.setVisible(not checked)
        self.btn_toggle.setText("Mostrar Contenido" if checked else "Colapsar Contenido")

    def remove_internal_item(self, item):
        self.content_layout.removeWidget(item)
        item.deleteLater()
        self.items.remove(item)
        # Si se eliminan todos los CSVs, sugerir borrar el ZIP
        if not self.items:
            self.lbl_title.setText(self.lbl_title.text() + " (Vacío)")

    def get_tasks(self):
        """Retorna las tareas configuradas de los CSVs internos marcados."""
        tasks = []
        for item in self.items:
            t = item.get_task_info()
            if t: tasks.append(t)  # noqa: E701
        return tasks