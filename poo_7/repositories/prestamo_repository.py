# repositories/prestamo_repository.py
from models.prestamo import Prestamo


class PrestamoRepository:
    """
    Persiste la AGREGACIÓN Prestamo -> (Socio, Libro) guardando solo las LLAVES
    (numero_socio, isbn), nunca los datos completos del Socio o el Libro. Esos
    datos ya viven, cada uno, en su propia tabla.

    Por eso este Repository necesita, además de la conexión, los otros dos
    Repository (Libro y Socio) inyectados: los usa para RECONSTRUIR el objeto
    Prestamo completo a partir de una fila con solo dos llaves foráneas.
    """

    def __init__(self, conexion, libro_repository, socio_repository, marcador='?'):
        self.conexion = conexion                    # inyectada, no se crea aquí
        self.libro_repository = libro_repository    # para reconstruir el Libro agregado
        self.socio_repository = socio_repository    # para reconstruir el Socio agregado
        self.marcador = marcador

    def crear(self, prestamo):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(
            f"INSERT INTO prestamos (numero_socio, isbn, fecha_prestamo, fecha_devolucion) "
            f"VALUES ({m}, {m}, {m}, {m})",
            (prestamo.socio.numero_socio, prestamo.libro.isbn,
             prestamo.fecha_prestamo, prestamo.fecha_devolucion)
        )
        self.conexion.commit()
        prestamo.id_prestamo = cursor.lastrowid   # la BD asigna el id, se lo devolvemos al objeto
        return True

    def buscar_por_id(self, id_prestamo):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT * FROM prestamos WHERE id_prestamo = {m}", (id_prestamo,))
        fila = cursor.fetchone()
        if fila is None:
            return None
        return self._reconstruir(fila)

    def listar_por_socio(self, numero_socio):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(
            f"SELECT * FROM prestamos WHERE numero_socio = {m} ORDER BY fecha_prestamo",
            (numero_socio,)
        )
        return [self._reconstruir(fila) for fila in cursor.fetchall()]

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM prestamos ORDER BY fecha_prestamo")
        return [self._reconstruir(fila) for fila in cursor.fetchall()]

    def registrar_devolucion(self, id_prestamo, fecha_devolucion):
        m = self.marcador
        cursor = self.conexion.cursor()
        cursor.execute(
            f"UPDATE prestamos SET fecha_devolucion = {m} WHERE id_prestamo = {m}",
            (fecha_devolucion, id_prestamo)
        )
        self.conexion.commit()
        return cursor.rowcount > 0

    def _reconstruir(self, fila):
        # fila: (id_prestamo, numero_socio, isbn, fecha_prestamo, fecha_devolucion)
        id_prestamo, numero_socio, isbn, fecha_prestamo, fecha_devolucion = fila
        # Aquí se ve la agregación en el Repository: se pide prestado (nunca se
        # copia) el Socio y el Libro ya existentes a SUS PROPIOS repositorios.
        socio = self.socio_repository.buscar_por_numero(numero_socio)
        libro = self.libro_repository.buscar_por_isbn(isbn)
        return Prestamo(id_prestamo, socio, libro, fecha_prestamo, fecha_devolucion)
