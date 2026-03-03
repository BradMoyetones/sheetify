import os
import zipfile
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFileDialog, QProgressBar, QCheckBox, QLineEdit, 
    QRadioButton, QButtonGroup, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal
from app.core.engine import ExcelEngine

# ==========================================
# WORKER / HILO EN SEGUNDO PLANO
# ==========================================
class ConversionWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, tasks, mode, target_dir, combined_name="Exportacion_Maestra.xlsx"):
        super().__init__()
        self.tasks = tasks
        self.mode = mode
        self.target_dir = target_dir
        self.combined_name = combined_name

    def run(self):
        try:
            if self.mode == "single":
                result_path = ExcelEngine.export_single_excel(self.tasks, self.target_dir, self.combined_name)
                self.finished.emit(f"Exportación en un solo archivo completada:\n{result_path}")
            elif self.mode == "multiple":
                result_paths = ExcelEngine.export_multiple_excels(self.tasks, self.target_dir)
                msg = f"Exportación de {len(result_paths)} archivos completada en:\n{self.target_dir}"
                self.finished.emit(msg)
        except Exception as e:
            self.error.emit(str(e))

# ==========================================
# COMPONENTES VISUALES
# ==========================================
class FileItem(QFrame):
    """Fila para gestionar un CSV individual."""
    remove_requested = Signal(object)
    
    def __init__(self, path, file_type='csv', zip_path=None, internal_path=None, parent=None):
        super().__init__(parent)
        self.path = path
        self.file_type = file_type
        self.zip_path = zip_path
        self.internal_path = internal_path
        
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
        self.lbl_original.setStyleSheet("color: #64748b; font-size: 12px;")
        
        # 3. Input para renombrar (El nombre final del archivo o de la hoja)
        self.input_rename = QLineEdit()
        self.input_rename.setText(base_name)
        self.input_rename.setPlaceholderText("Nombre de salida...")
        self.input_rename.setToolTip("Edita el nombre final del Excel o la hoja")
        
        # 4. Botón Exportar Individualmente (Fuerza guardar este único archivo donde diga el usuario)
        self.btn_export_single = QPushButton("Guardar Individual")
        self.btn_export_single.setToolTip("Exportar solo este archivo independientemente del modo global")
        self.btn_export_single.setCursor(Qt.PointingHandCursor)
        self.btn_export_single.clicked.connect(self.export_directly)
        
        # 5. Botón Remover Individual
        self.btn_remove = QPushButton("Eliminar")
        self.btn_remove.setObjectName("btn_danger")
        self.btn_remove.setToolTip("Quitar este archivo de la lista")
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.clicked.connect(lambda: self.remove_requested.emit(self))
        
        # Ensamblar fila
        layout.addWidget(self.checkbox)
        layout.addWidget(self.input_rename, stretch=2)
        layout.addWidget(self.lbl_original, stretch=1)
        layout.addWidget(self.btn_export_single)
        layout.addWidget(self.btn_remove)

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

class ZipGroup(QFrame):
    """Componente Accordion para ZIPs."""
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
        self.lbl_title.setStyleSheet("font-weight: bold; color: #334155;")
        
        self.btn_toggle = QPushButton("Colapsar Contenido")
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.clicked.connect(self.toggle_content)
        
        self.btn_remove_zip = QPushButton("Eliminar ZIP Completo")
        self.btn_remove_zip.setObjectName("btn_danger")
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
                    lbl.setStyleSheet("color: #ef4444;")
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
            if t: tasks.append(t)
        return tasks


