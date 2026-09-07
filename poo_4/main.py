# Generar una clase invetario que pueda recibir items o agregar items
# donde contenga un metodo que muestre los que los items hacen.
# Considerar una clase Item y sub-clases a partir de ella,
# como por ejemplo: Arma, Pocion, Armadura, etc.

from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, descripcion: str, nivel: int):
        super().__init__()
        self.descripcion = descripcion
        self.nivel = nivel

    @abstractmethod
    def mostrar(self):
        pass

class Arma(Item):
    def __init__(self, descripcion, nivel):
        super().__init__(descripcion, nivel)

    def mostrar(self):
        return f"Soy un Arma, especificamente: {self.descripcion}"

class Pocion(Item):
    def __init__(self, descripcion, nivel):
        super().__init__(descripcion, nivel)

    def mostrar(self):
        return f"Soy una Poción, especificamente: {self.descripcion}"

class Armadura(Item):
    def __init__(self, descripcion, nivel):
        super().__init__(descripcion, nivel)

    def mostrar(self):
        return f"Soy una Armadura, especificamente: {self.descripcion}"


class Invetario:
    def __init__(self):
        self.__lista_items = []

    def agregar_item(self, item: Item):
        self.__lista_items.append(item)

    def mostrar_contenido(self) -> list:
        return self.__lista_items


mi_invetario = Invetario()
armadura = Armadura("Armadura nivel 2", 100)
pocion = Pocion("Pocion nivel 2 para restar el 50%", 50)
arma = Arma("Arma nivel 4, nivel de daño 25%", 25)

mi_invetario.agregar_item(armadura)
mi_invetario.agregar_item(pocion)
mi_invetario.agregar_item(arma)

for i in mi_invetario.mostrar_contenido():
    print(i.mostrar())