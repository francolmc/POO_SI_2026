from utils.rick_and_morty_client import obtener_personaje


personaje = obtener_personaje(15)

print("nombre:", personaje.nombre)
print("origen:", personaje.origen)