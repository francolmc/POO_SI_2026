from models.libro import Libro
import sqlite3

class LibroRepository:
    def __init__(self, conexion):
        self.__conexion = conexion     # inyectada desde database/conexion.py

    def crear(self, libro: Libro):
        try:
            cursor = self.__conexion.cursor()
            cursor.execute(
                f"INSERT INTO libros VALUES (?, ?, ?)",
                (libro.isbn, libro.titulo, libro.copias_disponibles,)
            )
            self.__conexion.commit()
        except sqlite3.IntegrityError:
            # Podemos enviar el error a un log de errores
            return False
        except sqlite3.OperationError:
            # Podemos enviar el error a un log de errores
            return False
        return True

    def buscar_por_isbn(self, isbn:str):
        cursor = self.__conexion.cursor()
        consulta = f"SELECT isbn, titulo, copias_disponibles FROM libros WHERE isbn = ?"
        cursor.execute(consulta, (isbn,))
        registros = cursor.fetchone()
        if registros is None:
            return None
        # ('1234', 'Mi Libro', '3')
        return Libro(registros[0], registros[1], registros[2]) # el repositorio reconstruye el objeto Modelo a partir de la fila

    def listar(self):
        cursor = self.__conexion.cursor()
        cursor.execute(
            "SELECT isbn, titulo, copias_disponibles FROM libros"
        )
        registros = cursor.fetchall() # lista de tuplas
        libros = []
        for registro in registros:
            libros.append(
                Libro(registro[0], registro[1], registro[2])
            )
        return libros

    def actualizar(self, libro: Libro):
        cursor = self.__conexion.cursor()
        cursor.execute("""
        UPDATE libros SET 
            titulo = ?,
            copias_disponibles = ?
        WHERE
            isbn = ?
        """, (libro.titulo, libro.copias_disponibles, libro.isbn))
        self.__conexion.commit()
        return cursor.rowcount > 0

    def eliminar(self, isbn: str):
        cursor = self.__conexion.cursor()
        cursor.execute("""
        DELETE FROM libros WHERE isbn = ?
        """, (isbn))
        self.__conexion.commit()
        return cursor.rowcount > 0
