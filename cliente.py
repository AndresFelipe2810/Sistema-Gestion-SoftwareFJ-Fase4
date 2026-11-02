# Para la clase Cliente y sus validaciones
from excepciones import ClienteInvalidoError

class Cliente:
    def __init__(self, cedula, nombre, correo):
        self.set_cedula(cedula)
        self.set_nombre(nombre)
        self.set_correo(correo)

    def set_cedula(self, cedula):
        if not str(cedula).isdigit() or len(str(cedula)) < 7:
            raise ClienteInvalidoError(f"Cédula inválida: '{cedula}'. Debe contener solo números y al menos 7 dígitos.")
        self.__cedula = cedula

    def set_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: '{nombre}'. Demasiado corto o vacío.")
        self.__nombre = nombre.strip()

    def set_correo(self, correo):
        if "@" not in correo or "." not in correo:
            raise ClienteInvalidoError(f"Correo electrónico inválido: '{correo}'.")
        self.__correo = correo.strip()

    # Getters para acceder a los datos encapsulados
    @property
    def cedula(self):
        return self.__cedula

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def __str__(self):
        return f"Cliente: {self.__nombre} (Cédula: {self.__cedula}, Correo: {self.__correo})"