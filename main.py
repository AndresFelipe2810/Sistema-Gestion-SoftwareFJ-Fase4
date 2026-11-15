# main.py
# Punto de entrada del sistema de gestión de Software FJ.
# Ejecuta 19 simulaciones de operación (válidas e inválidas) sin base de datos.
# Todos los eventos y errores se registran en sistema.log y el programa
# continúa funcionando aunque ocurran errores.
#
# Para ejecutarlo:  python main.py

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SoftwareFJError
from logger import registrar_info, registrar_error, registrar_evento, limpiar_log


# Simulaciones. Cada una recibe "ctx", un diccionario donde se guardan los
# objetos creados (clientes, servicios, reservas) para usarlos después.

def sim_01_cliente_valido(ctx):
    ctx["cliente"] = Cliente("1082345678", "Ana María Pérez", "ana.perez@correo.com")
    return ctx["cliente"].obtener_detalle()


def sim_02_cliente_cedula_invalida(ctx):
    # La cédula contiene letras: debe lanzar ClienteInvalidoError.
    Cliente("12AB", "Luis Gómez", "luis@correo.com")


def sim_03_cliente_correo_invalido(ctx):
    # Correo sin arroba: debe lanzar ClienteInvalidoError.
    Cliente("1090123456", "Carlos Ruiz", "carlos-sin-arroba")


def sim_04_servicios_validos(ctx):
    ctx["sala"] = ReservaSala("S01", "Sala Magdalena", 50000, 10)
    ctx["auditorio"] = ReservaSala("S02", "Auditorio Tayrona", 80000, 40)
    ctx["equipo"] = AlquilerEquipo("E01", "Video Beam", 15000, "videoproyector", 2)
    ctx["asesoria"] = AsesoriaEspecializada("A01", "Asesoría Python", 70000, "Python", "senior")
    # Servicio en mantenimiento, se usa en una simulación posterior.
    ctx["sala_mantenimiento"] = ReservaSala("S03", "Sala Sierra", 50000, 8, disponible=False)
    return ctx["asesoria"].obtener_detalle()


def sim_05_servicio_tarifa_negativa(ctx):
    # Tarifa negativa: debe lanzar ParametroInvalidoError.
    AlquilerEquipo("E99", "Proyector", -5000, "videoproyector")


def sim_06_servicio_nivel_inexistente(ctx):
    # Nivel que no existe: debe lanzar ParametroInvalidoError.
    AsesoriaEspecializada("A99", "Asesoría Datos", 60000, "Datos", "maestro")


def sim_07_reserva_sala_exitosa(ctx):
    reserva = Reserva(ctx["cliente"], ctx["sala"], 3)
    reserva.confirmar()
    reserva.procesar(0.19, 0.10)   # con impuesto del 19 % y descuento del 10 %
    ctx["reserva_procesada"] = reserva
    return reserva.obtener_detalle()


def sim_08_reserva_auditorio_exitosa(ctx):
    # Sala grande: se aplica el recargo del 15 %.
    reserva = Reserva(ctx["cliente"], ctx["auditorio"], 2)
    reserva.confirmar()
    reserva.procesar(0.19)
    return reserva.obtener_detalle()


def sim_09_reserva_equipo_exitosa(ctx):
    reserva = Reserva(ctx["cliente"], ctx["equipo"], 5)
    reserva.confirmar()
    reserva.procesar()
    return reserva.obtener_detalle()


def sim_10_reserva_asesoria_exitosa(ctx):
    reserva = Reserva(ctx["cliente"], ctx["asesoria"], 2)
    reserva.confirmar()
    reserva.procesar(0.19, 0.05)
    return reserva.obtener_detalle()


def sim_11_reserva_duracion_excesiva(ctx):
    # Una sala solo se puede reservar hasta 12 horas.
    Reserva(ctx["cliente"], ctx["sala"], 30)


def sim_12_reserva_duracion_texto(ctx):
    # La duración llega como texto no numérico (error encadenado en 3 niveles).
    Reserva(ctx["cliente"], ctx["sala"], "dos horas")


def sim_13_reserva_servicio_no_disponible(ctx):
    reserva = Reserva(ctx["cliente"], ctx["sala_mantenimiento"], 2)
    reserva.confirmar()   # falla porque el servicio no está disponible


def sim_14_reserva_sin_cliente(ctx):
    # Intento de reserva sin cliente.
    Reserva(None, ctx["sala"], 2)


def sim_15_procesar_sin_confirmar(ctx):
    # Operación no permitida: procesar una reserva que sigue pendiente.
    reserva = Reserva(ctx["cliente"], ctx["sala"], 1)
    reserva.procesar()


def sim_16_cancelar_reserva_valida(ctx):
    reserva = Reserva(ctx["cliente"], ctx["sala"], 4)
    reserva.confirmar()
    reserva.cancelar("El cliente cambió de fecha")
    return reserva.obtener_detalle()


def sim_17_cancelar_reserva_procesada(ctx):
    # Operación no permitida: una reserva procesada no se puede cancelar.
    ctx["reserva_procesada"].cancelar("Intento tardío")


def sim_18_descuento_total_inconsistente(ctx):
    # Un descuento del 100 % deja el costo en cero: cálculo inconsistente.
    reserva = Reserva(ctx["cliente"], ctx["sala"], 2)
    reserva.confirmar()
    reserva.procesar(0.0, 1.0)