# ==========================================
# VISTA PRINCIPAL (EL DASHBOARD)
# ==========================================
class ConversionView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True) # Activamos Drag and Drop
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. TÍTULO Y BOTÓN AGREGAR
        header_layout = QHBoxLayout()
        title = QLabel("Procesador Inteligente de CSV a Excel")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #f8fafc;")
        
        self.btn_add = QPushButton("Cargar Archivos (CSV o ZIP)")
        self.btn_add.setObjectName("primary_button")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.clicked.connect(self.dialog_add_files)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add)
        main_layout.addLayout(header_layout)

        # 2. ÁREA DE LISTA (SCROLL) O EMPTY STATE
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        
        # Contenedor interno del scroll
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignTop)
        
        # Empty State
        self.lbl_empty = QLabel("No hay archivos en la cola.\nArrastra archivos .csv o .zip aquí, o usa el botón superior para cargar.")
        self.lbl_empty.setAlignment(Qt.AlignCenter)
        self.lbl_empty.setStyleSheet("color: #64748b; font-size: 14px; padding: 40px; border: 2px dashed #64748b; border-radius: 8px;")
        self.list_layout.addWidget(self.lbl_empty)
        
        self.scroll_area.setWidget(self.list_container)
        main_layout.addWidget(self.scroll_area, stretch=1)

        # 3. CONTROLES GLOBALES (Opciones de Exportación)
        options_frame = QFrame()
        options_frame.setObjectName("options_frame")
        options_layout = QVBoxLayout(options_frame)
        
        lbl_options = QLabel("Opciones de Exportación Global")
        lbl_options.setStyleSheet("font-weight: bold; color: #f8fafc;")
        options_layout.addWidget(lbl_options)
        
        radio_layout = QHBoxLayout()
        self.radio_group = QButtonGroup(self)
        
        self.radio_single = QRadioButton("Combinar en un Excel con hojas separadas")
        self.radio_single.setChecked(True)
        self.radio_multiple = QRadioButton("Exportar como archivos Excel individuales")
        
        self.radio_group.addButton(self.radio_single)
        self.radio_group.addButton(self.radio_multiple)
        radio_layout.addWidget(self.radio_single)
        radio_layout.addWidget(self.radio_multiple)
        radio_layout.addStretch()
        options_layout.addLayout(radio_layout)
        
        # Selector de directorio
        dir_layout = QHBoxLayout()
        self.input_dir = QLineEdit()
        self.input_dir.setPlaceholderText("Selecciona una carpeta destino...")
        self.input_dir.setReadOnly(True)
        
        self.btn_dir = QPushButton("Elegir Carpeta")
        self.btn_dir.setCursor(Qt.PointingHandCursor)
        self.btn_dir.clicked.connect(self.select_directory)
        
        dir_layout.addWidget(QLabel("Carpeta de salida:"))
        dir_layout.addWidget(self.input_dir, stretch=1)
        dir_layout.addWidget(self.btn_dir)
        options_layout.addLayout(dir_layout)
        
        main_layout.addWidget(options_frame)

        # 4. BARRA DE ESTADO Y BOTÓN FINAL
        footer_layout = QHBoxLayout()
        
        self.status_bar = QProgressBar()
        self.status_bar.setVisible(False)
        self.status_bar.setStyleSheet("QProgressBar { border: 1px solid #cbd5e1; border-radius: 4px; text-align: center; } QProgressBar::chunk { background-color: #3b82f6; }")
        
        self.lbl_status_text = QLabel("")
        self.lbl_status_text.setStyleSheet("color: #16a34a; font-weight: bold;")
        
        self.btn_process_all = QPushButton("Ejecutar Exportación Global")
        self.btn_process_all.setObjectName("primary_button")
        self.btn_process_all.setMinimumHeight(45)
        self.btn_process_all.setCursor(Qt.PointingHandCursor)
        self.btn_process_all.setEnabled(False)
        self.btn_process_all.clicked.connect(self.start_processing)
        
        footer_layout.addWidget(self.status_bar, stretch=1)
        footer_layout.addWidget(self.lbl_status_text, stretch=1)
        footer_layout.addWidget(self.btn_process_all)
        
        main_layout.addLayout(footer_layout)

    # --- DRAG & DROP EVENTOS ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.process_incoming_files(files)

    # --- LÓGICA DE INTERFAZ ---
    def dialog_add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos", "", "Data (*.csv *.zip)")
        if files:
            self.process_incoming_files(files)

    def process_incoming_files(self, files):
        # Quitar el estado vacío si es la primera vez
        if self.lbl_empty.isVisible():
            self.lbl_empty.setVisible(False)
            
        for path in files:
            if path.endswith('.zip'):
                group = ZipGroup(path)
                group.remove_requested.connect(self.remove_item)
                self.list_layout.addWidget(group)
            elif path.endswith('.csv'):
                item = FileItem(path=path)
                item.remove_requested.connect(self.remove_item)
                self.list_layout.addWidget(item)
        
        self.check_queue()

    def remove_item(self, widget):
        self.list_layout.removeWidget(widget)
        widget.deleteLater()
        self.check_queue()

    def check_queue(self):
        # Contamos cuántos widgets hay (ignorando el empty label)
        count = self.list_layout.count()
        has_items = False
        for i in range(count):
            item = self.list_layout.itemAt(i).widget()
            if isinstance(item, (FileItem, ZipGroup)):
                has_items = True
                break
        
        self.lbl_empty.setVisible(not has_items)
        # Solo habilitar exportar si hay una carpeta elegida y items en cola
        self.btn_process_all.setEnabled(has_items and bool(self.input_dir.text()))

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta para exportar")
        if dir_path:
            self.input_dir.setText(dir_path)
            self.check_queue()

    # --- EJECUCIÓN DEL WORKER ---
    def start_processing(self):
        # Recolectar tareas
        tasks = []
        for i in range(self.list_layout.count()):
            widget = self.list_layout.itemAt(i).widget()
            if isinstance(widget, FileItem):
                t = widget.get_task_info()
                if t: tasks.append(t)
            elif isinstance(widget, ZipGroup):
                tasks.extend(widget.get_tasks())

        if not tasks:
            self.lbl_status_text.setText("Ningún archivo seleccionado para procesar.")
            self.lbl_status_text.setStyleSheet("color: #ef4444;")
            return

        mode = "single" if self.radio_single.isChecked() else "multiple"
        target_dir = self.input_dir.text()
        
        self.btn_process_all.setEnabled(False)
        self.status_bar.setVisible(True)
        self.status_bar.setRange(0, 0)
        self.lbl_status_text.setText("Procesando...")
        self.lbl_status_text.setStyleSheet("color: #ca8a04;") # Warning yellow para progreso

        self.worker = ConversionWorker(tasks, mode, target_dir)
        self.worker.finished.connect(self.on_process_finished)
        self.worker.error.connect(self.on_process_error)
        self.worker.start()

    def on_process_finished(self, msg):
        self.status_bar.setVisible(False)
        self.btn_process_all.setEnabled(True)
        self.lbl_status_text.setText("Completado")
        self.lbl_status_text.setStyleSheet("color: #16a34a;")
        
        # Opcional: mostrar un QMessageBox con el mensaje detallado (msg)

    def on_process_error(self, error_msg):
        self.status_bar.setVisible(False)
        self.btn_process_all.setEnabled(True)
        self.lbl_status_text.setText("Ocurrió un error")
        self.lbl_status_text.setStyleSheet("color: #ef4444;")
        print(error_msg)