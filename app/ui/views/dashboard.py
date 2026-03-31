# app/ui/views/dashboard.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFileDialog, QProgressBar, QLineEdit, 
    QRadioButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt

# Importamos las piezas del rompecabezas
from app.ui.components.file_item import FileItem
from app.ui.components.zip_group import ZipGroup
from app.core.workers import ConversionWorker

class ConversionView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. TÍTULO Y BOTÓN AGREGAR
        header_layout = QHBoxLayout()
        title = QLabel("Procesador Inteligente de CSV a Excel")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        
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
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setWidgetResizable(True)
        
        # Contenedor interno del scroll
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.list_layout.setObjectName("list_layout")
        
        # Empty State
        self.lbl_empty = QLabel("No hay archivos en la cola.\nArrastra archivos .csv o .zip aquí, o usa el botón superior para cargar.")
        self.lbl_empty.setObjectName("empty_state")
        self.lbl_empty.setAlignment(Qt.AlignCenter)
        self.list_layout.addWidget(self.lbl_empty)
        
        self.scroll_area.setWidget(self.list_container)
        main_layout.addWidget(self.scroll_area, stretch=1)

        # 3. CONTROLES GLOBALES (Opciones de Exportación)
        options_frame = QFrame()
        options_frame.setObjectName("options_frame")
        options_layout = QVBoxLayout(options_frame)
        
        lbl_options = QLabel("Opciones de Exportación Global")
        lbl_options.setStyleSheet("font-weight: bold;")
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
        
        self.lbl_status_text = QLabel("")
        self.lbl_status_text.setStyleSheet("font-weight: bold;")
        
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
                if t: tasks.append(t)  # noqa: E701
            elif isinstance(widget, ZipGroup):
                tasks.extend(widget.get_tasks())

        if not tasks:
            self.lbl_status_text.setText("Ningún archivo seleccionado para procesar.")
            return

        mode = "single" if self.radio_single.isChecked() else "multiple"
        target_dir = self.input_dir.text()
        
        self.btn_process_all.setEnabled(False)
        self.status_bar.setVisible(True)
        self.status_bar.setRange(0, 0)
        self.lbl_status_text.setText("Procesando...")

        self.worker = ConversionWorker(tasks, mode, target_dir)
        self.worker.finished.connect(self.on_process_finished)
        self.worker.error.connect(self.on_process_error)
        self.worker.start()

    def on_process_finished(self, msg):
        self.status_bar.setVisible(False)
        self.btn_process_all.setEnabled(True)
        self.lbl_status_text.setText("Completado")
        
        # Opcional: mostrar un QMessageBox con el mensaje detallado (msg)

    def on_process_error(self, error_msg):
        self.status_bar.setVisible(False)
        self.btn_process_all.setEnabled(True)
        self.lbl_status_text.setText("Ocurrió un error")
        print(error_msg)