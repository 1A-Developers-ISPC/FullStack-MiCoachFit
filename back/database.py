import mysql.connector
from mysql.connector import Error
import datetime

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
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"\n❌ Error al conectar a la base de datos: {e}")
            return False

    def desconectar(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
    
    # ----------------------------------------------------
    # Funciones CRUD para USUARIOS
    # ----------------------------------------------------
    
    def buscar_usuario(self, email):
        query = "SELECT u.*, r.nombre_rol FROM USUARIOS u JOIN ROLES r ON u.rol_id = r.rol_id WHERE u.email = %s"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()

    def registrar_usuario(self, nombre, apellido, email, telefono, contrasena, rol, entrenador_vinculado_id=None):
        try:
            rol_busqueda = rol.lower().strip()
            self.cursor.execute("SELECT rol_id FROM ROLES WHERE nombre_rol = %s", (rol_busqueda,))
            rol_id_data = self.cursor.fetchone()
            if not rol_id_data:
                print(f"\n❌ Rol '{rol_busqueda}' no encontrado en la base de datos.")
                return False
            
            rol_id = rol_id_data['rol_id']
            # Se guarda la contraseña en texto plano
            password_plano = contrasena 
            
            query = """
            INSERT INTO USUARIOS (nombre, apellido, email, telefono, password_hash, rol_id, entrenador_vinculado_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (nombre, apellido, email, telefono, password_plano, rol_id, entrenador_vinculado_id)
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            if e.errno == 1062:
                 print("\n❌ Error: El email ya está registrado.")
            else:
                 print(f"\n❌ Error al registrar el usuario: {e}")
            self.connection.rollback()
            return False

    def obtener_todos_usuarios(self):
        query = """
        SELECT 
            u.usuario_id, u.nombre, u.apellido, u.email, u.telefono, r.nombre_rol, 
            e.nick_entrenador
        FROM USUARIOS u 
        JOIN ROLES r ON u.rol_id = r.rol_id
        LEFT JOIN ENTRENADORES e ON u.entrenador_vinculado_id = e.entrenador_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def actualizar_usuario(self, usuario_id, **kwargs):
        try:
            updates = []
            values = []
            if 'contrasena' in kwargs:
                contrasena_plano = kwargs.pop('contrasena')
                kwargs['password_hash'] = contrasena_plano
                
            for key, value in kwargs.items():
                updates.append(f"{key} = %s")
                values.append(value)
            
            if not updates:
                return False

            query = "UPDATE USUARIOS SET " + ", ".join(updates) + " WHERE usuario_id = %s"
            values.append(usuario_id)
            
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n❌ Error al actualizar el usuario: {e}")
            self.connection.rollback()
            return False

    def eliminar_usuario(self, usuario_id):
        try:
            query = "DELETE FROM USUARIOS WHERE usuario_id = %s"
            self.cursor.execute(query, (usuario_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            if e.errno == 1452 or e.errno == 1451:
                print("\n❌ Error: No se puede eliminar el usuario. Está vinculado como Administrador de un Entrenador o tiene reservas/pases.")
            else:
                print(f"\n❌ Error al eliminar el usuario: {e}")
            self.connection.rollback()
            return False

    def cambiar_rol(self, usuario_id, nuevo_rol): 
        try:
            rol_busqueda = nuevo_rol.lower().strip()
            self.cursor.execute("SELECT rol_id FROM ROLES WHERE nombre_rol = %s", (rol_busqueda,))
            rol_id_data = self.cursor.fetchone()
            if not rol_id_data:
                print(f"\n❌ Rol '{rol_busqueda}' no encontrado.")
                return False

            rol_id = rol_id_data['rol_id']
            query = "UPDATE USUARIOS SET rol_id = %s WHERE usuario_id = %s"
            self.cursor.execute(query, (rol_id, usuario_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n❌ Error al actualizar el rol: {e}")
            self.connection.rollback()
            return False
        
    def obtener_entrenador_id_por_admin(self, usuario_admin_id):
        query = "SELECT entrenador_id FROM ENTRENADORES WHERE usuario_admin_id = %s"
        self.cursor.execute(query, (usuario_admin_id,))
        result = self.cursor.fetchone()
        return result['entrenador_id'] if result else None
    
    def registrar_entrenador(self, nick_entrenador, usuario_admin_id):
        try:
            query = """
            INSERT INTO ENTRENADORES (nick_entrenador, fecha_registro, estado_suscripcion, usuario_admin_id)
            VALUES (%s, NOW(), 'Activa', %s)
            """
            self.cursor.execute(query, (nick_entrenador, usuario_admin_id))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"\n❌ Error al registrar el entrenador: {e}")
            self.connection.rollback()
            return None

    def buscar_alumnos_por_entrenador(self, entrenador_id):
        query = """
        SELECT 
            u.usuario_id, u.nombre, u.apellido, u.email, u.telefono, r.nombre_rol
        FROM USUARIOS u
        JOIN ROLES r ON u.rol_id = r.rol_id
        WHERE u.entrenador_vinculado_id = %s
        """
        self.cursor.execute(query, (entrenador_id,))
        return self.cursor.fetchall()
    
    def obtener_datos_alumno(self, usuario_id):
        query = """
        SELECT 
            u.usuario_id, u.nombre, u.apellido, u.email, u.telefono, u.password_hash, u.entrenador_vinculado_id, r.nombre_rol, 
            e.nick_entrenador
        FROM USUARIOS u 
        JOIN ROLES r ON u.rol_id = r.rol_id
        LEFT JOIN ENTRENADORES e ON u.entrenador_vinculado_id = e.entrenador_id
        WHERE u.usuario_id = %s
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchone()
    
    def obtener_conteo_alumnos_por_entrenador(self):
        query = """
        SELECT 
            e.nick_entrenador, 
            COUNT(u.usuario_id) AS total_alumnos
        FROM ENTRENADORES e
        LEFT JOIN USUARIOS u ON u.entrenador_vinculado_id = e.entrenador_id
        GROUP BY e.entrenador_id, e.nick_entrenador
        ORDER BY total_alumnos DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # ----------------------------------------------------
    # Funciones CRUD y Compras para Productos (Tienda)
    # ----------------------------------------------------
    
    def agregar_producto(self, nombre, descripcion, precio, stock):
        try:
            query = """
            INSERT INTO PRODUCTOS (nombre, descripcion, precio_base, stock_actual, fecha_creacion)
            VALUES (%s, %s, %s, %s, NOW())
            """
            values = (nombre, descripcion, precio, stock)
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"\n❌ Error al agregar el producto: {e}")
            self.connection.rollback()
            return False

    def obtener_todos_productos(self):
        query = "SELECT producto_id, nombre, descripcion, precio_base, stock_actual FROM PRODUCTOS ORDER BY nombre"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def actualizar_producto(self, producto_id, **kwargs):
        try:
            updates = []
            values = []
            for key, value in kwargs.items():
                updates.append(f"{key} = %s")
                values.append(value)
            if not updates:
                return False
            query = "UPDATE PRODUCTOS SET " + ", ".join(updates) + " WHERE producto_id = %s"
            values.append(producto_id)
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n❌ Error al actualizar el producto: {e}")
            self.connection.rollback()
            return False

    def eliminar_producto(self, producto_id):
        try:
            query = "DELETE FROM PRODUCTOS WHERE producto_id = %s"
            self.cursor.execute(query, (producto_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"\n❌ Error al eliminar el producto: {e}")
            self.connection.rollback()
            return False
            
    def comprar_producto(self, usuario_id, producto_id, cantidad):
        try:
            self.cursor.execute("SELECT precio_base, stock_actual FROM PRODUCTOS WHERE producto_id = %s", (producto_id,))
            producto = self.cursor.fetchone()
            
            if not producto:
                print("❌ Producto no encontrado.")
                return False
            if producto['stock_actual'] < cantidad:
                print(f"❌ Stock insuficiente. Solo quedan {producto['stock_actual']} unidades.")
                return False
            
            precio_unitario = producto['precio_base']
            subtotal = precio_unitario * cantidad
            
            query_pedido = """
            INSERT INTO PEDIDOS (fecha_pedido, estado_pedido, total, cliente_id)
            VALUES (NOW(), 'Completado', %s, %s)
            """
            self.cursor.execute(query_pedido, (subtotal, usuario_id))
            pedido_id = self.cursor.lastrowid
            
            query_detalle = """
            INSERT INTO DETALLE_PEDIDO (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query_detalle, (pedido_id, producto_id, cantidad, precio_unitario, subtotal))
            
            query_stock = "UPDATE PRODUCTOS SET stock_actual = stock_actual - %s WHERE producto_id = %s"
            self.cursor.execute(query_stock, (cantidad, producto_id))
            
            self.connection.commit()
            return True
        except Error as e:
            print(f"\n❌ Error durante la compra: {e}")
            self.connection.rollback()
            return False

    def listar_compras_usuario(self, usuario_id):
        query = """
        SELECT 
            p.pedido_id, p.fecha_pedido, p.total, dp.cantidad, pr.nombre AS nombre_producto
        FROM PEDIDOS p
        JOIN DETALLE_PEDIDO dp ON p.pedido_id = dp.pedido_id
        JOIN PRODUCTOS pr ON dp.producto_id = pr.producto_id
        WHERE p.cliente_id = %s
        ORDER BY p.fecha_pedido DESC
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()