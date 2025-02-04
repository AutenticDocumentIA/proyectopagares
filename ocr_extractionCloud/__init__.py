import os
import configparser
from .ocr_utils import process_pdf, process_file  # ✅ Importamos correctamente desde `ocr_utils.py`

# Cargar configuración desde config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Obtener la ruta de las credenciales de Google Cloud Vision
google_credentials = config["OCR"].get("GoogleCredentials", "").strip()

# Validar que las credenciales existan y configurar la variable de entorno
if google_credentials and os.path.exists(google_credentials):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials  # ✅ Configurar automáticamente
    print(f"✅ Google Cloud Credentials configuradas desde: {google_credentials}")
else:
    raise ValueError("❌ ERROR: No se encontraron las credenciales de Google Cloud Vision. Verifica `config.ini`.")

# Exponer las funciones necesarias
__all__ = ["process_file", "process_pdf"]
