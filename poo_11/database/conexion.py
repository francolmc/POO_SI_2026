import sqlite3

RUTA_BD = "rickmorty.db"

def obtener_conexion(ruta=RUTA_BD):
    return sqlite3.connect(ruta)

def create_tablas(conexion):
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS personajes (
            id_api INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            estado TEXT NOT NULL,
            especie TEXT NOT NULL,
            origen TEXT NOT NULL
        )
        """
    )

    conexion.commit()