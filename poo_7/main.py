# main.py — Aplicación mantenedora CRUD (Libro y Socio), motor intercambiable
#
# Regla de oro del proyecto: main.py nunca abre una conexión directamente ni
# escribe SQL. Solo elige el Conector, arma las capas y delega todo a services/.
#
#   main.py  →  services/ (reglas de negocio)  →  repositories/ (SQL)  →  database/conector.py  →  BD

from database.conector_sqlite import ConectorSQLite
from database.conector_mysql import ConectorMySQL
from database.conexion import crear_tablas
from repositories.libro_repository import LibroRepository
from repositories.socio_repository import SocioRepository
from repositories.prestamo_repository import PrestamoRepository
from services.libro_service import LibroService
from services.socio_service import SocioService
from services.prestamo_service import PrestamoService


# --- 1) Elegir el motor. Esta es la ÚNICA línea que cambia entre SQLite y MySQL. ---
MOTOR = 'mysql'   # cambiar a 'mysql' para usar MySQL (requiere mysql-connector-python
                    # instalado y una base 'biblioteca' creada de antemano en el servidor)

if MOTOR == 'sqlite':
    conector = ConectorSQLite('biblioteca.db')
elif MOTOR == 'mysql':
    conector = ConectorMySQL(host='localhost', usuario='root', clave='masterdba', base_datos='biblioteca')
else:
    raise ValueError(f"Motor no soportado: {MOTOR}")


def construir_capas():
    """Arma conexión → repositorios → servicios, para el motor elegido arriba.
    Ningún Service ni Repository sabe qué motor se está usando."""
    conexion = conector.obtener_conexion()
    crear_tablas(conexion)

    marcador = conector.marcador_parametro
    repositorio_libros = LibroRepository(conexion, marcador)
    repositorio_socios = SocioRepository(conexion, marcador)
    # PrestamoRepository necesita los otros dos repos para reconstruir la agregación
    repositorio_prestamos = PrestamoRepository(conexion, repositorio_libros, repositorio_socios, marcador)

    servicio_libros = LibroService(repositorio_libros)
    servicio_socios = SocioService(repositorio_socios)
    servicio_prestamos = PrestamoService(repositorio_prestamos, repositorio_socios, repositorio_libros)

    return conexion, servicio_libros, servicio_socios, servicio_prestamos


# ------------------------- Menú de Libros -------------------------

def menu_libros(servicio_libros):
    while True:
        print("\n--- LIBROS ---")
        print("1) Listar")
        print("2) Crear")
        print("3) Buscar por ISBN")
        print("4) Actualizar")
        print("5) Eliminar")
        print("6) Prestar (baja 1 copia disponible)")
        print("7) Devolver (sube 1 copia disponible)")
        print("0) Volver")
        opcion = input("Opción: ").strip()

        try:
            if opcion == '1':
                libros = servicio_libros.listar_libros()
                if not libros:
                    print("(no hay libros registrados)")
                for libro in libros:
                    print(f"  {libro.isbn} — {libro.titulo} ({libro.copias_disponibles} disponibles)")

            elif opcion == '2':
                isbn = input("ISBN: ").strip()
                titulo = input("Título: ").strip()
                copias = int(input("Copias disponibles: ").strip())
                if servicio_libros.registrar_libro(isbn, titulo, copias):
                    print("Libro creado.")

            elif opcion == '3':
                isbn = input("ISBN: ").strip()
                libro = servicio_libros.obtener_libro(isbn)
                print(libro if libro else "No existe un libro con ese ISBN.")

            elif opcion == '4':
                isbn = input("ISBN: ").strip()
                titulo = input("Nuevo título (enter para no cambiar): ").strip()
                copias = int(input("Nuevas copias disponibles: ").strip())
                if servicio_libros.actualizar_libro(isbn, titulo, copias):
                    print("Libro actualizado.")

            elif opcion == '5':
                isbn = input("ISBN: ").strip()
                if servicio_libros.eliminar_libro(isbn):
                    print("Libro eliminado.")

            elif opcion == '6':
                isbn = input("ISBN: ").strip()
                libro = servicio_libros.prestar_libro(isbn)
                print(f"Préstamo OK. Copias restantes: {libro.copias_disponibles}")

            elif opcion == '7':
                isbn = input("ISBN: ").strip()
                libro = servicio_libros.devolver_libro(isbn)
                print(f"Devolución OK. Copias disponibles: {libro.copias_disponibles}")

            elif opcion == '0':
                return

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Dato inválido: {error}")


# ------------------------- Menú de Socios -------------------------

