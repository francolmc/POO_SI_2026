from models.libro import Libro

class LibroRepository:
    def __init__(self, conexion):
        self.__conexion = conexion     # inyectada desde database/conexion.py

    def crear(self, libro: Libro):
        cursor = self.__conexion.cursor()
        cursor.execute(
            f"INSERT INTO libros VALUES (?, ?, ?)",
            (libro.isbn, libro.titulo, libro.copias_disponibles,)
        )
        self.__conexion.commit()

    def buscar_por_isbn(self, isbn:str) -> None | Libro:
        cursor = self.__conexion.cursor()
        consulta = f"SELECT isbn, titulo, copias_diponibles FROM libros WHERE isbn = ?"
        cursor.execute(consulta, (isbn,))
        registros = cursor.fetchone()
        if registros is None:
            return None
        # ('1234', 'Mi Libro', '3')
        return Libro(registros[0], registros[1], registros[2]) # el repositorio reconstruye el objeto Modelo a partir de la fila

    def listar(self):
        cursor = self.__conexion.cursor()
        cursor.execute(
            "SELECT isbn, titulo, copias_diponibles FROM libros"
        )
        registros = cursor.fetchall() # lista de tuplas
        libros = []
        for registro in registros:
            libros.append(
                Libro(registro[0], registro[1], registro[2])
            )
        return libros
