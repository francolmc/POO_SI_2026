import sqlite3
from models.personaje import Personaje

MSG_DB_ERROR = "No se puede leer la base de datos."

class BaseDatoError(Exception):
    pass


class PersonajeRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def guardar_muchos(self, personajes):
        filas = [(p.id_api, p.nombre, p.estado, p.especie, p.origen) 
                 for p in personajes]

        try:
            self.conexion.executemany(
                "INSERT OR REPLACE INTO personajes"
                "(id_api, nombre, estado, especie, origen)"
                "VALUES (?, ?, ?, ?, ?)",
                filas,
            )
            self.conexion.commit()
        except sqlite3.Error:
            raise BaseDatoError(MSG_DB_ERROR) from None

    def listar(self):
        return self._consultar(
            "SELECT id_api, nombre, estado, especie, origen"
            "FROM personajes"
            "ORDER BY nombre"
        )

    def buscar_por_nombre(self, nombre):
        return self._consultar(
            "SELECT id_api, nombre, estado, especie, origen"
            "FROM personajes"
            "WHERE nombre LIKE ?",
            (nombre,)
        )

    def contar(self):
        try:
            return self.conexion.execute(
                "SELECT COUNT(*) FROM personajes"
            ).fetchone()[0]
        except sqlite3.Error:
            raise BaseDatoError(MSG_DB_ERROR) from None

    def _consultar(self, sql, params=()): # DRY
        try:
            filas = self.conexion.execute(sql, params).fetchall()
        except sqlite3.Error:
            raise BaseDatoError(MSG_DB_ERROR) from None
        return [Personaje(*fila) for fila in filas]