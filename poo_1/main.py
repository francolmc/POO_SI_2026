class Persona:
    def __init__(self, nombre: str):
        # Definicion de atributos
        self.nombre = nombre
        self.__email = None

    def saludar(self):
        print(f"Hola, soy {self.nombre}")

    def asignar_email(self, email: str):
        if "@" not in email:
            raise ValueError("Error: el email ingresado no es valido")
        else:
            self.__email = email

    def obtener_email(self) -> str:
        return self.__email

# Crear un objeto (instanciar)
carlos = Persona("Carlos Prado")
carlos.asignar_email("carlos@sucorreo.com")
carlos.saludar()
print(f"Mi correo es: {carlos.obtener_email()}")

