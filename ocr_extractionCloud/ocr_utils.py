import os
import io
import json
from google.cloud import vision
from pdf2image import convert_from_path
from base64conversor.base64_utils import decode_base64_to_pdf

def pdf_to_images(pdf_path, output_folder="./temp_images", dpi=300, poppler_path=None):
    """ Convierte un PDF en imágenes. """
    os.makedirs(output_folder, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    image_paths = []
    for i, page in enumerate(images):
        output_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        page.save(output_path, "JPEG")
        image_paths.append(output_path)
        print(f"✅ Imagen guardada: {output_path}")  # Depuración
    return image_paths

def extract_text_from_images(image_paths):
    """ Extrae texto de imágenes con Google Cloud Vision. """
    client = vision.ImageAnnotatorClient()
    extracted_text = ""

    for image_path in image_paths:
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)

        if response.error.message:
            raise Exception(f"Error en Cloud Vision: {response.error.message}")

        if response.full_text_annotation.text.strip():
            print(f"📄 Texto extraído de {image_path}:")
            print(response.full_text_annotation.text[:500])  # Muestra los primeros 500 caracteres para depuración
        else:
            print(f"⚠️ No se detectó texto en {image_path}")

        extracted_text += response.full_text_annotation.text + "\n"

    return extracted_text.strip()

def process_pdf(pdf_path, poppler_path=None):
    """ Procesa un PDF y devuelve solo el texto extraído. """
    image_paths = pdf_to_images(pdf_path, poppler_path=poppler_path)
    extracted_text = extract_text_from_images(image_paths)

    # Limpiar imágenes temporales
    for image_path in image_paths:
        os.remove(image_path)

    return extracted_text

def process_file(file_path):
    """ Procesa un archivo PDF o Base64 y guarda solo el texto extraído en un archivo .txt. """
    filename = os.path.basename(file_path)
    base_name, _ = os.path.splitext(filename)
    output_pdf_path = os.path.join("output/processed_pdfs", f"{base_name}_procesado.pdf")
    output_text_path = os.path.join("output/extracted_text", f"{base_name}.txt")

    try:
        with open(file_path, "rb") as f:
            content = f.read()

        try:
            base64_data = content.decode("utf-8")
            decode_base64_to_pdf(base64_data, output_pdf_path)
        except (UnicodeDecodeError, ValueError):
            with open(output_pdf_path, "wb") as pdf_out:
                pdf_out.write(content)

        extracted_text = process_pdf(output_pdf_path)

        # Guardar el texto en un archivo .txt
        with open(output_text_path, "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)

        print(f"✅ Texto extraído guardado en: {output_text_path}")
        return output_text_path

    except Exception as e:
        print(f"❌ Error procesando {filename}: {e}")
        return None