def menu_socios(servicio_socios):
    while True:
        print("\n--- SOCIOS ---")
        print("1) Listar")
        print("2) Crear")
        print("3) Buscar por número")
        print("4) Actualizar")
        print("5) Eliminar")
        print("0) Volver")
        opcion = input("Opción: ").strip()

        try:
            if opcion == '1':
                socios = servicio_socios.listar_socios()
                if not socios:
                    print("(no hay socios registrados)")
                for socio in socios:
                    print(f"  {socio.numero_socio} — {socio.nombre}")

            elif opcion == '2':
                numero = int(input("Número de socio: ").strip())
                nombre = input("Nombre: ").strip()
                if servicio_socios.registrar_socio(numero, nombre):
                    print("Socio creado.")

            elif opcion == '3':
                numero = int(input("Número de socio: ").strip())
                socio = servicio_socios.obtener_socio(numero)
                print(socio if socio else "No existe un socio con ese número.")

            elif opcion == '4':
                numero = int(input("Número de socio: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                if servicio_socios.actualizar_socio(numero, nombre):
                    print("Socio actualizado.")

            elif opcion == '5':
                numero = int(input("Número de socio: ").strip())
                if servicio_socios.eliminar_socio(numero):
                    print("Socio eliminado.")

            elif opcion == '0':
                return

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Dato inválido: {error}")


# ------------------------- Menú de Préstamos (agregación Socio + Libro) -------------------------

def menu_prestamos(servicio_prestamos):
    while True:
        print("\n--- PRÉSTAMOS ---")
        print("1) Listar todos")
        print("2) Realizar préstamo")
        print("3) Registrar devolución")
        print("4) Historial de un socio")
        print("0) Volver")
        opcion = input("Opción: ").strip()

        try:
            if opcion == '1':
                prestamos = servicio_prestamos.listar_prestamos()
                if not prestamos:
                    print("(no hay préstamos registrados)")
                for prestamo in prestamos:
                    # Navegación directa por la agregación: prestamo.socio y prestamo.libro
                    # son objetos completos (no ids sueltos), así que se accede a sus
                    # propios atributos con punto, como cualquier objeto normal.
                    estado = "vigente" if prestamo.esta_vigente() else f"devuelto el {prestamo.fecha_devolucion}"
                    print(f"  Préstamo #{prestamo.id_prestamo}: {prestamo.socio.nombre} (socio #{prestamo.socio.numero_socio}) "
                          f"— \"{prestamo.libro.titulo}\" (ISBN {prestamo.libro.isbn}) · {estado}")

            elif opcion == '2':
                numero_socio = int(input("Número de socio: ").strip())
                isbn = input("ISBN del libro: ").strip()
                prestamo = servicio_prestamos.realizar_prestamo(numero_socio, isbn)
                # Mismo punto: apenas se crea, ya se puede navegar socio/libro sin volver a consultarlos.
                print(f"Préstamo #{prestamo.id_prestamo} registrado: "
                      f"{prestamo.socio.nombre} se llevó \"{prestamo.libro.titulo}\"")

            elif opcion == '3':
                id_prestamo = int(input("ID del préstamo: ").strip())
                prestamo = servicio_prestamos.registrar_devolucion(id_prestamo)
                print(f"Devolución registrada: {prestamo}")

            elif opcion == '4':
                numero_socio = int(input("Número de socio: ").strip())
                historial = servicio_prestamos.historial_de_socio(numero_socio)
                if not historial:
                    print("(este socio no tiene préstamos)")
                for prestamo in historial:
                    estado = "vigente" if prestamo.esta_vigente() else f"devuelto el {prestamo.fecha_devolucion}"
                    print(f"  #{prestamo.id_prestamo}: \"{prestamo.libro.titulo}\" · {estado}  "
                          f"(socio: {prestamo.socio.nombre})")

            elif opcion == '0':
                return

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"No se pudo completar: {error}")


def menu_principal():
    conexion, servicio_libros, servicio_socios, servicio_prestamos = construir_capas()
    print(f"Conectado con motor: {MOTOR}")

    try:
        while True:
            print("\n=== APLICACIÓN MANTENEDORA — Biblioteca ===")
            print("1) Gestionar Libros")
            print("2) Gestionar Socios")
            print("3) Gestionar Préstamos")
            print("0) Salir")
            opcion = input("Opción: ").strip()

            if opcion == '1':
                menu_libros(servicio_libros)
            elif opcion == '2':
                menu_socios(servicio_socios)
            elif opcion == '3':
                menu_prestamos(servicio_prestamos)
            elif opcion == '0':
                break
            else:
                print("Opción inválida.")
    finally:
        conexion.close()


if __name__ == '__main__':
    menu_principal()
