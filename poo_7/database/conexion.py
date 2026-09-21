import sqlite3
from .conector import Conector

RUTA_BD = 'biblioteca.db'

def obtener_conexion():
    # Unico lugar del proyecto que abre conexion
    return sqlite3.connect(RUTA_BD)

def crear_tablas(conexion: Conector):
    """
    SQL compatible con SQLite y MySQL a la vez (VARCHAR con largo, tipos simples,
    IF NOT EXISTS soportado por ambos motores). Se llama una sola vez al arrancar
    la app, sin importar qué Conector se haya usado para abrir 'conexion'.
    """
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            isbn VARCHAR(20) PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            copias_disponibles INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS socios (
            numero_socio INTEGER PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    """)
    conexion.commit()