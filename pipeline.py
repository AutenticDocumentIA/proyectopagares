import os
import base64
from base64conversor.base64_utils import decode_base64_to_pdf
from ocr_extractionCloud import extract_text
import configparser

# Leer configuraciones
config = configparser.ConfigParser()
config.read('config.ini')

# Rutas
input_folder = config['PATHS']['InputFolder']
output_pdf_folder = config['PATHS']['ProcessedPDFs']
output_text_folder = config['PATHS']['ExtractedTexts']
google_credentials = config['OCR']['GoogleCredentials']  # Ruta a las credenciales de Google Cloud Vision
poppler_path = config['OCR']['PopplerPath']

# Configurar las credenciales para Google Cloud Vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials

def test_flow():
    # Verificar si las carpetas de salida existen, si no, crearlas
    os.makedirs(output_pdf_folder, exist_ok=True)
    os.makedirs(output_text_folder, exist_ok=True)

    # Iterar sobre los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        print(f"Verificando archivo en la carpeta de entrada: {filename}")
        input_file_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_pdf_path = os.path.join(output_pdf_folder, f"{base_name}_procesado.pdf")
        output_text_path = os.path.join(output_text_folder, f"{base_name}_extractedText.txt")

        print(f"Ruta de entrada: {input_file_path}")
        print(f"Ruta de salida PDF: {output_pdf_path}")
        print(f"Ruta de salida texto: {output_text_path}")

        # Determinar si el archivo es Base64 o PDF binario
        try:
            with open(input_file_path, "rb") as f:
                file_content = f.read()

            # Intentar decodificar como Base64
            try:
                base64_data = file_content.decode("utf-8")
                print(f"Archivo identificado como Base64: {filename}")
                decode_success = decode_base64_to_pdf(base64_data, output_pdf_path)
                if decode_success is not True:
                    print(f"Error al decodificar Base64: {decode_success}")
                    continue
            except (UnicodeDecodeError, base64.binascii.Error):
                print(f"Archivo identificado como PDF binario: {filename}")
                # Si es PDF binario, simplemente copia el archivo
                with open(output_pdf_path, "wb") as pdf_out:
                    pdf_out.write(file_content)

        except Exception as e:
            print(f"Error al leer el archivo {filename}: {e}")
            continue

        # Verificar si el PDF fue guardado correctamente
        if not os.path.exists(output_pdf_path):
            print(f"Error: El archivo PDF no se guardó correctamente en {output_pdf_path}")
            continue

        # Extraer texto del PDF usando Google Cloud Vision OCR
        try:
            text = extract_text(output_pdf_path, poppler_path)
            if not text:
                print(f"Advertencia: No se extrajo texto del archivo {output_pdf_path}")
        except Exception as e:
            print(f"Error al extraer texto del archivo PDF {output_pdf_path}: {e}")
            continue

        # Guardar el texto extraído
        try:
            with open(output_text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
        except Exception as e:
            print(f"Error al guardar el texto extraído para {output_text_path}: {e}")

        print(f"Procesado: {output_pdf_path}")
        print(f"Texto extraído: {output_text_path}")

if __name__ == "__main__":
    test_flow()
