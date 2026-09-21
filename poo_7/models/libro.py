class Libro:
    def __init__(self, isbn:str, titulo:str, copias_disponibles:int):
        self.isbn = isbn
        self.titulo = titulo
        self.copias_disponibles = copias_disponibles

    def esta_disponible(self):
        if self.copias_disponibles > 0:
            return True
        else:
            return False

    # Nótese: ni una línea de SQL aquí.
    # El modelo no sabe que existe una base de datos.