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
    # Tabla de la AGREGACIÓN Prestamo -> (Socio, Libro): solo guarda las llaves
    # foráneas, nunca copia los datos de socios/libros (eso violaría la agregación).
    # Nota: INTEGER PRIMARY KEY con autoincremento es sintaxis de SQLite; en MySQL
    # sería "id_prestamo INT AUTO_INCREMENT PRIMARY KEY" (fuera del alcance de este ejemplo).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_socio INTEGER NOT NULL,
            isbn VARCHAR(20) NOT NULL,
            fecha_prestamo VARCHAR(20) NOT NULL,
            fecha_devolucion VARCHAR(20),
            FOREIGN KEY (numero_socio) REFERENCES socios(numero_socio),
            FOREIGN KEY (isbn) REFERENCES libros(isbn)
        )
    """)
    conexion.commit()