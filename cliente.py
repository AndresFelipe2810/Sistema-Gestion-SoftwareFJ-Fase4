# cliente.py
# Clase Cliente con encapsulación, validaciones robustas y registro de eventos.

import re

from entidad import EntidadBase
from excepciones import ClienteInvalidoError
from logger import registrar_info

# Patrón de correo: usuario + @ + dominio + extensión de al menos 2 letras.
PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class Cliente(EntidadBase):

    def __init__(self, cedula, nombre, correo):
        # Cada asignación pasa por el setter de la propiedad correspondiente.
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        # Si llegó hasta aquí, los tres datos son válidos: se registra el evento INFO.
        registrar_info(
            f"Cliente creado correctamente: {self.cedula} - {self.nombre}",
            origen="Cliente"
        )

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        if valor is None:
            raise ClienteInvalidoError("Cédula inválida: no puede ser None.")
        cedula_txt = str(valor).strip()
        if not cedula_txt.isdigit() or len(cedula_txt) < 7:
            raise ClienteInvalidoError(
                f"Cédula inválida: '{valor}'. Debe contener solo números y al menos 7 dígitos."
            )
        self.__cedula = cedula_txt

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None:
            raise ClienteInvalidoError("Nombre inválido: no puede ser None.")
        nombre_txt = str(valor).strip()
        if len(nombre_txt) < 3 or not any(c.isalpha() for c in nombre_txt):
            raise ClienteInvalidoError(
                f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres y contener letras."
            )
        self.__nombre = nombre_txt

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None:
            raise ClienteInvalidoError("Correo electrónico inválido: no puede ser None.")
        correo_txt = str(valor).strip()
        if not PATRON_CORREO.match(correo_txt):
            raise ClienteInvalidoError(
                f"Correo electrónico inválido: '{valor}'."
            )
        self.__correo = correo_txt

    def obtener_detalle(self) -> str:
        return f"Cliente: {self.nombre} (Cédula: {self.cedula}, Correo: {self.correo})"