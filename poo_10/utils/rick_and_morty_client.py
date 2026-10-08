import requests
from models.personaje import Personaje

BASE_URL = 'https://rickandmortyapi.com/api'
TIMEOUT = 5 # segundos

class PersonajeNoEncontrdoError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass


def _get(ruta, params=None):
    try:
        return requests.get(f'{BASE_URL}{ruta}', params=params, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise ServicioNoDisponibleError("No hay conexion con el servicio.") from None
    except requests.exceptions.Timeout:
        raise ServicioNoDisponibleError("El servicio tarda en responder.") from None

def _json(respuesta):
    try:
        return respuesta.json()
    except ValueError:
        raise ServicioNoDisponibleError("La respues del servicio no es valida.") from None


def obtener_personaje(id_personaje):
    if not isinstance(id_personaje, int) or id_personaje < 1:
        raise ValueError("El id debe ser un numero entero positivo.")
    respuesta = _get(f'/character/{id_personaje}')
    if respuesta.status_code == 404:
        raise PersonajeNoEncontrdoError(f'El personaje con id={id_personaje} buscado no existe.')
    return Personaje.desde_dict(Personaje, _json(respuesta))