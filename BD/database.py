import pandas as pd
import mysql.connector
from mysql.connector import Error
from conexiondb import connect_to_mysql

# Cargar datos desde Excel con validaciones
def load_excel(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name="Hoja 1", dtype=str)
        print("📝 Columnas detectadas:", df.columns.tolist())

        # Definir columnas esperadas
        columnas_correctas = [
            'iddocumento_pagare', 'fecha_grabacion_pagare', 'numpagareentidad', 'fechadesembolso',
            'fecha_firma', 'idotorgantepagare', 'idapoderadopagare', 'valorpesosdesembolso', 
            'valorpesosdiligenciamiento', 'valorpesosactual', 'xmltemporal', 'constancia', 
            'fechavencimientofinanciero', 'codigo_georeferenciacion', 'resultado_verificacion', 'fecha_ultima_verificacion'
        ]
        
        # Filtrar columnas existentes
        df = df[[col for col in columnas_correctas if col in df.columns]]

        # Convertir valores NaN a None
        df = df.astype(object).where(pd.notna(df), None)

        # Convertir iddocumento_pagare a numérico y eliminar nulos
        df['iddocumento_pagare'] = pd.to_numeric(df['iddocumento_pagare'], errors='coerce')
        df = df.dropna(subset=['iddocumento_pagare'])  # Eliminar registros sin ID
        df['iddocumento_pagare'] = df['iddocumento_pagare'].astype(int)

        return df
    except Exception as e:
        print(f"❌ Error al cargar el Excel compa: {e}")
        exit()

# Crear la tabla en MySQL
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS pagares (
        iddocumento_pagare BIGINT PRIMARY KEY,
        fecha_grabacion_pagare DATE NULL,
        numpagareentidad VARCHAR(255) NULL,
        fechadesembolso DATE NULL,
        fecha_firma DATE NULL,
        idotorgantepagare BIGINT NULL,
        idapoderadopagare BIGINT NULL,
        valorpesosdesembolso DECIMAL(18,2) NULL,
        valorpesosdiligenciamiento DECIMAL(18,2) NULL,
        valorpesosactual DECIMAL(18,2) NULL,
        xmltemporal VARCHAR(255) NULL,
        constancia INT NULL,
        fechavencimientofinanciero DATE NULL,
        codigo_georeferenciacion VARCHAR(255) NULL,
        resultado_verificacion VARCHAR(255) NULL,
        fecha_ultima_verificacion DATETIME NULL
    );
    """
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    print("✅ Tabla 'pagares' creada o ya existente.")

# Insertar datos en MySQL
def insert_data(connection, df):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO pagares (iddocumento_pagare, fecha_grabacion_pagare, numpagareentidad, fechadesembolso,
                            fecha_firma, idotorgantepagare, idapoderadopagare, valorpesosdesembolso, 
                            valorpesosdiligenciamiento, valorpesosactual, xmltemporal, constancia, 
                            fechavencimientofinanciero, codigo_georeferenciacion, resultado_verificacion, fecha_ultima_verificacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = df.values.tolist()
        cursor.executemany(query, data)
        connection.commit()
        print(f"✅ {cursor.rowcount} registros insertados.")
    except Error as e:
        print(f"❌ Error al insertar datos: {e}")

# Ejecutar script
if __name__ == "__main__":
    file_path = r"C:\Users\User\Documents\Copia de PDF Pagarés Fisicos.xlsx" #cambiar ruta cuando se ejecute en producción porfa
    df = load_excel(file_path)

    try:
        connection = connect_to_mysql()
        if connection:
            create_table(connection)
            insert_data(connection, df)
            connection.close()
            print("✅ Proceso completado.")
    except Error as e:
        print(f"❌ Error en la conexión compa): {e}")

