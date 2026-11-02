# Para las excepciones personalizadas y el registro de logs

import datetime

class SoftwareFJError(Exception):
    """Clase base para todas las excepciones personalizadas de Software FJ."""
    def __init__(self, mensaje="Ha ocurrido un error en el sistema Software FJ"):
        super().__init__(mensaje)
        self.registrar_log(mensaje)

    def registrar_log(self, mensaje):
        """Registra el evento o error en un archivo de texto (logs)."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("sistema.log", "a", encoding="utf-8") as archivo:
            archivo.write(f"[{timestamp}] ERROR: {mensaje}\n")


class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos de un cliente no son válidos."""
    pass


class ReservaError(SoftwareFJError):
    """Excepción lanzada cuando falla una operación de reserva."""
    pass