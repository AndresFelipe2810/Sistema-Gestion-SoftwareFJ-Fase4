# entidad.py
# Clase abstracta general del sistema Software FJ.
# Cliente, Servicio y Reserva heredan de esta clase.

from abc import ABC, abstractmethod


class EntidadBase(ABC):

    @abstractmethod
    def obtener_detalle(self) -> str:
        # Devuelve la informacion principal de la entidad.
        # Cada clase hija define su propio formato.
        pass

    def __str__(self) -> str:
        # print(entidad) muestra lo que devuelve obtener_detalle().
        return self.obtener_detalle()