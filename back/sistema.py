# ------------------- sistema.py -------------------
import re
from usuario import Usuario

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = []

    def validar_nombre_apellido(self, valor):
        return bool(valor.strip())

    def validar_nombre_usuario(self, valor):
        return bool(valor.strip()) and not self.buscar_usuario(valor.strip())

    def validar_telefono(self, telefono):
        # Validamos teléfono: solo números, mínimo 7 y máximo 15 dígitos
        telefono = telefono.strip()
        return re.fullmatch(r'\d{7,15}', telefono) is not None

    def validar_email(self, email):
        email = email.strip()
        # Validación simple de email
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
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                return usuario
        return None

    def registrar_usuario(self, nombre, apellido, nombre_usuario, telefono, email, contrasena, rol='usuario'):
        # Validaciones:
        if not self.validar_nombre_apellido(nombre):
            print("❌ El nombre no puede estar vacío.")
            return
        if not self.validar_nombre_apellido(apellido):
            print("❌ El apellido no puede estar vacío.")
            return
        if not self.validar_nombre_usuario(nombre_usuario):
            print("❌ El nombre de usuario está vacío o ya existe.")
            return
        if not self.validar_telefono(telefono):
            print("❌ Teléfono inválido. Debe contener solo números (7 a 15 dígitos).")
            return
        if not self.validar_email(email):
            print("❌ Email inválido.")
            return
        if not self.validar_contrasena(contrasena):
            print("❌ La contraseña debe tener al menos 6 caracteres y contener letras y números.")
            return

        nuevo_usuario = Usuario(nombre, apellido, nombre_usuario, telefono, email, contrasena, rol)
        self.usuarios.append(nuevo_usuario)
        print("✅ Usuario registrado exitosamente.")

    def iniciar_sesion(self, nombre_usuario, contrasena):
        if not nombre_usuario.strip():
            print("❌ El nombre de usuario no puede estar vacío.")
            return
        if not contrasena.strip():
            print("❌ La contraseña no puede estar vacía.")
            return
        usuario = self.buscar_usuario(nombre_usuario)
        if usuario and usuario.verificar_credenciales(contrasena):
            print(f"🔓 Bienvenido, {usuario.nombre} ({usuario.rol})")
            if usuario.rol == 'admin':
                self.menu_admin()
            else:
                self.menu_usuario(usuario)
        else:
            print("❌ Nombre de usuario o contraseña incorrectos.")

    # Los demás métodos de menú y funciones se mantienen igual, adaptando para mostrar datos nuevos.

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
                print("🔒 Sesión cerrada.")
                break
            else:
                print("⚠️ Opción inválida")

    def menu_usuario(self, usuario):
        print(f"\n--- Menú Usuario ---")
        print(f"Nombre: {usuario.nombre} {usuario.apellido}")
        print(f"Nombre de usuario: {usuario.nombre_usuario}")
        print(f"Teléfono: {usuario.telefono}")
        print(f"Email: {usuario.email}")
        print(f"Rol: {usuario.rol}")

    def mostrar_usuarios(self):
        print("\n📋 Lista de usuarios:")
        for usuario in self.usuarios:
            print(f" - {usuario}")

    def cambiar_rol(self):
        nombre_usuario = input("Ingrese el nombre del usuario a modificar: ")
        if not nombre_usuario.strip():
            print("❌ El nombre de usuario no puede estar vacío.")
            return
        usuario = self.buscar_usuario(nombre_usuario)
        if usuario:
            nuevo_rol = input("Ingrese el nuevo rol (admin/usuario): ")
            if nuevo_rol in ['admin', 'usuario']:
                usuario.rol = nuevo_rol
                print("✅ Rol actualizado.")
            else:
                print("❌ Rol inválido.")
        else:
            print("❌ Usuario no encontrado.")

    def eliminar_usuario(self):
        nombre_usuario = input("Ingrese el nombre del usuario a eliminar: ")
        if not nombre_usuario.strip():
            print("❌ El nombre de usuario no puede estar vacío.")
            return
        usuario = self.buscar_usuario(nombre_usuario)
        if usuario:
            self.usuarios.remove(usuario)
            print("✅ Usuario eliminado.")
        else:
            print("❌ Usuario no encontrado.")