# Simulaciones adicionales de casos INVÁLIDOS del sistema Software FJ.
# Cada caso debe fallar con una excepción del sistema, y el programa debe
# seguir funcionando hasta el final.
#
# Se ejecuta con:  python simulaciones_adicionales.py

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo
from reserva import Reserva
from excepciones import SoftwareFJError
from logger import registrar_info, registrar_error


# Casos inválidos (cada función debe lanzar una excepción del sistema)

def caso_01_cliente_sin_nombre():
    # El nombre está vacío: debe lanzar ClienteInvalidoError.
    Cliente("1082345678", "", "persona@correo.com")


def caso_02_sala_capacidad_cero():
    # Una sala no puede tener capacidad 0: debe lanzar ParametroInvalidoError.
    ReservaSala("S10", "Sala vacía", 50000, 0)


def caso_03_reserva_horas_negativas():
    # Una duración negativa no es válida: debe lanzar ReservaError.
    cliente = Cliente("1082345678", "Ana María Pérez", "ana.perez@correo.com")
    sala = ReservaSala("S11", "Sala Rodadero", 50000, 10)
    Reserva(cliente, sala, -2)



# Caso 4: Cliente con correo incorrecto
def caso_04_correo_mal_escrito():
    cliente = Cliente("1082345681", "Pedro Torres", "pedrogmail.com")
  # El correo electronico debe estara bien escrito


# Caso 5: Sala con capacidad negativa
def caso_05_capacidad_negativa():
    sala = ReservaSala("S14", "Sala pequeña", 40000, -5)
  # la capacidad de la sala debe ser positiva.


# Caso 6: Servicio con nombre vacío
def caso_06_sala_sin_nombre():
    sala = ReservaSala("S15", "", 30000, 5)
  # el servicio debe tener un nombre

# Caso 7: Cliente con correo vacío
def caso_07_correo_vacio():
    # El cliente debe tener un correo electronico.
    Cliente("1082345682", "Camila Torres", "")


# Caso 8: Reserva con cliente incorrecto
def caso_08_reserva_sin_cliente():
    # No se puede realizar una reserva sin un cliente valido.
    sala = ReservaSala("S16", "Sala Principal", 45000, 10)
    Reserva(None, sala, 2)


# Caso 9: Sala con código vacío
def caso_09_codigo_sala_vacio():
    # La sala debe tener un codigo para poder identificarla.
    ReservaSala("", "Sala Oriente", 35000, 6)

# Caso 10: Cliente con documento muy corto
def caso_10_documento_corto():
    # El documento del cliente debe tener una longitud valida.
    Cliente("123", "Andres Lopez", "andres@gmail.com")


# Caso 11: Sala sin codigo
def caso_11_sala_sin_codigo():
    # La sala necesita un codigo para poder identificarla.
    ReservaSala("", "Sala del Norte", 45000, 10)


# Caso 12: Sala sin descripcion
def caso_12_sala_sin_descripcion():
    # No se debe crear una sala sin colocar su nombre.
    ReservaSala("S20", "", 40000, 8)


# Caso 13: Sala con precio como texto
def caso_13_precio_con_texto():
    # El precio debe ser un valor numerico.
    ReservaSala("S21", "Sala Principal", "caro", 10)


# Caso 14: Sala con capacidad en texto
def caso_14_capacidad_con_texto():
    # La capacidad debe ser un numero.
    ReservaSala("S22", "Sala de reuniones", 50000, "muchas personas")


# Caso 15: Cliente con espacios en el nombre
def caso_15_nombre_con_espacios():
    # El nombre no puede estar formado solamente por espacios.
    Cliente("1082345690", "     ", "usuario@gmail.com")

CASOS = [
    ("Cliente sin nombre", caso_01_cliente_sin_nombre),
    ("Sala con capacidad 0", caso_02_sala_capacidad_cero),
    ("Reserva con horas negativas", caso_03_reserva_horas_negativas),
    ("Cliente con correo mal escrito", caso_04_correo_mal_escrito),
    ("Sala con capacidad negativa", caso_05_capacidad_negativa),
    ("Sala sin nombre", caso_06_sala_sin_nombre),
    ("Cliente con correo vacío", caso_07_correo_vacio),
    ("Reserva sin cliente", caso_08_reserva_sin_cliente),
    ("Sala con código vacío", caso_09_codigo_sala_vacio),
    ("Cliente con documento corto", caso_10_documento_corto),
    ("Sala sin código", caso_11_sala_sin_codigo),
    ("Sala sin descripción", caso_12_sala_sin_descripcion),
    ("Sala con precio en texto", caso_13_precio_con_texto),
    ("Sala con capacidad en texto", caso_14_capacidad_con_texto),
    ("Cliente con nombre formado por espacios", caso_15_nombre_con_espacios),
]

