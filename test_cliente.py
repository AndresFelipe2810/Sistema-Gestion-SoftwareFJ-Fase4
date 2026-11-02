# Archivo para probar que los errores se atrapan bien y se escriben en el sistema.log
from cliente import Cliente
from excepciones import ClienteInvalidoError

print("--- INICIANDO PRUEBAS DE CLIENTES Y EXCEPCIONES ---")

# Prueba 1: Cliente Válido
try:
    c1 = Cliente("12345678", "Carlos Pérez", "carlos@mail.com")
    print(f"[ÉXITO] Creado correctamente: {c1}")
except ClienteInvalidoError as e:
    print(f"[ERROR ESPERADO]: {e}")

# Prueba 2: Cliente con Cédula inválida (debe generar error y log)
try:
    print("\nIntentando crear cliente con cédula inválida...")
    c2 = Cliente("123", "Ana Gómez", "ana@mail.com")
except ClienteInvalidoError as e:
    print(f"[LOG CAPTURADO]: {e}")

# Prueba 3: Cliente con Correo Inválido
try:
    print("\nIntentando crear cliente con correo sin '@'... del correo")
    c3 = Cliente("98765432", "Pedro Picapiedra", "pedromail.com")
except ClienteInvalidoError as e:
    print(f"[LOG CAPTURADO]: {e}")

print("\n--- PRUEBA FINALIZADA. ---")