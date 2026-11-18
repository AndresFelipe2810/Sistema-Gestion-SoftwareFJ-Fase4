# Sistema Integral de Gestión - Software FJ (Fase 4)

Proyecto colaborativo desarrollado para el curso de **Programación (UNAD)**. Sistema orientado a objetos para la gestión de clientes, servicios y reservas, implementado sin bases de datos, con validaciones estrictas, manejo avanzado de excepciones y registro centralizado de eventos.

## Estructura del Proyecto

El sistema está dividido en módulos independientes para garantizar la modularidad y el cumplimiento de los principios de la Programación Orientada a Objetos (POO):

- **`entidad.py`**: Contiene la clase abstracta base (`EntidadBase`) de la cual heredan las entidades del sistema.
- **`cliente.py`**: Módulo de gestión de usuarios con encapsulación mediante propiedades (`@property`) y validaciones estrictas.
- **`servicios.py`**: Define la clase abstracta `Servicio` y tres variantes especializadas (*Reserva de salas*, *Alquiler de equipos* y *Asesorías especializadas*), implementando polimorfismo y costos con parámetros opcionales.
- **`reserva.py`**: Integra cliente, servicio, duración y estados de la operación (confirmada, cancelada, procesada).
- **`excepciones.py`**: Jerarquía completa de excepciones personalizadas de la aplicación (`SoftwareFJError` y subclases).
- **`logger.py`**: Configuración del sistema centralizado de logs para el registro de errores y eventos en `sistema.log`.
- **`main.py`**: Punto de entrada de la aplicación encargado de ejecutar las simulaciones completas (casos válidos e inválidos).

## Requisitos y Ejecución

El proyecto está desarrollado en **Python** puro y no requiere motores de bases de datos ni instalación de paquetes externos. 

Para ejecutar el programa y verificar las simulaciones completas, abre una terminal en la carpeta raíz del proyecto y ejecuta el siguiente comando:

``` python
python main.py
```