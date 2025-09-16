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
                self.cursor = self.connection.cursor(dictionary=True)
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
