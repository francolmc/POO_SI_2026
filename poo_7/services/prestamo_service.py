# services/prestamo_service.py
from datetime import date
from models.prestamo import Prestamo


class PrestamoService:
    """
    Aquí es donde se ARMA la agregación: este Service NUNCA crea un Socio ni un
    Libro nuevo. Los BUSCA entre los que ya existen (a través de SocioRepository
    y LibroRepository), valida la regla de negocio, y recién ahí los agrega
    dentro de un Prestamo nuevo.

    Igual que LibroService y SocioService de este proyecto: reglas de negocio
    sí, SQL jamás, y los errores se reportan con ValueError (mismo estilo que
    ya usan los otros dos Service).
    """

    def __init__(self, prestamo_repository, socio_repository, libro_repository):
        self.prestamo_repository = prestamo_repository
        self.socio_repository = socio_repository
        self.libro_repository = libro_repository

    def realizar_prestamo(self, numero_socio, isbn):
        socio = self.socio_repository.buscar_por_numero(numero_socio)
        if socio is None:
            raise ValueError(f"No existe un socio con el número {numero_socio}")

        libro = self.libro_repository.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError(f"No existe un libro con el ISBN {isbn}")
        if not libro.esta_disponible():
            raise ValueError(f"No hay copias de '{libro.titulo}' disponibles")

        # --- Agregación en acción ---
        # El Prestamo referencia los MISMOS objetos socio y libro que ya viven
        # en el sistema (no crea copias, no inventa datos nuevos de ellos).
        prestamo = Prestamo(
            id_prestamo=None,
            socio=socio,
            libro=libro,
            fecha_prestamo=date.today().isoformat(),
            fecha_devolucion=None
        )

        # Misma regla que LibroService.prestar_libro(): baja 1 copia.
        libro.copias_disponibles -= 1
        self.libro_repository.actualizar(libro)

        self.prestamo_repository.crear(prestamo)
        return prestamo

    def registrar_devolucion(self, id_prestamo):
        prestamo = self.prestamo_repository.buscar_por_id(id_prestamo)
        if prestamo is None:
            raise ValueError(f"No existe un préstamo con id {id_prestamo}")
        if not prestamo.esta_vigente():
            raise ValueError("Este préstamo ya fue devuelto")

        prestamo.libro.copias_disponibles += 1
        self.libro_repository.actualizar(prestamo.libro)

        fecha_devolucion = date.today().isoformat()
        self.prestamo_repository.registrar_devolucion(id_prestamo, fecha_devolucion)
        prestamo.fecha_devolucion = fecha_devolucion  # reflejar el cambio también en el objeto en memoria
        return prestamo

    def historial_de_socio(self, numero_socio):
        if self.socio_repository.buscar_por_numero(numero_socio) is None:
            raise ValueError(f"No existe un socio con el número {numero_socio}")
        return self.prestamo_repository.listar_por_socio(numero_socio)

    def listar_prestamos(self):
        return self.prestamo_repository.listar()
