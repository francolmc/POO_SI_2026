class LibroRepository:
    def __init__(self, conexion):
        self.__conexion = conexion

    def agregar_libro(self, isbn:str, titulo:str, copias:int):
        cursor = self.__conexion
        cursor.execute(
            f"INSERT INTO libros VALUES (?, ?, ?)",
            (isbn, titulo, copias,)
        )
        self.__conexion.commit()

    def buscar_libro_por_titulo(self, titulo:str):
        cursor = self.__conexion
        consulta = f"SELECT * FROM libros WHERE titulo = ?"
        cursor.execute(consulta, (titulo,))
        return cursor.fetchall()
