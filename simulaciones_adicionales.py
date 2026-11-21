
# Simulaciones adicionales de casos INVÁLIDOS del sistema Software FJ.
# Cada caso debe fallar con una excepción del sistema, y el programa debe
# seguir funcionando hasta el final.
#
# Se ejecuta con: python simulaciones_adicionales.py

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo
from reserva import Reserva
from excepciones import SoftwareFJError
from logger import registrar_info, registrar_error


# CASO 1: Cliente sin nombre
def caso_01_cliente_sin_nombre():
    Cliente("1082345678", "", "persona@correo.com")


# CASO 2: Sala con capacidad cero
def caso_02_sala_capacidad_cero():
    ReservaSala("S10", "Sala vacía", 50000, 0)


# CASO 3: Reserva con horas negativas
def caso_03_reserva_horas_negativas():
    cliente = Cliente("1082345678", "Ana María Pérez", "ana.perez@correo.com")
    sala = ReservaSala("S11", "Sala Rodadero", 50000, 10)
    Reserva(cliente, sala, -2)


# CASO 4: Cliente con correo incorrecto
def caso_04_correo_mal_escrito():
    Cliente("1082345681", "Pedro Torres", "pedrogmail.com")


# CASO 5: Sala con capacidad negativa
def caso_05_capacidad_negativa():
    ReservaSala("S14", "Sala pequeña", 40000, -5)


# CASO 6: Reserva con duración de cero horas
def caso_06_reserva_sin_duracion():
    cliente = Cliente("1082345691", "Luis Alberto", "luis@gmail.com")
    sala = ReservaSala("S30", "Sala de capacitación", 40000, 10)
    Reserva(cliente, sala, 0)


# CASO 7: Cliente con correo vacío
def caso_07_correo_vacio():
    Cliente("1082345682", "Camila Torres", "")


# CASO 8: Reserva sin cliente
def caso_08_reserva_sin_cliente():
    sala = ReservaSala("S16", "Sala Principal", 45000, 10)
    Reserva(None, sala, 2)


# CASO 9: Sala con código vacío
def caso_09_codigo_sala_vacio():
    ReservaSala("", "Sala Oriente", 35000, 6)


# CASO 10: Cliente con documento muy corto
def caso_10_documento_corto():
    Cliente("123", "Andrés López", "andres@gmail.com")


# CASO 11: Cliente con números en el nombre
def caso_11_nombre_con_numeros():
    Cliente("1082345688", "Carlos123", "carlos@gmail.com")


# CASO 12: Sala sin descripción
def caso_12_sala_sin_descripcion():
    ReservaSala("S20", "", 40000, 8)


# CASO 13: Sala con precio como texto
def caso_13_precio_con_texto():
    ReservaSala("S21", "Sala Principal", "caro", 10)


# CASO 14: Sala con capacidad en texto
def caso_14_capacidad_con_texto():
    ReservaSala("S22", "Sala de reuniones", 50000, "muchas personas")


# CASO 15: Cliente con nombre formado por espacios
def caso_15_nombre_con_espacios():
    Cliente("1082345690", "     ", "usuario@gmail.com")


# LISTA DE CASOS
CASOS = [
    ("Cliente sin nombre", caso_01_cliente_sin_nombre),
    ("Sala con capacidad cero", caso_02_sala_capacidad_cero),
    ("Reserva con horas negativas", caso_03_reserva_horas_negativas),
    ("Cliente con correo mal escrito", caso_04_correo_mal_escrito),
    ("Sala con capacidad negativa", caso_05_capacidad_negativa),
    ("Reserva con duración de cero horas", caso_06_reserva_sin_duracion),
    ("Cliente con correo vacío", caso_07_correo_vacio),
    ("Reserva sin cliente", caso_08_reserva_sin_cliente),
    ("Sala con código vacío", caso_09_codigo_sala_vacio),
    ("Cliente con documento corto", caso_10_documento_corto),
    ("Cliente con números en el nombre", caso_11_nombre_con_numeros),
    ("Sala sin descripción", caso_12_sala_sin_descripcion),
    ("Sala con precio en texto", caso_13_precio_con_texto),
    ("Sala con capacidad en texto", caso_14_capacidad_con_texto),
    ("Cliente con nombre formado por espacios", caso_15_nombre_con_espacios),
]


# FUNCIÓN PARA EJECUTAR TODOS LOS CASOS
def ejecutar_casos():
    numero = 1

    for descripcion, funcion in CASOS:

        try:
            funcion()

        except SoftwareFJError as error:

            registrar_error(
                f"Caso adicional {numero} ({descripcion}) - "
                f"{type(error).__name__}: {error}",
                origen="Adicionales"
            )

            print(
                f"{numero:02d}. ERROR CONTROLADO - "
                f"{descripcion}: {error}"
            )

        except Exception as error:

            registrar_error(
                f"Caso adicional {numero} ({descripcion}) - "
                f"Error inesperado: {type(error).__name__}: {error}",
                origen="Adicionales"
            )

            print(
                f"{numero:02d}. ERROR NO CONTROLADO - "
                f"{descripcion}: {error}"
            )

        else:

            print(
                f"{numero:02d}. ATENCIÓN: "
                f"'{descripcion}' no produjo ningún error."
            )

        numero += 1


# INICIO DEL PROGRAMA
if __name__ == "__main__":

    registrar_info(
        "=== Inicio de simulaciones adicionales ===",
        origen="Adicionales"
    )

    print("\n==============================================")
    print("   SIMULACIONES ADICIONALES - SOFTWARE FJ")
    print("==============================================\n")

    ejecutar_casos()

    registrar_info(
        "=== Fin de simulaciones adicionales ===",
        origen="Adicionales"
    )

    print("\n==============================================")
    print("Fin: el programa siguió funcionando durante")
    print("todos los casos.")
    print("==============================================")



if __name__ == "_main_":
    registrar_info("=== Inicio de simulaciones adicionales ===", origen="Adicionales")
    ejecutar_casos()
    registrar_info("=== Fin de simulaciones adicionales ===", origen="Adicionales")
    print("Fin: el programa siguió funcionando durante todos los casos.")
