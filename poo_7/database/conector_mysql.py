from .conector import Conector
import mysql 

class ConectorMySQL(Conector):
    marcador_parametro = '%s'

    def __init__(self, host='localhost', usuario='root', clave='masterdba', base_datos='biblioteca'):
        self.host = host
        self.usuario = usuario
        self.clave = clave
        self.base_datos = base_datos

    def obtener_conexion(self):
        # Import perezoso: si mysql-connector-python no está instalado, el resto del
        # proyecto (SQLite incluido) sigue funcionando sin problema. Solo falla si
        # de verdad se elige este motor.
        import mysql.connector
        return mysql.connector.connect(
            host=self.host,
            user=self.usuario,
            password=self.clave,
            database=self.base_datos
        )