# servicios.py
# Módulo de servicios de Software FJ.
#
# Contiene:
#   - Servicio: clase abstracta que hereda de EntidadBase.
#   - ReservaSala, AlquilerEquipo, AsesoriaEspecializada: servicios concretos.

import math
from abc import abstractmethod

from entidad import EntidadBase
from excepciones import (
    SoftwareFJError,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)
from logger import registrar_info


# Funciones auxiliares de validación

def _convertir_a_numero(valor, nombre_campo):
    # Convierte un valor a float y verifica que sea un número real válido.
    if valor is None:
        raise ParametroInvalidoError(f"{nombre_campo} no puede ser None.")
    # bool es subclase de int en Python, así que se rechaza de forma explícita.
    if isinstance(valor, bool):
        raise ParametroInvalidoError(f"{nombre_campo} no puede ser un booleano.")
    try:
        numero = float(valor)
    except (TypeError, ValueError) as error:
        # Encadenamiento: se conserva el error original como causa.
        raise ParametroInvalidoError(
            f"{nombre_campo} debe ser numérico, se recibió '{valor}'."
        ) from error
    if not math.isfinite(numero):
        raise ParametroInvalidoError(f"{nombre_campo} debe ser un número finito.")
    return numero


def _validar_horas(horas, minimo, maximo):
    # Verifica que la duración esté dentro del rango permitido por el servicio.
    horas_num = _convertir_a_numero(horas, "La duración (horas)")
    if horas_num < minimo or horas_num > maximo:
        raise ParametroInvalidoError(
            f"La duración debe estar entre {minimo} y {maximo} horas, "
            f"se recibió {horas_num}."
        )
    return horas_num


def _validar_porcentaje(valor, nombre_campo):
    # El impuesto y el descuento se expresan como fracción: 0.19 equivale a 19 %.
    numero = _convertir_a_numero(valor, nombre_campo)
    if numero < 0 or numero > 1:
        raise ParametroInvalidoError(
            f"{nombre_campo} debe estar entre 0 y 1 (por ejemplo 0.19 para 19 %), "
            f"se recibió {numero}."
        )
    return numero


def _validar_entero(valor, nombre_campo, minimo, maximo):
    # Verifica que el valor sea un número entero dentro de un rango.
    numero = _convertir_a_numero(valor, nombre_campo)
    if not numero.is_integer():
        raise ParametroInvalidoError(
            f"{nombre_campo} debe ser un número entero, se recibió {valor}."
        )
    entero = int(numero)
    if entero < minimo or entero > maximo:
        raise ParametroInvalidoError(
            f"{nombre_campo} debe estar entre {minimo} y {maximo}, se recibió {entero}."
        )
    return entero


def _validar_texto(valor, nombre_campo, largo_minimo=3):
    # Verifica que el texto no sea None y tenga un largo mínimo.
    if valor is None:
        raise ParametroInvalidoError(f"{nombre_campo} no puede ser None.")
    texto = str(valor).strip()
    if len(texto) < largo_minimo:
        raise ParametroInvalidoError(
            f"{nombre_campo} debe tener al menos {largo_minimo} caracteres."
        )
    return texto


# Clase abstracta Servicio

