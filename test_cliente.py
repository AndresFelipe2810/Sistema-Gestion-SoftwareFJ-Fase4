# test_cliente.py
# Pruebas de la clase Cliente y del manejo de excepciones.
# Demuestra try/except, try/except/else, try/except/finally y encadenamiento.

from cliente import Cliente
from excepciones import ClienteInvalidoError
from logger import limpiar_log

print(" INICIANDO PRUEBAS DE CLIENTES Y EXCEPCIONES")

# Se limpia el log al inicio para que la demostración sea clara.
# Si se quiere conservar el historial, comentar esta línea.
limpiar_log()
print("[INFO] Archivo de logs limpiado para iniciar la prueba.\n")



# Prueba 1: Cliente válido usando try / except / else / finally
# Si no hay excepción, entra al else. El finally siempre se ejecuta.

print("Prueba 1: Cliente válido (try/except/else/finally)")
try:
    c1 = Cliente("12345678", "Carlos Pérez", "carlos@mail.com")
except ClienteInvalidoError as e:
    print(f"[ERROR ESPERADO]: {e}")
else:
    print(f"[ÉXITO] Cliente creado correctamente: {c1}")
finally:
    print("[FIN] Intento de creación de cliente finalizado.\n")



# Prueba 2: Cédula inválida usando try / except / finally
# Se espera que el error se capture y quede registrado en sistema.log.

print("Prueba 2: Cédula inválida (try/except/finally)")
try:
    c2 = Cliente("123", "Ana Gómez", "ana@mail.com")
except ClienteInvalidoError as e:
    print(f"[LOG CAPTURADO]: {e}")
finally:
    print("[FIN] Intento con cédula inválida finalizado.\n")



# Prueba 3: Correo inválido usando try / except

print("Prueba 3: Correo inválido (try/except)")
try:
    c3 = Cliente("98765432", "Pedro Picapiedra", "pedromail.com")
except ClienteInvalidoError as e:
    print(f"[LOG CAPTURADO]: {e}")
print()



# Prueba 4: Nombre solo con números

print("Prueba 4: Nombre solo con números (try/except)")
try:
    c4 = Cliente("11223344", "12345", "nombre@mail.com")
except ClienteInvalidoError as e:
    print(f"[LOG CAPTURADO]: {e}")
print()



# Prueba 5: Cédula y correo con espacios
# El strip() debe limpiar los espacios y permitir la creación correcta.

print("Prueba 5: Datos con espacios (deben limpiarse y aceptarse)")
try:
    c5 = Cliente("  55667788  ", "  Laura Díaz  ", "  laura@mail.com  ")
except ClienteInvalidoError as e:
    print(f"[ERROR INESPERADO]: {e}")
else:
    print(f"[ÉXITO] Cliente creado tras limpiar espacios: {c5}")
print()


# Prueba 6: Encadenamiento de excepciones con raise ... from
# Se simula un dato numérico que no se puede convertir.
# La excepción original (ValueError) queda encadenada como causa.

print("Prueba 6: Encadenamiento de excepciones (raise ... from)")
try:
    dato = int("abc")  # Esto lanza ValueError
except ValueError as e:
    try:
        # Se relanza como ClienteInvalidoError conservando la causa original.
        raise ClienteInvalidoError(
            "No se pudo convertir un dato numérico del cliente."
        ) from e
    except ClienteInvalidoError as e2:
        print(f"[LOG CAPTURADO]: {e2}")
        print(f"[CAUSA ORIGINAL]: {e2.__cause__}")
print()


print("\nFIN")