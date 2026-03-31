# app/core/workers.py
from PySide6.QtCore import QThread, Signal
from app.core.engine import ExcelEngine

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
                self.progress.emit(100)
                self.finished.emit(msg)
        except Exception as e:
            self.error.emit(str(e))