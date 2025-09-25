import mysql.connector
from mysql.connector import Error

class ConexionBD:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("\n✅ Conexión a la base de datos exitosa.")
                self.cursor = self.connection.cursor(dictionary=True) # Los resultados se devuelven como diccionarios
                return True
        except Error as e:
            print(f"\n❌ Error al conectar a la base de datos: {e}")
            return False

    def desconectar(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("\n🔒 Conexión a la base de datos cerrada.")

    def buscar_usuario(self, nombre_usuario):
        query = "SELECT u.*, r.nombre_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol WHERE u.nombre_usuario = %s"
        self.cursor.execute(query, (nombre_usuario,))
        return self.cursor.fetchone()

    def registrar_usuario(self, nombre, apellido, email, nombre_usuario, telefono, contrasena, rol):
        try:
            self.cursor.execute("SELECT id_rol FROM roles WHERE nombre_rol = %s", (rol,))
            rol_id = self.cursor.fetchone()
            if not rol_id:
                print(f"\n❌ Rol '{rol}' no encontrado en la base de datos.")
                return False

            query = "INSERT INTO usuarios (nombre, apellido, email, nombre_usuario, telefono, password, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (nombre, apellido, email, nombre_usuario, telefono, contrasena, rol_id['id_rol'])
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"\n❌ Error al registrar el usuario: {e}")
            self.connection.rollback()
            return False

    def cambiar_rol(self, nombre_usuario, nuevo_rol):
        try:
            self.cursor.execute("SELECT id_rol FROM roles WHERE nombre_rol = %s", (nuevo_rol,))
            rol_id = self.cursor.fetchone()
            if not rol_id:
                print(f"\n❌ Rol '{nuevo_rol}' no encontrado.")
                return False

            query = "UPDATE usuarios SET id_rol = %s WHERE nombre_usuario = %s"
            self.cursor.execute(query, (rol_id['id_rol'], nombre_usuario))
            self.connection.commit()
            return True
        except Error as e:
            print(f"\n❌ Error al actualizar el rol: {e}")
            self.connection.rollback()
            return False

    def eliminar_usuario(self, id_usuario):
        try:
            query = "DELETE FROM usuarios WHERE id_usuario = %s"
            self.cursor.execute(query, (id_usuario,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n❌ Error al eliminar el usuario: {e}")
            self.connection.rollback()
            return False

    def obtener_todos_usuarios(self):
        query = "SELECT u.*, r.nombre_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol"
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def actualizar_usuario(self, nombre_usuario, **kwargs):
        """Actualiza los datos de un usuario en la base de datos."""
        try:
            updates = []
            values = []
            for key, value in kwargs.items():
                updates.append(f"{key} = %s")
                values.append(value)
            
            if not updates:
                return False # No hay nada que actualizar

            query = "UPDATE usuarios SET " + ", ".join(updates) + " WHERE nombre_usuario = %s"
            values.append(nombre_usuario)
            
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n❌ Error al actualizar el usuario: {e}")
            self.connection.rollback()
            return False
