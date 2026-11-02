# Excepciones personalizadas del sistema.

from logger import registrar_error

class SoftwareFJError(Exception):
    # Clase base para todas las excepciones personalizadas de Software FJ.
    def __init__(self, mensaje="Ha ocurrido un error en el sistema Software FJ"):
        super().__init__(mensaje)
        # Se registra el error en sistema.log usando el módulo centralizado.
        # El origen permite saber qué clase generó el error.
        registrar_error(
            f"{self.__class__.__name__}: {mensaje}",
            origen=self.__class__.__name__
        )


class ClienteInvalidoError(SoftwareFJError):
    # Excepción lanzada cuando los datos de un cliente no son válidos
    pass


class ReservaError(SoftwareFJError):
    # Excepción lanzada cuando falla una operación de reserva
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    # Excepción lanzada cuando un servicio solicitado no está disponible
    pass


class ParametroInvalidoError(SoftwareFJError):
    # Excepción lanzada cuando un parámetro recibido no es válido.
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    # Excepción lanzada cuando una operación no está permitida según el estado del objeto
    pass


class CalculoInconsistenteError(SoftwareFJError):
    # Excepción lanzada cuando un cálculo de costos produce un resultado inconsistente
    pass