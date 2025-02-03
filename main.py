import os
from google.cloud import vision
import os
import PyPDF2
import pdf2image
from google.cloud import vision
import cv2

# Configurar la variable de entorno
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Santiago\Documents\credencialesAPI.json"

# Inicializar el cliente de Vision API
client = vision.ImageAnnotatorClient()

print("Cliente inicializado correctamente:", client)


def procesar_imagen(ruta_imagen):
    client = vision.ImageAnnotatorClient()

    with open(ruta_imagen, "rb") as imagen:
        contenido = imagen.read()

    # Configuración de la solicitud
    imagen_vision = vision.Image(content=contenido)
    respuesta = client.document_text_detection(image=imagen_vision)

    # Mostrar el texto detectado
    texto_detectado = respuesta.text_annotations
    if texto_detectado:
        print("Texto detectado:")
        print(texto_detectado[0].description)
    else:
        print("No se detectó texto.")
# Mostrar el texto detectado y sus ubicaciones

# Ejemplo de uso
procesar_imagen(r"C:\Users\Santiago\Pictures\WhatsApp Image 2024-03-10 at 7.33.48 PM (1).jpeg")


