from .conector import Conector
import mysql 

class ConectorMySQL(Conector):
    def __init__(self, usuario, pwd, puerto, host):
        super().__init__()

    def obtener_conexion(self):
        return mysql.connector