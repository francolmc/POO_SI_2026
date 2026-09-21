class Prestamo:
    """
    RELACIÓN DE AGREGACIÓN (todo-parte débil): un Prestamo tiene un Socio y un
    Libro, pero NO es dueño de su ciclo de vida.

    Si se elimina un Prestamo, el Socio y el Libro siguen existiendo tranquilamente
    en sus propias tablas — ya existían antes del préstamo y van a seguir existiendo
    después. Por eso Prestamo nunca los crea: los RECIBE ya construidos.

    (Si fuera composición, Prestamo tendría que crear sus propias partes y
    destruirlas junto con él — como una Persona y su Corazon.)
    """

    def __init__(self, id_prestamo, socio, libro, fecha_prestamo: str, fecha_devolucion: str = None):
        self.id_prestamo = id_prestamo
        self.socio = socio            # objeto Socio agregado: la MISMA instancia que ya vive en 'socios'
        self.libro = libro            # objeto Libro agregado: la MISMA instancia que ya vive en 'libros'
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def esta_vigente(self):
        return self.fecha_devolucion is None

    # Nótese: ni una línea de SQL aquí, igual que en Libro y Socio.

    def __repr__(self):
        estado = "vigente" if self.esta_vigente() else f"devuelto el {self.fecha_devolucion}"
        return (f"Prestamo(id={self.id_prestamo}, socio={self.socio.nombre!r}, "
                f"libro={self.libro.titulo!r}, {estado})")
