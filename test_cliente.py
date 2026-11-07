# test_cliente.py
# Pruebas de la clase Cliente y del manejo de excepciones.
# Demuestra try/except, try/except/else, try/except/finally, encadenamiento,
# validación en @setter y rechazo de None.

from cliente import Cliente
from excepciones import ClienteInvalidoError
from logger import limpiar_log, registrar_error

print("=== INICIANDO PRUEBAS DE CLIENTES Y EXCEPCIONES ===")

# Se limpia el log al inicio para que la demostración sea clara.
limpiar_log()
print("[INFO] Archivo de logs limpiado para iniciar la prueba.\n")


# Prueba 1: Cliente válido usando try / except / else / finally
print("Prueba 1: Cliente válido (try/except/else/finally)")
try:
    c1 = Cliente("12345678", "Carlos Pérez", "carlos@mail.com")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[ERROR ESPERADO]: {e}")
else:
    print(f"[ÉXITO] Cliente creado correctamente: {c1}")
finally:
    print("[FIN] Intento de creación de cliente finalizado.\n")


# Prueba 2: Cédula inválida usando try / except / finally
print("Prueba 2: Cédula inválida (try/except/finally)")
try:
    c2 = Cliente("123", "Ana Gómez", "ana@mail.com")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO]: {e}")
finally:
    print("[FIN] Intento con cédula inválida finalizado.\n")


# Prueba 3: Correo inválido usando try / except
print("Prueba 3: Correo inválido (try/except)")
try:
    c3 = Cliente("98765432", "Pedro Picapiedra", "pedromail.com")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO]: {e}")
print()


# Prueba 4: Nombre solo con números
print("Prueba 4: Nombre solo con números (try/except)")
try:
    c4 = Cliente("11223344", "12345", "nombre@mail.com")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO]: {e}")
print()


# Prueba 5: Datos con espacios (el strip() debe limpiarlos y aceptarlos)
print("Prueba 5: Datos con espacios (deben limpiarse y aceptarse)")
try:
    c5 = Cliente("  55667788  ", "  Laura Díaz  ", "  laura@mail.com  ")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[ERROR INESPERADO]: {e}")
else:
    print(f"[ÉXITO] Cliente creado tras limpiar espacios: {c5}")
print()


# Prueba 6: Encadenamiento con raise ... from
# Se registra la causa original junto con la excepción final.
print("Prueba 6: Encadenamiento de excepciones (raise ... from)")
try:
    dato = int("abc")
except ValueError as e:
    try:
        raise ClienteInvalidoError(
            "No se pudo convertir un dato numérico del cliente."
        ) from e
    except ClienteInvalidoError as e2:
        registrar_error(
            f"{e2} (causa: {e2.__cause__})",
            origen="test_cliente"
        )
        print(f"[LOG CAPTURADO]: {e2}")
        print(f"[CAUSA ORIGINAL]: {e2.__cause__}")
print()


# Prueba 7: Reasignación de una propiedad con @setter
print("Prueba 7: Reasignación con @setter (debe validar)")
c7 = Cliente("44556677", "Marta Ruiz", "marta@mail.com")
try:
    c7.cedula = "12"
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO]: {e}")
finally:
    print(f"[FIN] La cédula del cliente sigue siendo: {c7.cedula}\n")


# Prueba 8: Rechazo de None en los tres campos
# Demuestra el hallazgo IMPORTANTE de la revisión: None no debe aceptarse.
print("Prueba 8: Rechazo de None en cédula, nombre y correo")

# 8a: nombre=None
try:
    Cliente("12345678", None, "test@mail.com")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO - nombre None]: {e}")

# 8b: cédula=None
try:
    Cliente(None, "Carlos", "test@mail.com")
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO - cédula None]: {e}")

# 8c: correo=None
try:
    Cliente("12345678", "Carlos", None)
except ClienteInvalidoError as e:
    registrar_error(str(e), origen="Cliente")
    print(f"[LOG CAPTURADO - correo None]: {e}")

print()


print("=== PRUEBA FINALIZADA ===")