# ------------------- main.py -------------------
from sistema import SistemaUsuarios

def main():
    sistema = SistemaUsuarios()

    # Crear admin por defecto si no existe
    if not sistema.buscar_usuario("admin"):
        sistema.registrar_usuario(
            nombre="Admin",
            apellido="Principal",
            nombre_usuario="admin",
            telefono="123456789",
            email="admin@ejemplo.com",
            contrasena="admin123",
            rol="admin"
        )

    while True:
        print("\n=== Sistema de Usuarios MiCoachFit ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            nombre_usuario = input("Nombre de usuario: ")
            telefono = input("Teléfono (solo números): ")
            email = input("Email: ")
            contrasena = input("Contraseña: ")
            sistema.registrar_usuario(nombre, apellido, nombre_usuario, telefono, email, contrasena)
        elif opcion == '2':
            nombre_usuario = input("Nombre de usuario: ")
            contrasena = input("Contraseña: ")
            sistema.iniciar_sesion(nombre_usuario, contrasena)
        elif opcion == '3':
            print("Hasta luego!")
            break
        else:
            print("⚠️ Opción inválida")

if __name__ == "__main__":
    main()