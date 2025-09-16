# ------------------- main.py -------------------
from sistema import SistemaUsuarios
from database import ConexionBD
from dbConfig import db_host, db_port, db_user, db_password, db_name

def main():
    db_conn = ConexionBD(
        host=db_host, 
        port=db_port, 
        user=db_user, 
        password=db_password, 
        database=db_name
    )

    if not db_conn.conectar():
        print("El programa no puede continuar sin una conexión a la base de datos.")
        return

    sistema = SistemaUsuarios(db_conn)

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
            print("\nHasta luego!")
            break
        else:
            print("\n⚠️ Opción inválida")

    db_conn.desconectar()

if __name__ == "__main__":
    main()
