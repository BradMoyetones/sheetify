import pandas as pd
import zipfile
import os

class ExcelEngine:
    @staticmethod
    def read_csv_to_dataframe(task):
        """Lee un CSV y retorna un DataFrame, ya sea de una ruta directa o de un ZIP."""
        if task['type'] == 'csv':
            return pd.read_csv(task['path'])
        elif task['type'] == 'zip_item':
            with zipfile.ZipFile(task['zip_path'], 'r') as z:
                with z.open(task['internal_path']) as f:
                    return pd.read_csv(f)
        return None

    @staticmethod
    def export_single_excel(tasks, target_directory, file_name="Exportacion_Maestra.xlsx"):
        """Modo A: Junta todos los CSV seleccionados en un solo Excel con múltiples hojas."""
        output_path = os.path.join(target_directory, file_name)
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            for task in tasks:
                df = ExcelEngine.read_csv_to_dataframe(task)
                if df is not None:
                    # Limitar nombre de hoja a 31 caracteres (regla estricta de Excel)
                    sheet_name = task['export_name'][:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        return output_path

    @staticmethod
    def export_multiple_excels(tasks, target_directory):
        """Modo B: Exporta cada CSV seleccionado como un archivo Excel independiente."""
        exported_files = []
        for task in tasks:
            df = ExcelEngine.read_csv_to_dataframe(task)
            if df is not None:
                # Asegurar que termina en .xlsx
                file_name = f"{task['export_name']}.xlsx"
                output_path = os.path.join(target_directory, file_name)
                df.to_excel(output_path, index=False)
                exported_files.append(output_path)
        return exported_files