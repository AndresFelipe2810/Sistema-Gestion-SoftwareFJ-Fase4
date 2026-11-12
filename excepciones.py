# excepciones.py
# Excepciones personalizadas del sistema Software FJ.
# El registro en sistema.log se hace en los bloques except, no al crear la excepción.


class SoftwareFJError(Exception):
    # Clase base para todas las excepciones del sistema.
    def __init__(self, mensaje="Ha ocurrido un error en el sistema Software FJ"):
        super().__init__(mensaje)


class ClienteInvalidoError(SoftwareFJError):
    # Datos inválidos de un cliente.
    pass


class ReservaError(SoftwareFJError):
    # Falla en una operación de reserva.
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    # Servicio solicitado no disponible.
    pass


class ParametroInvalidoError(SoftwareFJError):
    # Parámetro recibido no válido.
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    # Operación no permitida según el estado del objeto.
    pass


class CalculoInconsistenteError(SoftwareFJError):
    # Cálculo de costos con resultado inconsistente.
    pass