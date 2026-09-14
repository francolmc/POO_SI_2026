# Importamos las herramientas de conexion
from database.conexion import obtener_conexion, crear_tablas
# Importamos los modelos que regresentan las entidades
from models.libro import Libro
from models.socio import Socio
# Importamos los repositorios para gestionar los datos
from repositories.libro_repository import LibroRepository
from repositories.socio_repositorio import SocioRepository

# Validamos que la base de datos y tablas estan creadas
crear_tablas()

# Creamos la conexion principal con las base de datos
conexion = obtener_conexion()

# Crear los repositorios
repositorio_libro = LibroRepository(conexion)
repositorio_socio = SocioRepository(conexion)

# --- CREAR libros y socios (operaciones mutables) ---

# Creamos el objeto libro
try:
    nuevo_libro = Libro("978-0-2", "Rayuela", 2)
    # Gurdamos el libro en el repositorio de los libros
    repositorio_libro.crear(nuevo_libro)
except:
    print("El libro con ISB 978-0-2 ya existe")

# Crear el objeto socio
try:
    nuevo_socio = Socio(3, "Ana Pérez")
    repositorio_socio.crear(nuevo_socio)
except:
    print("El socio con numero 3 ya existe")

# -- BUSCAR libros y socios (operaciones NO mutables) --
print("Libro buscado por ISBN:", repositorio_libro.buscar_por_isbn("978-0-2").titulo)

print("Todos los libros:")
for libro in repositorio_libro.listar():
    print(f"{libro.isbn} - {libro.titulo} ({libro.copias_disponibles} disponibles)")

print("Socio buscado por Numero de Socio:", repositorio_socio.buscar_por_numero(3).nombre)

print("Todos los socio:")
for socio in repositorio_socio.listar():
    print(f"{socio.numero_socio} - {socio.nombre}")

# Una vez que terminamos de trabajar con la base de datos, podemos cerrar la conexion.
conexion.close()