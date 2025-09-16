import re
from usuario import Usuario
from database import ConexionBD

class SistemaUsuarios:
    def __init__(self, db):
        self.db = db
    
    def validar_nombre_usuario(self, valor):
        return bool(valor.strip()) and not self.db.buscar_usuario(valor.strip())

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