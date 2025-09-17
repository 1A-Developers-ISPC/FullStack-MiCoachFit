import re
from usuario import Usuario
from database import ConexionBD

class SistemaUsuarios:
    def __init__(self, db):
        self.db = db
    
    def validar_nombre_apellido(self, valor):
        return bool(valor.strip())

    def validar_nombre_usuario(self, valor):
        return bool(valor.strip()) and not self.db.buscar_usuario(valor.strip())

    def validar_telefono(self, telefono):
        telefono = telefono.strip()
        return re.fullmatch(r'\d{7,15}', telefono) is not None

    def validar_email(self, email):
        email = email.strip()
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron_email, email) is not None

    def validar_contrasena(self, contrasena):
        contrasena = contrasena.strip()
        if len(contrasena) < 6:
            return False
        if not re.search(r'[A-Za-z]', contrasena):
            return False
        if not re.search(r'\d', contrasena):
            return False
        return True

    def buscar_usuario(self, nombre_usuario):
        usuario_db = self.db.buscar_usuario(nombre_usuario)
        if usuario_db:
            return Usuario(
                nombre=usuario_db['nombre'],
                apellido=usuario_db['apellido'],
                nombre_usuario=usuario_db['nombre_usuario'],
                telefono=usuario_db['telefono'],
                email=usuario_db['email'],
                contrasena=usuario_db['password'], 
                rol=usuario_db['nombre_rol']
            )
        return None

    def registrar_usuario(self, nombre, apellido, nombre_usuario, telefono, email, contrasena, rol='usuario'):
        if not self.validar_nombre_apellido(nombre):
            print("\n❌ El nombre no puede estar vacío.")
            return
        if not self.validar_nombre_apellido(apellido):
            print("\n❌ El apellido no puede estar vacío.")
            return
        if not self.validar_nombre_usuario(nombre_usuario):
            print("\n❌ El nombre de usuario está vacío o ya existe.")
            return
        if not self.validar_telefono(telefono):
            print("\n❌ Teléfono inválido. Debe contener solo números (7 a 15 dígitos).")
            return
        if not self.validar_email(email):
            print("\n❌ Email inválido.")
            return
        if not self.validar_contrasena(contrasena):
            print("\n❌ La contraseña debe tener al menos 6 caracteres y contener letras y números.")
            return

        if self.db.registrar_usuario(nombre, apellido, email, nombre_usuario, telefono, contrasena, rol):
            print("\n✅ Usuario registrado exitosamente.")
        else:
            print("\n❌ No se pudo registrar el usuario.")

    def iniciar_sesion(self, nombre_usuario, contrasena):
        if not nombre_usuario.strip():
            print("\n❌ El nombre de usuario no puede estar vacío.")
            return
        if not contrasena.strip():
            print("\n❌ La contraseña no puede estar vacía.")
            return
        usuario = self.buscar_usuario(nombre_usuario)
        if usuario and usuario.verificar_credenciales(contrasena):
            print(f"\n🔓 Bienvenido, {usuario.nombre} {usuario.apellido}")
            if usuario.rol == 'admin':
                self.menu_admin()
            else:
                self.menu_usuario(usuario)
        else:
            print("\n❌ Nombre de usuario o contraseña incorrectos.")

    def menu_admin(self):
        while True:
            print("\n--- Menú Administrador ---")
            print("1. Ver todos los usuarios")
            print("2. Cambiar rol de usuario")
            print("3. Eliminar usuario")
            print("4. Cerrar sesión")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                self.mostrar_usuarios()
            elif opcion == '2':
                self.cambiar_rol()
            elif opcion == '3':
                self.eliminar_usuario()
            elif opcion == '4':
                print("\n🔒 Sesión cerrada.")
                break
            else:
                print("\n⚠️ Opción inválida")

    def menu_usuario(self, usuario):
        while True:
            print(f"\n--- Menú Usuario ---")
            print(f"1. Ver mi perfil")
            print(f"2. Editar mi perfil")
            print(f"3. Cerrar sesión")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                print(f"\nNombre: {usuario.nombre} {usuario.apellido}")
                print(f"Nombre de usuario: {usuario.nombre_usuario}")
                print(f"Teléfono: {usuario.telefono}")
                print(f"Email: {usuario.email}")
                print(f"Rol: {usuario.rol}")
            elif opcion == '2':
                self.editar_perfil(usuario)
                # Recargamos la información del usuario después de la edición
                usuario_actualizado = self.buscar_usuario(usuario.nombre_usuario)
                if usuario_actualizado:
                    usuario = usuario_actualizado
            elif opcion == '3':
                print("\n🔒 Sesión cerrada.")
                break
            else:
                print("\n⚠️ Opción inválida")


    def mostrar_usuarios(self):
        print("\n📋 Lista de usuarios:")
        usuarios_db = self.db.obtener_todos_usuarios()
        for usuario_db in usuarios_db:
            # Corregido: ahora se imprime el ID del usuario
            print(f" - ID: {usuario_db['id_usuario']} | {usuario_db['nombre']} {usuario_db['apellido']} | Usuario: {usuario_db['nombre_usuario']} | Rol: {usuario_db['nombre_rol']}")

    def cambiar_rol(self):
        nombre_usuario = input("Ingrese el nombre del usuario a modificar: ")
        if not nombre_usuario.strip():
            print("\n❌ El nombre de usuario no puede estar vacío.")
            return
        usuario = self.db.buscar_usuario(nombre_usuario)
        if usuario:
            nuevo_rol = input("Ingrese el nuevo rol (admin/usuario): ")
            if nuevo_rol in ['admin', 'usuario']:
                if self.db.cambiar_rol(nombre_usuario, nuevo_rol):
                    print("\n✅ Rol actualizado.")
                else:
                    print("\n❌ No se pudo actualizar el rol.")
            else:
                print("\n❌ Rol inválido.")
        else:
            print("\n❌ Usuario no encontrado.")

    def eliminar_usuario(self):
        try:
            id_usuario_eliminar = int(input("Ingrese el ID del usuario a eliminar: "))
            if self.db.eliminar_usuario(id_usuario_eliminar):
                print("\n✅ Usuario eliminado.")
            else:
                print("\n❌ No se pudo eliminar el usuario. El ID no existe.")
        except ValueError:
            print("\n❌ Por favor, ingrese un número de ID válido.")

    def editar_perfil(self, usuario):
        print("\n--- Editar Perfil ---")
        print("Deje el campo en blanco si no desea modificarlo.")
        
        nuevo_nombre = input(f"Nombre ({usuario.nombre}): ")
        if nuevo_nombre.strip() and self.validar_nombre_apellido(nuevo_nombre):
            usuario.nombre = nuevo_nombre
        else:
            print("\n⚠️ Nombre no válido o sin cambios.")

        nuevo_apellido = input(f"Apellido ({usuario.apellido}): ")
        if nuevo_apellido.strip() and self.validar_nombre_apellido(nuevo_apellido):
            usuario.apellido = nuevo_apellido
        else:
            print("\n⚠️ Apellido no válido o sin cambios.")

        nuevo_telefono = input(f"Teléfono ({usuario.telefono}): ")
        if nuevo_telefono.strip() and self.validar_telefono(nuevo_telefono):
            usuario.telefono = nuevo_telefono
        else:
            print("\n⚠️ Teléfono no válido o sin cambios.")
            
        nuevo_email = input(f"Email ({usuario.email}): ")
        if nuevo_email.strip() and self.validar_email(nuevo_email):
            usuario.email = nuevo_email
        else:
            print("\n⚠️ Email no válido o sin cambios.")

        nuevo_contrasena = input("Nueva contraseña (dejar en blanco para no cambiar): ")
        if nuevo_contrasena.strip() and self.validar_contrasena(nuevo_contrasena):
            usuario.contrasena = nuevo_contrasena
        else:
            print("\n⚠️ Contraseña no válida o sin cambios.")
            
        # Creamos un diccionario con los datos a actualizar
        datos_a_actualizar = {}
        if nuevo_nombre.strip() and self.validar_nombre_apellido(nuevo_nombre):
            datos_a_actualizar['nombre'] = nuevo_nombre
        if nuevo_apellido.strip() and self.validar_nombre_apellido(nuevo_apellido):
            datos_a_actualizar['apellido'] = nuevo_apellido
        if nuevo_telefono.strip() and self.validar_telefono(nuevo_telefono):
            datos_a_actualizar['telefono'] = nuevo_telefono
        if nuevo_email.strip() and self.validar_email(nuevo_email):
            datos_a_actualizar['email'] = nuevo_email
        if nuevo_contrasena.strip() and self.validar_contrasena(nuevo_contrasena):
            datos_a_actualizar['password'] = nuevo_contrasena

        if datos_a_actualizar:
            if self.db.actualizar_usuario(usuario.nombre_usuario, **datos_a_actualizar):
                print("\n✅ Perfil actualizado exitosamente.")
            else:
                print("\n❌ No se pudo actualizar el perfil.")
        else:
            print("\n📝 No se realizaron cambios en el perfil.")
