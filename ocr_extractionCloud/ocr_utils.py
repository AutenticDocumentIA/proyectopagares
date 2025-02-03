from google.cloud import vision
from pdf2image import convert_from_path
import os
import io

def pdf_to_images(pdf_path, output_folder="./temp_images", dpi=300, poppler_path=None):
    """
    Convierte cada página de un PDF en una imagen.
    :param pdf_path: Ruta del archivo PDF.
    :param output_folder: Carpeta donde se guardarán las imágenes.
    :param dpi: Resolución de las imágenes generadas.
    :param poppler_path: Ruta de Poppler para la conversión de PDF a imágenes.
    :return: Lista de rutas de las imágenes generadas.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)

        # Convierte el PDF a imágenes usando la ruta de Poppler
        images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        image_paths = []
        for i, page in enumerate(images):
            output_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
            page.save(output_path, "JPEG")
            image_paths.append(output_path)
        return image_paths
    except Exception as e:
        raise Exception(f"Error al convertir PDF a imágenes: {e}")

def extract_text_from_images(image_paths):
    """
    Extrae texto de una lista de imágenes utilizando la API de Google Cloud Vision.
    :param image_paths: Lista de rutas de las imágenes.
    :return: Texto extraído de las imágenes.
    """
    try:
        # Inicializa el cliente de la API de Google Vision
        client = vision.ImageAnnotatorClient()

        extracted_text = ""
        for image_path in image_paths:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            # Configura la solicitud para la API
            image = vision.Image(content=content)

            # Llama a la API de detección de texto
            response = client.document_text_detection(image=image)

            if response.error.message:
                raise Exception(f"Error en la API de Vision: {response.error.message}")

            # Agrega el texto extraído de la imagen actual
            extracted_text += response.full_text_annotation.text + "\n"

        return extracted_text.strip()

    except Exception as e:
        return f"Error al extraer texto de imágenes: {e}"

def extract_text(pdf_path, output_folder="./temp_images", poppler_path=None):
    """
    Extrae texto de un archivo PDF utilizando la API de Google Cloud Vision.
    :param pdf_path: Ruta del archivo PDF.
    :param output_folder: Carpeta temporal para las imágenes.
    :param poppler_path: Ruta de Poppler para la conversión de PDF a imágenes.
    :return: Texto extraído.
    """
    try:
        # Convierte el PDF en imágenes
        image_paths = pdf_to_images(pdf_path, output_folder, poppler_path=poppler_path)

        # Extrae texto de las imágenes generadas
        text = extract_text_from_images(image_paths)

        # Limpia las imágenes temporales
        for image_path in image_paths:
            os.remove(image_path)

        return text

    except Exception as e:
        return f"Error al procesar el archivo PDF: {e}"
