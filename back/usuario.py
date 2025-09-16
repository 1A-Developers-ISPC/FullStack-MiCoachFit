# ------------------- usuario.py -------------------
import re

class Usuario:
    def __init__(self, nombre, apellido, nombre_usuario, telefono, email, contrasena, rol='usuario'):
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.nombre_usuario = nombre_usuario.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()
        self.contrasena = contrasena
        self.rol = rol

    def verificar_credenciales(self, contrasena):
        return self.contrasena == contrasena

    def __str__(self):
        return (f"{self.nombre} {self.apellido} | Usuario: {self.nombre_usuario} | "
                f"Tel: {self.telefono} | Email: {self.email} | Rol: {self.rol}")