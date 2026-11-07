# logger.py
# Módulo centralizado de registro de eventos y errores.
# Todos los módulos del sistema deben usar estas funciones para escribir en sistema.log.

import datetime
import os

# Nombre del archivo de logs. Se deja como constante para no repetirlo en todo el código.
ARCHIVO_LOG = "sistema.log"

# Niveles permitidos. Sirve como validación para evitar niveles "inventados".
NIVELES_VALIDOS = ("INFO", "WARNING", "ERROR", "CRITICAL")


def registrar_evento(nivel, mensaje, origen=None):
    # Registra un evento o error en el archivo de logs.
    #
    # Parámetros:
    #   nivel (str): Nivel del evento. Debe ser uno de NIVELES_VALIDOS
    #                ('INFO', 'WARNING', 'ERROR', 'CRITICAL').
    #   mensaje (str): Descripción del evento o error.
    #   origen (str, opcional): Nombre del módulo o clase que genera el evento.
    #                           Ejemplo: 'Cliente', 'Reserva', 'ServicioSala'.
    #
    # Retorna:
    #   bool: True si el log se escribió correctamente, False si hubo un problema
    #         al escribir en el archivo.

    # Validación básica del nivel para evitar registros inconsistentes.
    nivel = str(nivel).upper().strip()
    if nivel not in NIVELES_VALIDOS:
        nivel = "INFO"  # Si llega un nivel inválido, no se rompe el sistema: se registra como INFO.

    # Construcción de la línea de log con fecha, hora, nivel y origen.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefijo_origen = f"[{origen}] " if origen else ""
    linea = f"[{timestamp}] {nivel}: {prefijo_origen}{mensaje}\n"

    # La escritura se protege con try/except para que un fallo de disco o permisos no tumbe la aplicación.
    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
        return True
    except OSError as e:
        # Si no se puede escribir el log, se informa por consola sin lanzar excepción.
        print(f"[ADVERTENCIA] No se pudo escribir en '{ARCHIVO_LOG}': {e}")
        return False


def registrar_info(mensaje, origen=None):
    # Atajo para registrar eventos informativos (operaciones exitosas).
    return registrar_evento("INFO", mensaje, origen)


def registrar_advertencia(mensaje, origen=None):
    # Atajo para registrar advertencias (situaciones no críticas).
    return registrar_evento("WARNING", mensaje, origen)


def registrar_error(mensaje, origen=None):
    # Atajo para registrar errores controlados.
    return registrar_evento("ERROR", mensaje, origen)


def limpiar_log():
    # Se usa para limpiar el archivo de logs antes de una demostración o simulación final.
    try:
        with open(ARCHIVO_LOG, "w", encoding="utf-8") as archivo:
            archivo.write("")
        return True
    except OSError as e:
        print(f"[ADVERTENCIA] No se pudo limpiar '{ARCHIVO_LOG}': {e}")
        return False


def existe_log():
    # Indica si el archivo de logs ya existe en el directorio del proyecto.
    return os.path.exists(ARCHIVO_LOG)