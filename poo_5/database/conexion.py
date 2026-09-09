import sqlite3

RUTA_BD = 'biblioteca.db'

def obtener_conexion():
    # Unico lugar del proyecto que abre conexion
    return sqlite3.connect(RUTA_BD)

def crear_tablas():
    conexion = obtener_conexion()
    # De aqui en adelante es un estandar
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            isbn TEXT PRIMARY KEY, 
            titulo TEXT NOT NULL,
            copias_disponibles INTEGER
        )
    """)
    conexion.commit()
    conexion.close()