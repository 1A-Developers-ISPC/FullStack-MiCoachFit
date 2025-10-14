
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

    # El menú principal solo tiene Iniciar Sesión y Salir, por el momento. Faltaría agregar el Registro
    while True:
        print("\n=== Sistema MiCoachFit ===")
        print("1. Iniciar Sesión")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            email_login = input("Email de usuario: ") 
            contrasena = input("Contraseña: ")
            
            
            sistema.iniciar_sesion(email_login, contrasena)
        elif opcion == '2':
            print("\nHasta luego!")
            break
        else:
            print("\n⚠️ Opción inválida")

    db_conn.desconectar()

if __name__ == "__main__":  
    main()