# services/socio_service.py
from models.socio import Socio


class SocioService:
    """Reglas de negocio sobre socios — mismo rol que LibroService, aplicado a Socio."""

    def __init__(self, socio_repository):
        self.socio_repository = socio_repository

    def registrar_socio(self, numero_socio, nombre):
        if numero_socio is None or numero_socio <= 0:
            raise ValueError("El número de socio debe ser un entero positivo")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if self.socio_repository.buscar_por_numero(numero_socio) is not None:
            raise ValueError(f"Ya existe un socio con el número {numero_socio}")

        socio = Socio(numero_socio, nombre.strip())
        return self.socio_repository.crear(socio)

    def obtener_socio(self, numero_socio):
        return self.socio_repository.buscar_por_numero(numero_socio)

    def listar_socios(self):
        return self.socio_repository.listar()

    def actualizar_socio(self, numero_socio, nombre):
        socio_existente = self.socio_repository.buscar_por_numero(numero_socio)
        if socio_existente is None:
            raise ValueError(f"No existe un socio con el número {numero_socio}")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        socio_existente.nombre = nombre.strip()
        return self.socio_repository.actualizar(socio_existente)

    def eliminar_socio(self, numero_socio):
        if self.socio_repository.buscar_por_numero(numero_socio) is None:
            raise SocioNoEncontradoError(f"No existe un socio con el número {numero_socio}")
        return self.socio_repository.eliminar(numero_socio)
