# repositories/libro_repository.py
import sqlite3
from models.libro import Libro

try:
    import mysql.connector.errors as mysql_errors
except ImportError:
    mysql_errors = None


class LibroRepository:
    """
    Única capa del proyecto que escribe SQL, y siempre parametrizado (nunca f-strings
    ni concatenación con datos del usuario).
    """

    def __init__(self, conexion, marcador='?'):
        self.conexion = conexion        # inyectada desde el Conector, nunca se crea aquí
        self.marcador = marcador        # '?' para SQLite, '%s' para MySQL (ver database/conector.py)

    def _errores_integridad(self):
        # Cada driver tiene su propia jerarquía de excepciones. Se resuelven en tiempo
        # de ejecución para no forzar la instalación de mysql-connector si no se usa.
        errores = [sqlite3.IntegrityError]
        if mysql_errors is not None:
            errores.append(mysql_errors.IntegrityError)
        return tuple(errores)

    def crear(self, libro):
        m = self.marcador
        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                f"INSERT INTO libros VALUES ({m}, {m}, {m})",
                (libro.isbn, libro.titulo, libro.copias_disponibles)
            )
            self.conexion.commit()
            return True
        except self._errores_integridad():
            print(f"Ya existe un libro con el ISBN {libro.isbn}")
            return False
        except (sqlite3.OperationalError,) as error:
            print(f"Error de base de datos: {error}")
            return False

    def buscar_por_isbn(self, isbn):
        m = self.marcador
        try:
            cursor = self.conexion.cursor()
            cursor.execute(f"SELECT * FROM libros WHERE isbn = {m}", (isbn,))
            fila = cursor.fetchone()      # una sola fila o None
            if fila is None:
                return None
            # el repositorio reconstruye el objeto Modelo a partir de la fila
            return Libro(isbn=fila[0], titulo=fila[1], copias_disponibles=fila[2])
        except sqlite3.Error as error:
            print(f"Error de base de datos: {error}")
            return None

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM libros")
        filas = cursor.fetchall()    # lista de tuplas

        libros = []
        for fila in filas:
            libros.append(
                Libro(isbn=fila[0], titulo=fila[1], copias_disponibles=fila[2])
            )
        return libros

    def actualizar(self, libro):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(
            f"UPDATE libros SET titulo = {m}, copias_disponibles = {m} WHERE isbn = {m}",
            (libro.titulo, libro.copias_disponibles, libro.isbn)
        )
        self.conexion.commit()
        return cursor.rowcount > 0    # True si existía y se actualizó

    def eliminar(self, isbn):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(f"DELETE FROM libros WHERE isbn = {m}", (isbn,))
        self.conexion.commit()
        return cursor.rowcount > 0    # True si existía y se eliminó
