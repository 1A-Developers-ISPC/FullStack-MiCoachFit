class Usuario:
    def __init__(self, nombre, apellido, email, contrasena, rol='usuario', 
                 usuario_id=None, telefono=None, entrenador_vinculado_id=None):
        
        self.usuario_id = usuario_id
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.telefono = telefono.strip() if telefono else None
        self.email = email.strip()
        # self.contrasena en texto plano de la BD
        self.contrasena = contrasena 
        self.rol = rol.strip().lower() 
        self.entrenador_vinculado_id = entrenador_vinculado_id

    def verificar_credenciales(self, contrasena_ingresada):
        """Compara la contraseña ingresada directamente con la almacenada en la BD (texto plano)."""
        return self.contrasena == contrasena_ingresada 

    def __str__(self):
        return (f"ID: {self.usuario_id} | {self.nombre} {self.apellido} | Email: {self.email} | "
                f"Tel: {self.telefono} | Rol: {self.rol}")