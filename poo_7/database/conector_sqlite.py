from .conector import Conector
import sqlite3

class ConectorSQLite(Conector):
    marcador_parametro = '?'

    def __init__(self, ruta_bd='biblioteca.db'):
        self.ruta_bd = ruta_bd

    def obtener_conexion(self):
        return sqlite3.connect(self.ruta_bd)