def sim_19_error_inesperado(ctx):
    # Error que NO es del sistema: se usa una clave que no existe.
    # Sirve para demostrar que el programa sigue funcionando.
    return ctx["reserva_inexistente"].obtener_detalle()


# Lista de simulaciones: cada elemento es (descripción, función).
SIMULACIONES = [
    ("Registro de cliente válido", sim_01_cliente_valido),
    ("Cliente con cédula inválida", sim_02_cliente_cedula_invalida),
    ("Cliente con correo inválido", sim_03_cliente_correo_invalido),
    ("Creación de servicios válidos", sim_04_servicios_validos),
    ("Servicio con tarifa negativa", sim_05_servicio_tarifa_negativa),
    ("Asesoría con nivel inexistente", sim_06_servicio_nivel_inexistente),
    ("Reserva de sala exitosa", sim_07_reserva_sala_exitosa),
    ("Reserva de auditorio exitosa", sim_08_reserva_auditorio_exitosa),
    ("Reserva de equipo exitosa", sim_09_reserva_equipo_exitosa),
    ("Reserva de asesoría exitosa", sim_10_reserva_asesoria_exitosa),
    ("Reserva con duración excesiva", sim_11_reserva_duracion_excesiva),
    ("Reserva con duración en texto", sim_12_reserva_duracion_texto),
    ("Reserva de servicio no disponible", sim_13_reserva_servicio_no_disponible),
    ("Reserva sin cliente", sim_14_reserva_sin_cliente),
    ("Procesar reserva sin confirmar", sim_15_procesar_sin_confirmar),
    ("Cancelación de reserva válida", sim_16_cancelar_reserva_valida),
    ("Cancelar reserva ya procesada", sim_17_cancelar_reserva_procesada),
    ("Descuento del 100 % (cálculo inconsistente)", sim_18_descuento_total_inconsistente),
    ("Error inesperado (clave inexistente)", sim_19_error_inesperado),
]


def registrar_cadena_de_causas(error):
    # Registra, con un bucle, cada causa de un error encadenado (raise ... from).
    causa = error.__cause__
    nivel = 1
    while causa is not None:
        registrar_error(
            f"   Causa {nivel}: {type(causa).__name__}: {causa}",
            origen="Simulacion"
        )
        causa = causa.__cause__
        nivel = nivel + 1


def ejecutar_simulaciones():
    ctx = {}
    exitosas = 0
    errores_controlados = 0
    errores_inesperados = 0
    numero = 1

    for descripcion, funcion in SIMULACIONES:
        registrar_info(f"Inicio simulación {numero}: {descripcion}", origen="Simulacion")
        try:
            resultado = funcion(ctx)
        except SoftwareFJError as error:
            # Error propio del sistema: se maneja y se registra aquí.
            errores_controlados = errores_controlados + 1
            registrar_error(
                f"Simulación {numero} ({descripcion}) - {type(error).__name__}: {error}",
                origen="Simulacion"
            )
            registrar_cadena_de_causas(error)
            print(f"{numero:02d}. ERROR CONTROLADO  {descripcion}: {error}")
        except Exception as error:
            # Cualquier otro error: se registra como CRITICAL y el programa sigue.
            errores_inesperados = errores_inesperados + 1
            registrar_evento(
                "CRITICAL",
                f"Simulación {numero} ({descripcion}) - error inesperado "
                f"{type(error).__name__}: {error}",
                origen="Simulacion"
            )
            print(f"{numero:02d}. ERROR INESPERADO  {descripcion}: {type(error).__name__}: {error}")
        else:
            # Solo se ejecuta si la simulación terminó sin errores.
            exitosas = exitosas + 1
            registrar_info(f"Simulación {numero} exitosa: {descripcion}", origen="Simulacion")
            print(f"{numero:02d}. OK                {descripcion}: {resultado}")
        finally:
            # Se ejecuta siempre: marca el fin de cada simulación en el log.
            registrar_info(f"Fin simulación {numero}", origen="Simulacion")
        numero = numero + 1

    return exitosas, errores_controlados, errores_inesperados


def main():
    # Se limpia el log para que la demostración quede registrada desde cero.
    limpiar_log()
    registrar_info("=== Inicio del sistema Software FJ ===", origen="Main")
    print("=== Sistema de gestión Software FJ: simulación de operaciones ===\n")

    exitosas, controlados, inesperados = ejecutar_simulaciones()

    total = exitosas + controlados + inesperados
    print("\n=== Resumen ===")
    print(f"Simulaciones ejecutadas: {total}")
    print(f"Exitosas: {exitosas}")
    print(f"Errores controlados (excepciones del sistema): {controlados}")
    print(f"Errores inesperados (el programa continuó): {inesperados}")
    print("El sistema siguió funcionando durante todas las simulaciones.")
    print("Revise el detalle de eventos y errores en el archivo sistema.log")

    registrar_info(
        f"=== Fin del sistema Software FJ: {total} simulaciones "
        f"({exitosas} exitosas, {controlados} errores controlados, "
        f"{inesperados} inesperados) ===",
        origen="Main"
    )


if __name__ == "__main__":
    main()