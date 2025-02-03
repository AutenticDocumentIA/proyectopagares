import base64

def decode_base64_to_pdf(base64_data, output_filename):
    """
    Decodifica un string en base64 y lo guarda como un archivo PDF.
    """
    try:
        base64_data_clean = base64_data.replace("\n", "").replace("\r", "")
        pdf_data = base64.b64decode(base64_data_clean, validate=True)

        with open(output_filename, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        return True
    except Exception as e:
        return f"Error: {e}"

def extract_base64_from_pdf(file_path):
    """
    Extrae el contenido en Base64 de un archivo PDF.
    """
    try:
        with open(file_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()
            base64_content = base64.b64encode(pdf_content).decode('utf-8')
            return base64_content
    except Exception as e:
        return f"Error: {e}"
    