class Servicio(EntidadBase):
    # Clase abstracta: no se puede instanciar directamente.
    # Cada servicio concreto debe implementar calcular_costo, describir
    # y validar_parametros (métodos abstractos).

    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        # Cada asignación pasa por el setter de su propiedad (validación).
        self.codigo = codigo
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible
        registrar_info(
            f"Servicio creado correctamente: {self.codigo} - {self.nombre}",
            origen="Servicio"
        )

    # Propiedades (encapsulación)

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        self.__codigo = _validar_texto(valor, "El código del servicio", 2)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = _validar_texto(valor, "El nombre del servicio", 3)

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):
        tarifa = _convertir_a_numero(valor, "La tarifa base")
        if tarifa <= 0:
            raise ParametroInvalidoError(
                f"La tarifa base debe ser mayor que cero, se recibió {tarifa}."
            )
        self.__tarifa_base = tarifa

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ParametroInvalidoError(
                "La disponibilidad debe ser True o False."
            )
        self.__disponible = valor

    # Métodos abstractos (cada servicio los sobrescribe)

    @abstractmethod
    def calcular_costo(self, horas):
        # Devuelve el costo base (sin impuesto ni descuento) para esa duración.
        pass

    @abstractmethod
    def describir(self) -> str:
        # Devuelve una descripción del servicio con sus datos propios.
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        # Valida la duración según las reglas del servicio y devuelve las
        # horas como número. Lanza ParametroInvalidoError si no son válidas.
        pass

    # Métodos concretos

    def obtener_detalle(self) -> str:
        # Implementa el método abstracto de EntidadBase.
        return self.describir()

    def verificar_disponibilidad(self):
        # Lanza ServicioNoDisponibleError si el servicio no se puede usar.
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.codigo} - {self.nombre} no está disponible."
            )

    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0):
        # Método con comportamiento sobrecargado mediante parámetros opcionales.
        # Variantes de uso:
        #   servicio.calcular_costo_total(3)              -> solo el costo base
        #   servicio.calcular_costo_total(3, 0.19)        -> con impuesto del 19 %
        #   servicio.calcular_costo_total(3, 0.19, 0.10)  -> con impuesto y 10 % de descuento
        #   servicio.calcular_costo_total(3, descuento=0.10) -> solo con descuento
        try:
            self.verificar_disponibilidad()
            horas_validas = self.validar_parametros(horas)
            tasa_impuesto = _validar_porcentaje(impuesto, "El impuesto")
            tasa_descuento = _validar_porcentaje(descuento, "El descuento")

            costo_base = self.calcular_costo(horas_validas)
            total = costo_base * (1 - tasa_descuento) * (1 + tasa_impuesto)

            # Verificación de consistencia del resultado.
            if total <= 0:
                raise CalculoInconsistenteError(
                    f"El costo calculado es {total}, un valor inconsistente."
                )
        except SoftwareFJError:
            # Los errores propios del sistema se dejan pasar sin cambios:
            # quien llama los maneja y los registra en el log.
            raise
        except Exception as error:
            # Cualquier error inesperado (por ejemplo, de cálculo) se convierte
            # en una excepción del sistema, conservando la causa original.
            raise CalculoInconsistenteError(
                f"Error inesperado al calcular el costo de {self.codigo}."
            ) from error
        else:
            # Solo se ejecuta si el cálculo terminó sin errores.
            registrar_info(
                f"Costo calculado para {self.codigo}: {round(total, 2)}",
                origen="Servicio"
            )
            return round(total, 2)
        finally:
            # Se ejecuta siempre, haya o no error.
            registrar_info(
                f"Fin del intento de cálculo de costo del servicio {self.codigo}.",
                origen="Servicio"
            )


# Servicio 1: Reserva de salas

class ReservaSala(Servicio):
    # Salas con tarifa por hora. Las salas grandes tienen un recargo.

    HORAS_MINIMAS = 1
    HORAS_MAXIMAS = 12
    CAPACIDAD_GRANDE = 20     # desde esta capacidad se aplica el recargo
    RECARGO_SALA_GRANDE = 0.15

    def __init__(self, codigo, nombre, tarifa_base, capacidad, disponible=True):
        # Se valida lo propio antes de crear la parte común del servicio.
        self.capacidad = capacidad
        super().__init__(codigo, nombre, tarifa_base, disponible)

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        self.__capacidad = _validar_entero(valor, "La capacidad de la sala", 1, 200)

    def validar_parametros(self, horas):
        return _validar_horas(horas, self.HORAS_MINIMAS, self.HORAS_MAXIMAS)

    def calcular_costo(self, horas):
        costo = self.tarifa_base * horas
        if self.capacidad >= self.CAPACIDAD_GRANDE:
            costo = costo * (1 + self.RECARGO_SALA_GRANDE)
        return costo

    def describir(self) -> str:
        return (
            f"Sala {self.nombre} ({self.codigo}) - capacidad {self.capacidad} personas - "
            f"${self.tarifa_base:,.2f} por hora"
        )


# Servicio 2: Alquiler de equipos

class AlquilerEquipo(Servicio):
    # Alquiler de equipos: el costo depende de las horas y de las unidades.

    HORAS_MINIMAS = 1
    HORAS_MAXIMAS = 72

    def __init__(self, codigo, nombre, tarifa_base, tipo_equipo, unidades=1,
                disponible=True):
        self.tipo_equipo = tipo_equipo
        self.unidades = unidades
        super().__init__(codigo, nombre, tarifa_base, disponible)

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        self.__tipo_equipo = _validar_texto(valor, "El tipo de equipo", 3)

    @property
    def unidades(self):
        return self.__unidades

    @unidades.setter
    def unidades(self, valor):
        self.__unidades = _validar_entero(valor, "Las unidades del equipo", 1, 50)

    def validar_parametros(self, horas):
        return _validar_horas(horas, self.HORAS_MINIMAS, self.HORAS_MAXIMAS)

    def calcular_costo(self, horas):
        return self.tarifa_base * horas * self.unidades

    def describir(self) -> str:
        return (
            f"Alquiler de {self.tipo_equipo} ({self.codigo}) - {self.unidades} unidad(es) - "
            f"${self.tarifa_base:,.2f} por hora por unidad"
        )


