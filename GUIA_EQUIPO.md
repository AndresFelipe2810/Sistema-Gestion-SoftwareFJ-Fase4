
## Archivos que dejé listos

- logger.py: registra eventos y errores en sistema.log.
- excepciones.py: contiene las excepciones del sistema.
- cliente.py: clase Cliente con encapsulación y validaciones.
- test_cliente.py: pruebas de Cliente y manejo de excepciones.
- README.md: estado del proyecto.

## Cómo registrar eventos y errores

Usar logger.py. No abrir sistema.log directamente.
```
from logger import registrar_info, registrar_error
registrar_info("Cliente creado correctamente", origen="Cliente")
registrar_error("Intento de reserva inválido", origen="Reserva")
```
Niveles disponibles: INFO, WARNING, ERROR, CRITICAL.

## Excepciones disponibles

- ClienteInvalidoError
- ReservaError
- ServicioNoDisponibleError
- ParametroInvalidoError
- OperacionNoPermitidaError
- CalculoInconsistenteError

Todas heredan de SoftwareFJError y registran el error automáticamente.

## Cómo lanzar una excepción
```
from excepciones import ParametroInvalidoError

if duracion <= 0:
    raise ParametroInvalidoError("La duración debe ser mayor que cero.")
```

## Ejemplo de validación como en Cliente

- Usar atributos privados: self.__cedula
- Validar antes de guardar.
- Usar strip() en datos de texto.
- Lanzar excepción específica si el dato es inválido.
- Registrar INFO cuando el objeto se crea correctamente.

## Cómo probar

Ejecutar:
```
python test_cliente.py
```
Luego revisar sistema.log. Deben aparecer líneas INFO y ERROR.

