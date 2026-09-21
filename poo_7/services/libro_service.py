# services/libro_service.py
from models.libro import Libro

class LibroService:
    """
    Reglas de NEGOCIO sobre libros: validar, decidir, orquestar.
    Nunca escribe SQL (eso es trabajo exclusivo de LibroRepository) y nunca conoce
    sqlite3/mysql.connector — solo conoce al Repository que recibe inyectado.
    """

    def __init__(self, libro_repository):
        self.libro_repository = libro_repository

    def registrar_libro(self, isbn, titulo, copias_disponibles):
        # Validación de negocio ANTES de tocar la base de datos
        if not isbn or not isbn.strip():
            raise ValueError("El ISBN no puede estar vacío")
        if not titulo or not titulo.strip():
            raise ValueError("El título no puede estar vacío")
        if copias_disponibles < 0:
            raise ValueError("Las copias disponibles no pueden ser negativas")
        if self.libro_repository.buscar_por_isbn(isbn) is not None:
            raise ValueError(f"Ya existe un libro con el ISBN {isbn}")

        libro = Libro(isbn.strip(), titulo.strip(), copias_disponibles)
        return self.libro_repository.crear(libro)

    def obtener_libro(self, isbn):
        return self.libro_repository.buscar_por_isbn(isbn)

    def listar_libros(self):
        return self.libro_repository.listar()

    def actualizar_libro(self, isbn, titulo, copias_disponibles):
        libro_existente = self.libro_repository.buscar_por_isbn(isbn)
        if libro_existente is None:
            raise ValueError(f"No existe un libro con el ISBN {isbn}")
        if copias_disponibles < 0:
            raise ValueError("Las copias disponibles no pueden ser negativas")

        libro_existente.titulo = titulo.strip() if titulo else libro_existente.titulo
        libro_existente.copias_disponibles = copias_disponibles
        return self.libro_repository.actualizar(libro_existente)

    def eliminar_libro(self, isbn):
        if self.libro_repository.buscar_por_isbn(isbn) is None:
            raise ValueError(f"No existe un libro con el ISBN {isbn}")
        return self.libro_repository.eliminar(isbn)

    def prestar_libro(self, isbn):
        # Ejemplo de regla que NUNCA podría vivir en el Repository: depende del
        # estado del dominio (¿hay copias?), no de si la base de datos respondió bien.
        libro = self.libro_repository.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError(f"No existe un libro con el ISBN {isbn}")
        if not libro.esta_disponible():
            raise ValueError(f"No hay copias de '{libro.titulo}' disponibles")

        libro.copias_disponibles -= 1
        self.libro_repository.actualizar(libro)
        return libro

    def devolver_libro(self, isbn):
        libro = self.libro_repository.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError(f"No existe un libro con el ISBN {isbn}")

        libro.copias_disponibles += 1
        self.libro_repository.actualizar(libro)
        return libro
