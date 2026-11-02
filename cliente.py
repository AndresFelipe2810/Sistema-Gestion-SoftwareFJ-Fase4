# Clase Cliente con encapsulación, validaciones robustas y registro de eventos.

import re

from excepciones import ClienteInvalidoError
from logger import registrar_info

# Patrón de correo: usuario + @ + dominio + extensión de al menos 2 letras.
# Evita aceptar casos como "a@b." o "correo@".
PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class Cliente:

    def __init__(self, cedula, nombre, correo):
        # Se valida y asigna cada dato por separado usando los setters.
        self.set_cedula(cedula)
        self.set_nombre(nombre)
        self.set_correo(correo)
        # Si llegó hasta aquí, los tres datos son válidos: se registra el evento INFO.
        registrar_info(
            f"Cliente creado correctamente: {self.__cedula} - {self.__nombre}",
            origen="Cliente"
        )

    def set_cedula(self, cedula):
        # Se convierte a texto y se quitan espacios antes de validar.
        cedula_txt = str(cedula).strip()
        # Debe tener solo dígitos y al menos 7 caracteres.
        if not cedula_txt.isdigit() or len(cedula_txt) < 7:
            raise ClienteInvalidoError(
                f"Cédula inválida: '{cedula}'. Debe contener solo números y al menos 7 dígitos."
            )
        self.__cedula = cedula_txt

    def set_nombre(self, nombre):
        # Se convierte a texto y se quitan espacios.
        nombre_txt = str(nombre).strip()
        # Debe tener al menos 3 caracteres y contener al menos una letra.
        if len(nombre_txt) < 3 or not any(c.isalpha() for c in nombre_txt):
            raise ClienteInvalidoError(
                f"Nombre inválido: '{nombre}'. Debe tener al menos 3 caracteres y contener letras."
            )
        self.__nombre = nombre_txt

    def set_correo(self, correo):
        # Se convierte a texto y se quitan espacios.
        correo_txt = str(correo).strip()
        # Se valida contra el patrón definido arriba.
        if not PATRON_CORREO.match(correo_txt):
            raise ClienteInvalidoError(
                f"Correo electrónico inválido: '{correo}'."
            )
        self.__correo = correo_txt

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