# Guía rápida para el equipo - Software FJ

## Archivos en el repositorio

- entidad.py: clase abstracta general EntidadBase(ABC).
- logger.py: registra eventos y errores en sistema.log.
- excepciones.py: contiene las excepciones del sistema.
- cliente.py: clase Cliente con encapsulación y validaciones.
- test_cliente.py: pruebas de cliente y manejo de excepciones.
- README.md: estado del proyecto.

## Herencia obligatoria

Todas las entidades del sistema deben heredar de EntidadBase e implementar obtener_detalle().

Ejemplo:

    from entidad import EntidadBase

    class Cliente(EntidadBase):
        def obtener_detalle(self) -> str:
            return f"Cliente: {self.nombre}"

Si una clase hija no implementa obtener_detalle(), Python lanza TypeError al instanciarla.

Aplica para Cliente, Servicio y Reserva.

## Cómo registrar eventos y errores

Usar logger.py. 

    from logger import registrar_info, registrar_error

    registrar_info("Cliente creado correctamente", origen="Cliente")
    registrar_error("Intento de reserva inválido", origen="Reserva")

Niveles disponibles: INFO, WARNING, ERROR, CRITICAL.

El parámetro origen es el módulo donde ocurrió el evento, no el tipo de excepción.
Ejemplo correcto: origen="Reserva". Ejemplo incorrecto: origen="ReservaError".

## Excepciones disponibles

- ClienteInvalidoError
- ReservaError
- ServicioNoDisponibleError
- ParametroInvalidoError
- OperacionNoPermitidaError
- CalculoInconsistenteError

Todas heredan de SoftwareFJError.

Importante: las excepciones NO registran el error solas. El registro se hace en el bloque except.

Forma correcta:

    from excepciones import ParametroInvalidoError
    from logger import registrar_error

    try:
        reserva = Reserva(cliente, servicio, duracion=0)
    except ParametroInvalidoError as e:
        registrar_error(str(e), origen="Reserva")

Forma incorrecta: crear la excepción y esperar que se registre sola.

## Cómo lanzar una excepción

    from excepciones import ParametroInvalidoError

    if duracion <= 0:
        raise ParametroInvalidoError("La duración debe ser mayor que cero.")

No crear excepciones nuevas. Usar las que ya están definidas.

## Estilo de las clases (ejemplo: Cliente)

- Atributos privados con doble guion bajo: self.__cedula.
- Encapsulación con @property y @atributo.setter.
- Validar dentro del setter antes de guardar.
- Usar strip() en datos de texto.
- Lanzar excepción específica si el dato es inválido.
- Implementar obtener_detalle() para cumplir el contrato de EntidadBase.
- Registrar INFO en el __init__ cuando el objeto se crea correctamente.

## Cómo probar

Ejecutar:

    python test_cliente.py

Revisar sistema.log. Deben aparecer líneas INFO (operaciones exitosas) y ERROR (excepciones capturadas en los except).

