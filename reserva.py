# Clase Reserva: integra un cliente, un servicio, la duración y el estado.
#
# Ciclo de vida de una reserva:
#   PENDIENTE --confirmar()--> CONFIRMADA --procesar()--> PROCESADA
#   PENDIENTE o CONFIRMADA --cancelar()--> CANCELADA
#
# Convención de errores del grupo:
#   - Esta clase LANZA las excepciones (usando "raise ... from ..." para
#     conservar la causa original) y registra solo los eventos exitosos.
#   - El registro de errores con registrar_error() lo hace el bloque except
#     que maneja el error de forma definitiva (por ejemplo, en main.py).

from entidad import EntidadBase
from cliente import Cliente
from servicios import Servicio
from excepciones import (
    SoftwareFJError,
    ReservaError,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)
from logger import registrar_info, registrar_advertencia


class Reserva(EntidadBase):

    # Estados posibles de una reserva.
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    # Contador compartido por todas las reservas para asignar el número.
    _contador = 0

    def __init__(self, cliente, servicio, horas):
        # Se valida que los objetos recibidos sean del tipo correcto.
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un servicio válido.")

        # La duración la valida el propio servicio (polimorfismo): cada tipo
        # de servicio tiene sus reglas. Si falla, se encadena el error.
        try:
            horas_validas = servicio.validar_parametros(horas)
        except ParametroInvalidoError as error:
            raise ReservaError(
                f"No se pudo crear la reserva: duración inválida ({horas})."
            ) from error

        Reserva._contador = Reserva._contador + 1
        self.__numero = Reserva._contador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas_validas
        self.__estado = Reserva.PENDIENTE
        self.__costo_total = None

        registrar_info(
            f"Reserva #{self.__numero} creada: {cliente.nombre} - "
            f"{servicio.nombre} ({horas_validas} h).",
            origen="Reserva"
        )

    # Propiedades de solo lectura (encapsulación)

    @property
    def numero(self):
        return self.__numero

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def horas(self):
        return self.__horas

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        # Es None mientras la reserva no haya sido procesada.
        return self.__costo_total

    # Operaciones de la reserva

    def confirmar(self):
        # Solo se puede confirmar una reserva pendiente.
        if self.__estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.__numero}: "
                f"su estado es {self.__estado}."
            )
        try:
            self.__servicio.verificar_disponibilidad()
        except ServicioNoDisponibleError as error:
            raise ReservaError(
                f"No se pudo confirmar la reserva #{self.__numero}: "
                f"el servicio no está disponible."
            ) from error
        else:
            # Solo se ejecuta si el servicio estaba disponible.
            self.__estado = Reserva.CONFIRMADA
            registrar_info(
                f"Reserva #{self.__numero} confirmada.", origen="Reserva"
            )

    def cancelar(self, motivo="Sin motivo indicado"):
        # No se puede cancelar una reserva ya cancelada ni una ya procesada.
        if self.__estado == Reserva.CANCELADA or self.__estado == Reserva.PROCESADA:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva #{self.__numero}: "
                f"su estado es {self.__estado}."
            )
        self.__estado = Reserva.CANCELADA
        registrar_advertencia(
            f"Reserva #{self.__numero} cancelada. Motivo: {motivo}.",
            origen="Reserva"
        )

    def procesar(self, impuesto=0.0, descuento=0.0):
        # Método con parámetros opcionales (sobrecarga):
        #   reserva.procesar()              -> costo base
        #   reserva.procesar(0.19)          -> con impuesto
        #   reserva.procesar(0.19, 0.10)    -> con impuesto y descuento
        # Solo se puede procesar una reserva confirmada.
        if self.__estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"No se puede procesar la reserva #{self.__numero}: "
                f"debe estar CONFIRMADA y su estado es {self.__estado}."
            )
        try:
            total = self.__servicio.calcular_costo_total(
                self.__horas, impuesto, descuento
            )
        except SoftwareFJError as error:
            # Se convierte en un error de reserva conservando la causa.
            raise ReservaError(
                f"No se pudo procesar la reserva #{self.__numero}."
            ) from error
        else:
            # Solo se ejecuta si el cálculo fue exitoso.
            self.__costo_total = total
            self.__estado = Reserva.PROCESADA
            registrar_info(
                f"Reserva #{self.__numero} procesada. Costo total: {total}.",
                origen="Reserva"
            )
            return total
        finally:
            # Se ejecuta siempre, haya o no error.
            registrar_info(
                f"Fin del procesamiento de la reserva #{self.__numero}.",
                origen="Reserva"
            )

    def obtener_detalle(self) -> str:
        # Implementa el método abstracto de EntidadBase.
        detalle = (
            f"Reserva #{self.__numero} | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | {self.__horas} h | "
            f"Estado: {self.__estado}"
        )
        if self.__costo_total is not None:
            detalle = detalle + f" | Costo total: ${self.__costo_total:,.2f}"
        return detalle
