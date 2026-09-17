from abc import ABC, abstractmethod

class Conector(ABC):
    """
    Contrato: cualquier motor de base de datos
    debe saber entregar una conexion
    """

    @abstractmethod
    def obtener_conexion(self):
        pass
