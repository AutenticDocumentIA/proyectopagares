import os
from ocr_extractionCloud import process_file
import configparser

# Cargar configuración
config = configparser.ConfigParser()
config.read("config.ini")

input_folder = config["PATHS"]["InputFolder"]

def process_all_files():
    """Procesa todos los archivos en la carpeta input/ y guarda el texto extraído en archivos .txt."""
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            print(f"🚀 Procesando archivo: {filename}")
            process_file(file_path)

if __name__ == "__main__":
    process_all_files()
