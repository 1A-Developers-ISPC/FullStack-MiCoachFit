import re
from usuario import Usuario

class SistemaUsuarios:
    def __init__(self, db):
        self.db = db
    
    # Validaciones

    def validar_nombre_apellido(self, valor):
        return bool(valor.strip())

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
    
    
    # Búsqueda, Registro e Inicio de Sesión
  

    def buscar_usuario(self, email):
        usuario_db = self.db.buscar_usuario(email)
        if usuario_db:
            return Usuario(
                usuario_id=usuario_db['usuario_id'],
                nombre=usuario_db['nombre'],
                apellido=usuario_db['apellido'],
                telefono=usuario_db['telefono'],
                email=usuario_db['email'],
                contrasena=usuario_db['password_hash'], 
                rol=usuario_db['nombre_rol'],
                entrenador_vinculado_id=usuario_db['entrenador_vinculado_id']
            )
        return None

    def registrar_usuario(self, nombre, apellido, email, telefono, contrasena, rol='usuario', entrenador_id=None):
        if not self.validar_nombre_apellido(nombre) or not self.validar_nombre_apellido(apellido):
            print("\n❌ Nombre o apellido no pueden estar vacíos.")
            return False
        if not self.validar_email(email):
            print("\n❌ Email inválido.")
            return False
        if not self.validar_telefono(telefono):
            print("\n❌ Teléfono inválido. Debe contener solo números (7 a 15 dígitos).")
            return False
        if not self.validar_contrasena(contrasena):
            print("\n❌ La contraseña debe tener al menos 6 caracteres y contener letras y números.")
            return False

        return self.db.registrar_usuario(nombre, apellido, email, telefono, contrasena, rol, entrenador_id)


    def iniciar_sesion(self, email, contrasena):
        usuario = self.buscar_usuario(email)
        
        if usuario and usuario.verificar_credenciales(contrasena):
            print(f"\n🔓 Bienvenido, {usuario.nombre} {usuario.apellido} ({usuario.rol.capitalize()})")
            
            if usuario.rol == 'admin':
                self.menu_admin(usuario)
            elif usuario.rol == 'entrenador':
                self.menu_entrenador(usuario)
            else: 
                self.menu_alumno(usuario)
        else:
            print("\n❌ Email o contraseña incorrectos.")

    
    # ----------------------------------------------------
    # 1. MENÚ ADMINISTRADOR 
    # ----------------------------------------------------
    
    def menu_admin(self, usuario_admin):
        while True:
            print("\n--- Menú Administrador ---")
            print("1. Listar todos los usuarios (Admin, Entrenadores, Alumnos)") 
            print("2. Contar alumnos por entrenador") 
            print("3. Registrar nuevo Usuario/Alumno/Entrenador") 
            print("4. Actualizar información de Usuarios") 
            print("5. Eliminar usuarios")
            print("6. Tienda (Gestión de Productos)") 
            print("7. Cerrar sesión")
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                self.mostrar_usuarios()
            elif opcion == '2':
                self.contar_alumnos_por_entrenador()
            elif opcion == '3':
                self.registrar_usuario_admin()
            elif opcion == '4':
                self.modificar_usuario_admin()
            elif opcion == '5':
                self.eliminar_usuario_admin()
            elif opcion == '6':
                self.menu_tienda_admin()
            elif opcion == '7':
                print("\n🔒 Sesión cerrada.")
                break
            else:
                print("\n⚠️ Opción inválida")
                
    
    def contar_alumnos_por_entrenador(self):
        print("\n📊 Conteo de Alumnos vinculados por Entrenador:")
        conteo_db = self.db.obtener_conteo_alumnos_por_entrenador()
        
        if not conteo_db:
            print("No hay entrenadores registrados o no hay alumnos vinculados.")
            return

        for c in conteo_db:
            print(f" - Entrenador: {c['nick_entrenador']} | Total Alumnos: {c['total_alumnos']}")


    def registrar_usuario_admin(self):
        print("\n--- Registro de Nuevo Usuario ---")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Email (será su login): ") 
        telefono = input("Teléfono: ")
        contrasena = input("Contraseña: ")
        rol = input("Rol (admin/entrenador/usuario) [por defecto: usuario]: ").strip().lower() or 'usuario'
        
        if rol not in ['admin', 'entrenador', 'usuario']:
            print("\n❌ Rol ingresado no válido. Usando 'usuario'.")
            rol = 'usuario'

        if self.registrar_usuario(nombre, apellido, email, telefono, contrasena, rol=rol):
            print(f"✅ Usuario con rol '{rol}' registrado exitosamente.")
        else:
            print("❌ No se pudo completar el registro. Revise los mensajes de error.")
            
    
    def menu_tienda_admin(self):
        while True:
            print("\n--- Tienda (Gestión de Productos) ---")
            print("1. Listar todos los productos")
            print("2. Agregar nuevo producto")
            print("3. Actualizar información de producto")
            print("4. Eliminar producto")
            print("5. Volver al menú Administrador")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.listar_productos()
            elif opcion == '2':
                self.agregar_producto()
            elif opcion == '3':
                self.actualizar_producto_admin()
            elif opcion == '4':
                self.eliminar_producto_admin()
            elif opcion == '5':
                break
            else:
                print("\n⚠️ Opción inválida")

    def agregar_producto(self):
        print("\n--- Agregar Nuevo Producto ---")
        nombre = input("Nombre del producto: ")
        descripcion = input("Descripción: ")
        try:
            precio = float(input("Precio base: "))
            stock = int(input("Stock inicial: "))
            if precio <= 0 or stock < 0:
                print("\n❌ El precio debe ser positivo y el stock no puede ser negativo.")
                return
        except ValueError:
            print("\n❌ Precio y/o stock inválido.")
            return

        if self.db.agregar_producto(nombre, descripcion, precio, stock):
             print("✅ Producto agregado exitosamente.")
        else:
             print("❌ Error al agregar el producto a la base de datos.")

    def actualizar_producto_admin(self):
        try:
            producto_id = int(input("Ingrese el ID del producto a actualizar: "))
            
            datos_a_actualizar = {}
            
            nuevo_nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ")
            if nuevo_nombre.strip():
                datos_a_actualizar['nombre'] = nuevo_nombre
            
            nueva_descripcion = input("Nueva descripción (dejar en blanco para no cambiar): ")
            if nueva_descripcion.strip():
                datos_a_actualizar['descripcion'] = nueva_descripcion
                
            nuevo_precio = input("Nuevo precio base (dejar en blanco para no cambiar): ")
            if nuevo_precio.strip():
                try:
                    datos_a_actualizar['precio_base'] = float(nuevo_precio)
                except ValueError:
                    print("\n❌ Precio inválido.")
                    return
            
            nuevo_stock = input("Nuevo stock actual (dejar en blanco para no cambiar): ")
            if nuevo_stock.strip():
                try:
                    datos_a_actualizar['stock_actual'] = int(nuevo_stock)
                except ValueError:
                    print("\n❌ Stock inválido.")
                    return
                    
            if datos_a_actualizar and self.db.actualizar_producto(producto_id, **datos_a_actualizar):
                print("\n✅ Producto actualizado exitosamente.")
            elif not datos_a_actualizar:
                print("\n📝 No se realizaron cambios.")
            else:
                print("\n❌ No se pudo actualizar el producto.")
                
        except ValueError:
            print("\n❌ ID inválido.")
            
    def eliminar_producto_admin(self):
        try:
            producto_id = int(input("Ingrese el ID del producto a eliminar: "))
            if self.db.eliminar_producto(producto_id):
                print("\n✅ Producto eliminado exitosamente.")
            else:
                print("\n❌ No se pudo eliminar el producto o el ID no existe.")
        except ValueError:
            print("\n❌ ID inválido.")

    def mostrar_usuarios(self):
        print("\n📋 Lista de usuarios:")
        usuarios_db = self.db.obtener_todos_usuarios()
        for u in usuarios_db:
            entrenador_nick = f"Entrenador: {u['nick_entrenador']}" if u['nick_entrenador'] else ""
            print(f" - ID: {u['usuario_id']} | {u['nombre']} {u['apellido']} | Email: {u['email']} | Rol: {u['nombre_rol']} | {entrenador_nick}")

    def modificar_usuario_admin(self):
        try:
            usuario_id = int(input("Ingrese el ID del usuario a modificar: "))
        except ValueError:
            print("\n❌ ID inválido.")
            return

        usuario_db = self.db.obtener_datos_alumno(usuario_id)
        if not usuario_db:
            print("\n❌ Usuario no encontrado.")
            return

        print(f"\n--- Editando Usuario ID: {usuario_id} ({usuario_db['email']}) ---")
        
        datos_a_actualizar = self._pedir_datos_para_edicion(usuario_db)
        
        nuevo_rol = input(f"Nuevo rol (Actual: {usuario_db['nombre_rol']}) [admin/entrenador/usuario] (dejar en blanco para no cambiar): ").strip().lower()
        if nuevo_rol and nuevo_rol in ['admin', 'entrenador', 'usuario']:
            if self.db.cambiar_rol(usuario_id, nuevo_rol):
                print(f"✅ Rol cambiado a '{nuevo_rol}'.")
            else:
                print("❌ No se pudo cambiar el rol.")
        elif nuevo_rol:
             print("⚠️ Rol no válido o sin cambios.")

        if datos_a_actualizar:
            if self.db.actualizar_usuario(usuario_id, **datos_a_actualizar):
                print("✅ Datos personales actualizados exitosamente.")
            else:
                print("❌ No se pudo actualizar los datos personales.")
        else:
            print("📝 No se realizaron cambios en los datos personales.")

    def eliminar_usuario_admin(self):
        try:
            usuario_id_eliminar = int(input("Ingrese el ID (usuario_id) del usuario a eliminar: ")) 
            if self.db.eliminar_usuario(usuario_id_eliminar):
                print("\n✅ Usuario eliminado.")
            else:
                print("\n❌ No se pudo eliminar el usuario. El ID no existe o está vinculado como Admin de Entrenador.")
        except ValueError:
            print("\n❌ Por favor, ingrese un número de ID válido.")
            
    
    # ----------------------------------------------------
    # 2. MENÚ ENTRENADOR
    # ----------------------------------------------------

    def menu_entrenador(self, entrenador_usuario):
        entrenador_id = self.db.obtener_entrenador_id_por_admin(entrenador_usuario.usuario_id)
        if not entrenador_id:
            print("\n❌ Este usuario 'entrenador' no tiene un registro en la tabla ENTRENADORES.")
            return

        while True:
            print("\n--- Menú Entrenador ---")
            print("1. Ver mis datos personales")
            print("2. Modificar mis datos personales")
            print("3. Listar mis alumnos")
            print("4. Editar información de alumnos")
            print("5. Eliminar alumnos")
            print("6. Tienda (Ver/Comprar/Mis Compras)")
            print("7. Cerrar sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.ver_perfil_alumno(entrenador_usuario.usuario_id)
            elif opcion == '2':
                self.editar_perfil_personal(entrenador_usuario)
                entrenador_usuario = self.buscar_usuario(entrenador_usuario.email)
            elif opcion == '3':
                self.listar_alumnos(entrenador_id)
            elif opcion == '4':
                self.modificar_alumno(entrenador_id)
            elif opcion == '5':
                self.eliminar_alumno(entrenador_id)
            elif opcion == '6':
                self.menu_tienda_compras(entrenador_usuario)
            elif opcion == '7':
                print("\n🔒 Sesión cerrada.")
                break
            else:
                print("\n⚠️ Opción inválida")


    def editar_perfil_personal(self, usuario):
        print("\n--- Editar Perfil Personal ---")
        print("Deje el campo en blanco si no desea modificarlo.")
        
        datos_a_actualizar = self._pedir_datos_para_edicion(usuario)

        if datos_a_actualizar:
            if self.db.actualizar_usuario(usuario.usuario_id, **datos_a_actualizar):
                print("\n✅ Perfil actualizado exitosamente.")
            else:
                print("\n❌ No se pudo actualizar el perfil.")
        else:
            print("\n📝 No se realizaron cambios en el perfil.")


    def listar_alumnos(self, entrenador_id):
        alumnos_db = self.db.buscar_alumnos_por_entrenador(entrenador_id)
        print(f"\n📋 Lista de Alumnos vinculados (Entrenador ID: {entrenador_id}):")
        if not alumnos_db:
            print("No hay alumnos vinculados a este entrenador.")
            return

        for u in alumnos_db:
            print(f" - ID: {u['usuario_id']} | {u['nombre']} {u['apellido']} | Email: {u['email']} | Rol: {u['nombre_rol']}")

    def modificar_alumno(self, entrenador_id):
        try:
            usuario_id = int(input("Ingrese el ID del alumno a modificar: "))
        except ValueError:
            print("\n❌ ID inválido.")
            return

        alumno_db = self.db.obtener_datos_alumno(usuario_id)
        
        if not alumno_db or alumno_db.get('entrenador_vinculado_id') != entrenador_id:
            print("\n❌ Alumno no encontrado o no está vinculado a su cuenta.")
            return

        if alumno_db['nombre_rol'].lower().strip() != 'usuario':
            print("\n⚠️ Solo puede modificar usuarios con rol 'usuario' (Alumnos).")
            return
            
        print(f"\n--- Editando Alumno ID: {usuario_id} ({alumno_db['email']}) ---")
        
        datos_a_actualizar = self._pedir_datos_para_edicion(alumno_db)
        
        if datos_a_actualizar:
            if self.db.actualizar_usuario(usuario_id, **datos_a_actualizar):
                print("✅ Datos del alumno actualizados exitosamente.")
            else:
                print("❌ No se pudo actualizar los datos del alumno.")
        else:
            print("📝 No se realizaron cambios en el perfil del alumno.")

    def eliminar_alumno(self, entrenador_id):
        try:
            usuario_id_eliminar = int(input("Ingrese el ID del alumno a eliminar: "))
        except ValueError:
            print("\n❌ Por favor, ingrese un número de ID válido.")
            return
            
        alumno_db = self.db.obtener_datos_alumno(usuario_id_eliminar)

        if not alumno_db or alumno_db.get('entrenador_vinculado_id') != entrenador_id:
            print("\n❌ Alumno no encontrado o no está vinculado a su cuenta.")
            return
        
        if alumno_db['nombre_rol'].lower().strip() != 'usuario':
            print("\n⚠️ Solo puede eliminar usuarios con rol 'usuario' (Alumnos).")
            return

        if self.db.eliminar_usuario(usuario_id_eliminar):
            print("\n✅ Alumno eliminado.")
        else:
            print("\n❌ No se pudo eliminar el alumno.")
            
    
    # ----------------------------------------------------
    # 3. MENÚ ALUMNO (USUARIO)
    # ----------------------------------------------------

    def menu_alumno(self, usuario):
        while True:
            print(f"\n--- Menú Alumno ---")
            print(f"1. Ver mi perfil y entrenador")
            print(f"2. Editar mis datos personales")
            print(f"3. Entrar a la Tienda (Ver/Comprar/Mis Compras)")
            print(f"4. Cerrar sesión")
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                self.ver_perfil_alumno(usuario.usuario_id)
            elif opcion == '2':
                self.editar_perfil_personal(usuario)
                usuario_actualizado = self.buscar_usuario(usuario.email)
                if usuario_actualizado:
                    usuario = usuario_actualizado
            elif opcion == '3':
                self.menu_tienda_compras(usuario)
            elif opcion == '4':
                print("\n🔒 Sesión cerrada.")
                break
            else:
                print("\n⚠️ Opción inválida")

    def ver_perfil_alumno(self, usuario_id):
        usuario_db = self.db.obtener_datos_alumno(usuario_id)
        if not usuario_db:
            print("Error al cargar perfil.")
            return
            
        entrenador_nick = usuario_db['nick_entrenador'] if usuario_db['nick_entrenador'] else "No vinculado"

        print(f"\nNombre: {usuario_db['nombre']} {usuario_db['apellido']}")
        print(f"Email (Login): {usuario_db['email']}")
        print(f"Teléfono: {usuario_db['telefono']}")
        print(f"Rol: {usuario_db['nombre_rol']}")
        print(f"Entrenador: {entrenador_nick}")

    
    # ----------------------------------------------------
    # Funciones de Tienda (Comunes)
    # ----------------------------------------------------

    def menu_tienda_compras(self, usuario):
        while True:
            print(f"\n--- Tienda (Usuario: {usuario.nombre}) ---")
            print("1. Listar productos disponibles")
            print("2. Comprar un producto")
            print("3. Listar mis productos comprados")
            print("4. Volver al menú anterior")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.listar_productos()
            elif opcion == '2':
                self.realizar_compra(usuario.usuario_id)
            elif opcion == '3':
                self.listar_compras(usuario.usuario_id)
            elif opcion == '4':
                break
            else:
                print("\n⚠️ Opción inválida")
                
    def realizar_compra(self, usuario_id):
        self.listar_productos()
        try:
            producto_id = int(input("Ingrese el ID del producto a comprar: "))
            cantidad = int(input("Ingrese la cantidad: "))
            
            if cantidad <= 0:
                print("❌ La cantidad debe ser mayor a cero.")
                return

            if self.db.comprar_producto(usuario_id, producto_id, cantidad):
                print("\n✅ Compra realizada con éxito.")
            else:
                print("\n❌ Error al procesar la compra. (Verifique ID/Stock)")
                
        except ValueError:
            print("\n❌ ID y/o cantidad inválida.")

    def listar_compras(self, usuario_id):
        print("\n🧾 Mis Compras Realizadas:")
        compras_db = self.db.listar_compras_usuario(usuario_id)
        
        if not compras_db:
            print("No ha realizado ninguna compra.")
            return
            
        for c in compras_db:
            fecha = c['fecha_pedido'].strftime('%Y-%m-%d %H:%M')
            print(f" - Pedido ID: {c['pedido_id']} | Producto: {c['nombre_producto']} | Cantidad: {c['cantidad']} | Total: ${c['total']:.2f} | Fecha: {fecha}")

    def listar_productos(self):
        print("\n📦 Lista de Productos:")
        productos_db = self.db.obtener_todos_productos()
        if not productos_db:
            print("No hay productos registrados en la tienda.")
            return
        
        for p in productos_db:
            print(f" - ID: {p['producto_id']} | {p['nombre']} | Precio: ${p['precio_base']:.2f} | Stock: {p['stock_actual']}")


    # ----------------------------------------------------
    # Funciones Auxiliares
    # ----------------------------------------------------

    def _pedir_datos_para_edicion(self, usuario_o_db_dict):
        """Función auxiliar para pedir y validar datos comunes de edición."""
        datos_a_actualizar = {}
        
        nombre_actual = getattr(usuario_o_db_dict, 'nombre', usuario_o_db_dict.get('nombre'))
        apellido_actual = getattr(usuario_o_db_dict, 'apellido', usuario_o_db_dict.get('apellido'))
        telefono_actual = getattr(usuario_o_db_dict, 'telefono', usuario_o_db_dict.get('telefono'))
        
        nuevo_nombre = input(f"Nombre (Actual: {nombre_actual}): ")
        if nuevo_nombre.strip() and self.validar_nombre_apellido(nuevo_nombre):
            datos_a_actualizar['nombre'] = nuevo_nombre

        nuevo_apellido = input(f"Apellido (Actual: {apellido_actual}): ")
        if nuevo_apellido.strip() and self.validar_nombre_apellido(nuevo_apellido):
            datos_a_actualizar['apellido'] = nuevo_apellido

        nuevo_telefono = input(f"Teléfono (Actual: {telefono_actual}): ")
        if nuevo_telefono.strip() and self.validar_telefono(nuevo_telefono):
            datos_a_actualizar['telefono'] = nuevo_telefono
        elif nuevo_telefono.strip():
            print("\n⚠️ Teléfono no válido. ")
            
        nuevo_contrasena = input("Nueva contraseña (dejar en blanco para no cambiar): ")
        if nuevo_contrasena.strip() and self.validar_contrasena(nuevo_contrasena):
            datos_a_actualizar['contrasena'] = nuevo_contrasena 
        elif nuevo_contrasena.strip():
            print("\n⚠️ Contraseña no válida. ")
            
        return datos_a_actualizar