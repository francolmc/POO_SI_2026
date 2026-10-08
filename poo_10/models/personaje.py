
class DatosInvalidosRickAndMortyError(Exception):
    pass

class Personaje:
    def __init__(self, id_api, nombre, estado, especie, origen):
        self.id_api = id_api
        self.nombre = nombre
        self.estado = estado
        self.especie = especie
        self.origen = origen

    def desde_dict(cls, d):
        try:
            return cls(d["id"], d["name"], d["status"], d["species"], d["origin"]["name"])
        except (KeyError, TypeError):
            raise DatosInvalidosRickAndMortyError(
                "La respuesta de la API de Rick And Morty no es la esperada"
            ) from None

    def esta_vivo(self):
        return self.estado == "Alive"

        