# repositories/socio_repository.py
import sqlite3
from models.socio import Socio

try:
    import mysql.connector.errors as mysql_errors
except ImportError:
    mysql_errors = None


class SocioRepository:
    """Mismo patrón exacto que LibroRepository — el Repository nunca decide reglas
    de negocio, solo traduce objetos Modelo <-> filas de la tabla 'socios'."""

    def __init__(self, conexion, marcador='?'):
        self.conexion = conexion        # inyectada, no se crea aquí
        self.marcador = marcador

    def _errores_integridad(self):
        errores = [sqlite3.IntegrityError]
        if mysql_errors is not None:
            errores.append(mysql_errors.IntegrityError)
        return tuple(errores)

    def crear(self, socio):
        m = self.marcador
        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                f"INSERT INTO socios VALUES ({m}, {m})",
                (socio.numero_socio, socio.nombre)
            )
            self.conexion.commit()
            return True
        except self._errores_integridad():
            print(f"Ya existe un socio con el número {socio.numero_socio}")
            return False
        except (sqlite3.OperationalError,) as error:
            print(f"Error de base de datos: {error}")
            return False

    def buscar_por_numero(self, numero_socio):
        m = self.marcador
        try:
            cursor = self.conexion.cursor()
            cursor.execute(f"SELECT * FROM socios WHERE numero_socio = {m}", (numero_socio,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Socio(numero_socio=fila[0], nombre=fila[1])
        except sqlite3.Error as error:
            print(f"Error de base de datos: {error}")
            return None

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM socios")
        filas = cursor.fetchall()

        socios = []
        for fila in filas:
            socios.append(Socio(numero_socio=fila[0], nombre=fila[1]))
        return socios

    def actualizar(self, socio):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(
            f"UPDATE socios SET nombre = {m} WHERE numero_socio = {m}",
            (socio.nombre, socio.numero_socio)
        )
        self.conexion.commit()
        return cursor.rowcount > 0

    def eliminar(self, numero_socio):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(f"DELETE FROM socios WHERE numero_socio = {m}", (numero_socio,))
        self.conexion.commit()
        return cursor.rowcount > 0
