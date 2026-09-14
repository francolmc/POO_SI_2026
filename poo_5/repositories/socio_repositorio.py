import sqlite3
from models.socio import Socio

class SocioRepository:
    def __init__(self, conexion):
        self.conexion = conexion    # inyectada, no se crea aquí

    def crear(self, socio):
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT INTO socios VALUES (?, ?)",
            (socio.numero_socio, socio.nombre)
        )
        self.conexion.commit()

    def buscar_por_numero(self, numero_socio):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                "SELECT * FROM socios WHERE numero_socio = ?", (numero_socio,)
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Socio(numero_socio=fila[0], nombre=fila[1])
        except sqlite3.Error as error:
            print(f"Error de base de datos: {error}")
            return None

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM socios")
        filas = cursor.fetchall()

        socios = []
        for fila in filas:
            socios.append(Socio(numero_socio=fila[0], nombre=fila[1]))
        return socios