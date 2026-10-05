from pockeapi_client import obtener_pockemon, PokemonNoEncontradoError, ServicioNoDisponibleError

def mostrar_datos(datos):
    tipos = ", ".join(t["type"]["name"] for t in datos["types"])
    print(f"#{datos['id']} - {datos['name'].capitalize()}")
    print(f"Tipos: {tipos}")
    print(f"Altura: {datos['height'] / 10} m")
    print(f"Peso: {datos['weight'] / 10} kg")

entrada = input("Nombre del pokemon: ")
salida = obtener_pockemon(entrada)
print("DATOS DEL POKEMON")
print(mostrar_datos(salida))