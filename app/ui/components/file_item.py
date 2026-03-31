from app.core.utils import render_svg_icon, get_resource_path
import os
from PySide6.QtWidgets import QFrame, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton, QFileDialog, QApplication
from PySide6.QtCore import Qt, Signal
from app.core.engine import ExcelEngine # Solo lo necesitas para la acción directa

class FileItem(QFrame):
    remove_requested = Signal(object)
    
    def __init__(self, path, file_type='csv', zip_path=None, internal_path=None, parent=None):
        super().__init__(parent)
        self.path = path
        self.file_type = file_type
        self.zip_path = zip_path
        self.internal_path = internal_path

        self.theme_manager = QApplication.instance().theme_manager
        self.theme_manager.theme_changed.connect(self.update_styles)
        self.theme = self.theme_manager.get_current_tokens()
        
        # Estilos de la fila
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("file_item")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. Checkbox para selección individual
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        
        # 2. Nombre Original (Info estática)
        original_name = os.path.basename(self.internal_path if self.file_type == 'zip_item' else self.path)
        base_name, _ = os.path.splitext(original_name)
        
        self.lbl_original = QLabel(f"De: {original_name}")
        self.lbl_original.setObjectName("lbl_original")
        self.lbl_original.setStyleSheet("font-size: 12px;")
        
        # 3. Input para renombrar (El nombre final del archivo o de la hoja)
        self.input_rename = QLineEdit()
        self.input_rename.setText(base_name)
        self.input_rename.setPlaceholderText("Nombre de salida...")
        self.input_rename.setToolTip("Edita el nombre final del Excel o la hoja")
        
        # 4. Botón Exportar Individualmente (Fuerza guardar este único archivo donde diga el usuario)
        self.btn_export_single = QPushButton()
        self.btn_export_single.setIcon(render_svg_icon(get_resource_path("assets/save.svg"), self.theme['primary_fg']))
        self.btn_export_single.setToolTip("Exportar solo este archivo independientemente del modo global")
        self.btn_export_single.setCursor(Qt.PointingHandCursor)
        self.btn_export_single.clicked.connect(self.export_directly)
        
        # 5. Botón Remover Individual
        self.btn_remove = QPushButton()
        self.btn_remove.setIcon(render_svg_icon(get_resource_path("assets/trash.svg"), self.theme['destructive_fg']))
        self.btn_remove.setObjectName("destructive")
        self.btn_remove.setToolTip("Quitar este archivo de la lista")
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.clicked.connect(lambda: self.remove_requested.emit(self))
        
        # Ensamblar fila
        layout.addWidget(self.checkbox)
        layout.addWidget(self.input_rename, stretch=2)
        layout.addWidget(self.lbl_original, stretch=1)
        layout.addWidget(self.btn_export_single)
        layout.addWidget(self.btn_remove)

    def update_styles(self, new_tokens):
        self.theme = new_tokens
        self.btn_remove.setIcon(render_svg_icon(get_resource_path("assets/trash.svg"), self.theme['destructive_fg']))
        self.btn_export_single.setIcon(render_svg_icon(get_resource_path("assets/save.svg"), self.theme['primary_fg']))
        
    def get_task_info(self):
        """Retorna el diccionario de tarea para el Engine si el checkbox está marcado."""
        if not self.checkbox.isChecked():
            return None
        return {
            'type': self.file_type,
            'path': self.path,
            'zip_path': self.zip_path,
            'internal_path': self.internal_path,
            'export_name': self.input_rename.text() or "Hoja_Sin_Nombre"
        }

    def export_directly(self):
        """Acción rápida: guardar solo este archivo."""
        task = self.get_task_info()
        if not task:
            # Si el usuario intentó guardar uno desmarcado, forzamos la info para este caso
            task = {
                'type': self.file_type,
                'path': self.path,
                'zip_path': self.zip_path,
                'internal_path': self.internal_path,
                'export_name': self.input_rename.text() or "Hoja_Sin_Nombre"
            }
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Guardar Excel Individual", f"{task['export_name']}.xlsx", "Excel (*.xlsx)")
        if save_path:
            target_dir = os.path.dirname(save_path)
            # Reutilizamos el motor forzando nombre personalizado
            ExcelEngine.export_single_excel([task], target_dir, os.path.basename(save_path))