# Servicio 3: Asesorías especializadas

class AsesoriaEspecializada(Servicio):
    # Asesorías: el costo depende del nivel del asesor.

    HORAS_MINIMAS = 1
    HORAS_MAXIMAS = 8
    # Factor que multiplica la tarifa según el nivel del asesor.
    FACTORES_NIVEL = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, codigo, nombre, tarifa_base, especialidad, nivel="junior",
                disponible=True):
        self.especialidad = especialidad
        self.nivel = nivel
        super().__init__(codigo, nombre, tarifa_base, disponible)

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, valor):
        self.__especialidad = _validar_texto(valor, "La especialidad", 3)

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, valor):
        if valor is None:
            raise ParametroInvalidoError("El nivel del asesor no puede ser None.")
        nivel_txt = str(valor).strip().lower()
        if nivel_txt not in self.FACTORES_NIVEL:
            # Se arma la lista de niveles permitidos con un bucle explícito.
            permitidos = ""
            for nombre_nivel in self.FACTORES_NIVEL:
                if permitidos != "":
                    permitidos = permitidos + ", "
                permitidos = permitidos + nombre_nivel
            raise ParametroInvalidoError(
                f"Nivel '{valor}' no válido. Niveles permitidos: {permitidos}."
            )
        self.__nivel = nivel_txt

    def validar_parametros(self, horas):
        return _validar_horas(horas, self.HORAS_MINIMAS, self.HORAS_MAXIMAS)

    def calcular_costo(self, horas):
        factor = self.FACTORES_NIVEL[self.nivel]
        return self.tarifa_base * horas * factor

    def describir(self) -> str:
        return (
            f"Asesoría de {self.especialidad} ({self.codigo}) - nivel {self.nivel} - "
            f"${self.tarifa_base:,.2f} por hora"
        )


# Prueba rápida del módulo (solo se ejecuta con: python servicios.py)

if __name__ == "__main__":
    from logger import registrar_error

    # Lista de intentos: cada elemento es (descripción, función a ejecutar).
    # Se usan funciones lambda para que los errores ocurran dentro del try.
    intentos = [
        ("Sala válida, 3 horas",
        lambda: ReservaSala("S01", "Sala Magdalena", 50000, 10).calcular_costo_total(3)),
        ("Sala grande con impuesto y descuento",
        lambda: ReservaSala("S02", "Auditorio", 80000, 40).calcular_costo_total(2, 0.19, 0.10)),
        ("Equipo válido, 5 horas, 2 unidades",
        lambda: AlquilerEquipo("E01", "Video Beam", 15000, "videoproyector", 2).calcular_costo_total(5, 0.19)),
        ("Asesoría senior, 2 horas",
        lambda: AsesoriaEspecializada("A01", "Asesoría Python", 70000, "Python", "senior").calcular_costo_total(2)),
        ("Sala con duración inválida (30 horas)",
        lambda: ReservaSala("S03", "Sala Tayrona", 50000, 10).calcular_costo_total(30)),
        ("Equipo con tarifa negativa",
        lambda: AlquilerEquipo("E02", "Portátil", -100, "computador", 1)),
        ("Asesoría con nivel inexistente",
        lambda: AsesoriaEspecializada("A02", "Asesoría Datos", 60000, "Datos", "maestro")),
        ("Servicio no disponible",
        lambda: ReservaSala("S04", "Sala Sierra", 50000, 10, disponible=False).calcular_costo_total(2)),
        ("Impuesto con texto inválido",
        lambda: ReservaSala("S05", "Sala Rodadero", 50000, 10).calcular_costo_total(2, "abc")),
        ("Descuento del 100 % (costo inconsistente)",
        lambda: ReservaSala("S06", "Sala Bahía", 50000, 10).calcular_costo_total(2, 0.0, 1.0)),
    ]

    numero = 1
    for descripcion, accion in intentos:
        try:
            resultado = accion()
        except SoftwareFJError as error:
            # Aquí se maneja el error de forma definitiva, así que aquí se registra.
            registrar_error(f"{descripcion}: {error}", origen="PruebaServicios")
            causa = ""
            if error.__cause__ is not None:
                causa = f" (causa: {type(error.__cause__).__name__})"
            print(f"{numero:02d}. ERROR  {descripcion}: {error}{causa}")
        else:
            print(f"{numero:02d}. OK     {descripcion}: {resultado}")
        numero = numero + 1

    # Un Servicio abstracto no se puede instanciar.
    try:
        Servicio("X01", "Servicio genérico", 1000)
    except TypeError as error:
        print(f"Servicio abstracto no instanciable: {error}")