# Ejemplo de herencia y sobreescritura de metodos

# Clase padre o super clase
class Persona:
    def __init__(self, nombre: str, rut: str):
        self.nombre = nombre
        self.rut = rut

    def saludar(self):
        return f"Hola, soy {self.nombre}"


# Las clases hijas que heredan de Persona
class Socio(Persona):
    def __init__(self, nombre, rut, numero_socio):
        # Llamado al constructor de la clase padre
        super().__init__(nombre, rut)
        # Este atributo es propio de la clase Socio
        # y se suma a los atributos de su clase padre Persona
        # Persona: nombre y rut
        self.numero_socio = numero_socio

    def saludar(self):
        base = super().saludar()   # reutiliza el saludo del padre: "Hola, Soy {nombre_persona}"
        return base + ", socio de la biblioteca"

class Bibliotecario(Persona):
    def __init__(self, nombre, rut, turno):
        super().__init__(nombre, rut)
        self.turno = turno

    def saludar(self):
        return super().saludar() + f", turno {self.turno}"

# Instanciar objeto desde la clase Socio
objeto_socio = Socio("Carlos Parado", "1-1", "1234")
objeto_socio.nombre = "Carlitos Prado" # accediendo al atributo de la clase padre
print(objeto_socio.saludar()) # Llamamos al saludo del socio, que internamente 
                              # llama al saludo de la Persona

# Instanciar objeto desde la clase Bibliotecario
objeto_bibliotecario = Bibliotecario("Juana Rojas", "1-2", "Tarde")
objeto_bibliotecario.nombre = "Maria Rojas"
print(objeto_bibliotecario.saludar()) # Llamamos al saludo del bibliotecario, que internamente 
                                      # llama al saludo de la Persona
