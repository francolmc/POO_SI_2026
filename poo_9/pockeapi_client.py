import requests

BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT = 5 # segundos

class PokemonNoEncontradoError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass


def validar_nombre(nombre: str):
    nombre = nombre.strip().lower()
    if not nombre:
        raise ValueError("Escribe un nombre o numero")
    return nombre

def obtener_pockemon(nombre: str):
    nombre = validar_nombre(nombre)
    url = f"{BASE_URL}/pokemon/{nombre}"
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)
        if respuesta.status_code == 404:
            raise PokemonNoEncontradoError(nombre)
        return respuesta.json()
    except requests.exceptions.Timeout:
        raise ServicioNoDisponibleError("El servicio tarda demasiado.")
