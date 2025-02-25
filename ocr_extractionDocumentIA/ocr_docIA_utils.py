import os

# Configurar manualmente las credenciales en el código
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/User/Documents/credencialesAPI2.json"


from google.cloud import documentai

# 📌 Configuración
PROJECT_ID = "778281436674"
LOCATION = "us"  # Asegúrate de usar la ubicación correcta
PROCESSOR_ID = "d4a8d7ac950d9750"
FILE_PATH = r"C:\Users\User\Desktop\aumento test set 2\output\9712155_3099600011344 (1).pdf"
MIME_TYPE = "application/pdf"

def process_document():
    """Procesa un PDF con Document AI y obtiene tanto etiquetas predefinidas como datos extra detectados"""

    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"

    with open(FILE_PATH, "rb") as file:
        file_content = file.read()

    raw_document = {"content": file_content, "mime_type": MIME_TYPE}
    request = {"name": name, "raw_document": raw_document}

    response = client.process_document(request=request)

    # 📌 Mostrar solo las entidades etiquetadas en el entrenamiento
    print("\n📌 Datos extraídos según etiquetas entrenadas:\n")
    for entity in response.document.entities:
        print(f"{entity.type_}: {entity.mention_text}")

    # 📌 Mostrar información adicional detectada por Document AI
    print("\n📌 Información extra detectada por Document AI (sin entrenamiento):\n")
    for entity in response.document.entities:
        if entity.confidence < 0.6:  # Si el modelo no estaba 100% seguro, aún así lo mostramos
            print(f"{entity.type_}: {entity.mention_text} (Confianza: {entity.confidence:.2f})")

# 🔹 Ejecutar la extracción combinada
process_document()
