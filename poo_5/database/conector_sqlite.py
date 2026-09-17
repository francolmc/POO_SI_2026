from .conector import Conector
import sqlite3

class ConectorSQLite(Conector):
    def __init__(self, ruta_db='biblioteca.db'):
        self.ruta_db = ruta_db

    def obtener_conexion(self):
        return sqlite3.connect(self.ruta_db)