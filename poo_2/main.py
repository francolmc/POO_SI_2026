class Libro:
    def __init__(self, titulo: str, copias_disponibles: int):
        self.titulo = titulo
        self.__copias_disponibles = None
        self.copias_disponibles = copias_disponibles

    @property
    def copias_disponibles(self) -> int:
        return self.__copias_disponibles

    @copias_disponibles.setter
    def copias_disponibles(self, copias_disponibles: int):
        if copias_disponibles <= 0:
            raise ValueError("Solo valores positivos")
        else:
            self.__copias_disponibles = copias_disponibles

libro = Libro("Hola", 1)
libro.copias_disponibles = 10
