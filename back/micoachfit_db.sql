CREATE DATABASE micoachfit_db;
USE micoachfit_db;

-- 1. Tabla ROLES
CREATE TABLE IF NOT EXISTS ROLES (
    rol_id INT NOT NULL AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (rol_id)
) ENGINE=InnoDB;

-- 2. Tabla ENTRENADORES (Suscripción/Agencia/Nick)
CREATE TABLE IF NOT EXISTS ENTRENADORES (
    entrenador_id INT NOT NULL AUTO_INCREMENT,
    -- Nick del entrenador que usan los alumnos para vincularse.
    nick_entrenador VARCHAR(100) NOT NULL UNIQUE, 
    fecha_registro DATETIME NOT NULL,
    estado_suscripcion VARCHAR(50) NOT NULL,
    usuario_admin_id INT NOT NULL, -- FK al usuario persona que gestiona esta suscripción
    PRIMARY KEY (entrenador_id)
) ENGINE=InnoDB;

-- 3. Tabla USUARIOS (Personas)
CREATE TABLE IF NOT EXISTS USUARIOS (
    usuario_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    rol_id INT NOT NULL,
    -- El alumno solo puede vincularse a un entrenador (relación 1:1)
    entrenador_vinculado_id INT NULL, 
    PRIMARY KEY (usuario_id),
    FOREIGN KEY (rol_id) REFERENCES ROLES(rol_id),
    FOREIGN KEY (entrenador_vinculado_id) REFERENCES ENTRENADORES(entrenador_id)
) ENGINE=InnoDB;

-- FK para USUARIO_ADMIN_ID en ENTRENADORES (Dependencia mutua)
ALTER TABLE ENTRENADORES
ADD CONSTRAINT fk_usuario_admin
FOREIGN KEY (usuario_admin_id) REFERENCES USUARIOS(usuario_id);

-- 4. Tabla CLASES (Tipos de entrenamiento - Ej: Funcional Grupal)
CREATE TABLE IF NOT EXISTS CLASES (
    clase_id INT NOT NULL AUTO_INCREMENT,
    nombre_clase VARCHAR(100) NOT NULL,
    descripcion TEXT,
    duracion_minutos INT, 
    -- Se elimina 'precio' ya que la asistencia solo es posible con un pase
    cupos_maximos INT NOT NULL, -- Los cupos son fijos para este tipo de clase
    entrenador_id INT NOT NULL,
    PRIMARY KEY (clase_id),
    FOREIGN KEY (entrenador_id) REFERENCES ENTRENADORES(entrenador_id)
) ENGINE=InnoDB;

-- 5. Tabla HORARIOS (Instancias de clase)
CREATE TABLE IF NOT EXISTS HORARIOS (
    horario_id INT NOT NULL AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    cupos_disponibles INT NOT NULL,
    clase_id INT NOT NULL,
    PRIMARY KEY (horario_id),
    UNIQUE KEY uk_horario_clase (fecha, hora_inicio, clase_id),
    FOREIGN KEY (clase_id) REFERENCES CLASES(clase_id)
) ENGINE=InnoDB;

-- ==================================================================
-- MÓDULO DE GESTIÓN DE PASES
-- ==================================================================

-- 6. Tabla PASES (Definición de tipos de pases/bonos)
CREATE TABLE IF NOT EXISTS PASES (
    pase_id INT NOT NULL AUTO_INCREMENT,
    nombre_pase VARCHAR(100) NOT NULL, -- Ej: Pase Funcional Grupal
    descripcion TEXT,
    clases_incluidas INT NULL, -- Ej: 8 (NULL para ilimitado, aunque el pase es mensual)
    vigencia_dias INT NOT NULL, -- Generalmente 30
    precio DECIMAL(10, 2) NOT NULL,
    entrenador_id INT NOT NULL,
    PRIMARY KEY (pase_id),
    FOREIGN KEY (entrenador_id) REFERENCES ENTRENADORES(entrenador_id)
) ENGINE=InnoDB;

-- 7. Tabla PASES_ADQUIRIDOS (El pase comprado por un alumno, su saldo y estado)
CREATE TABLE IF NOT EXISTS PASES_ADQUIRIDOS (
    pase_adquirido_id INT NOT NULL AUTO_INCREMENT,
    fecha_compra DATETIME NOT NULL,
    fecha_expiracion DATE NOT NULL,
    clases_restantes INT NULL,
    estado VARCHAR(50) NOT NULL,
    pase_id INT NOT NULL,
    usuario_id INT NOT NULL,
    PRIMARY KEY (pase_adquirido_id),
    FOREIGN KEY (pase_id) REFERENCES PASES(pase_id),
    FOREIGN KEY (usuario_id) REFERENCES USUARIOS(usuario_id)
) ENGINE=InnoDB;

-- 8. Tabla PEDIDOS (General para transacciones de Productos o COMPRA DE PASES)
CREATE TABLE IF NOT EXISTS PEDIDOS (
    pedido_id INT NOT NULL AUTO_INCREMENT,
    fecha_pedido DATETIME NOT NULL,
    estado_pedido VARCHAR(50) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    -- Se elimina direccion_envio, ya que la entrega es presencial
    cliente_id INT NOT NULL,
    pase_adquirido_id INT NULL, -- Solo se usa si el pedido fue para comprar un pase
    PRIMARY KEY (pedido_id),
    FOREIGN KEY (cliente_id) REFERENCES USUARIOS(usuario_id),
    FOREIGN KEY (pase_adquirido_id) REFERENCES PASES_ADQUIRIDOS(pase_adquirido_id)
) ENGINE=InnoDB;

-- 9. Tabla RESERVAS (Reserva de cupos de clase)
CREATE TABLE IF NOT EXISTS RESERVAS (
    reserva_id INT NOT NULL AUTO_INCREMENT,
    fecha_reserva DATETIME NOT NULL,
    estado VARCHAR(50) NOT NULL,
    usuario_id INT NOT NULL,
    horario_id INT NOT NULL,
    pase_adquirido_id INT NULL, -- El pase usado para esta reserva (consume 1 clase)
    PRIMARY KEY (reserva_id),
    UNIQUE KEY uk_reserva_unica (usuario_id, horario_id),
    FOREIGN KEY (usuario_id) REFERENCES USUARIOS(usuario_id),
    FOREIGN KEY (horario_id) REFERENCES HORARIOS(horario_id),
    FOREIGN KEY (pase_adquirido_id) REFERENCES PASES_ADQUIRIDOS(pase_adquirido_id)
) ENGINE=InnoDB;

-- 10. Tabla PRODUCTOS (Inventario de artículos físicos)
CREATE TABLE IF NOT EXISTS PRODUCTOS (
    producto_id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_base DECIMAL(10, 2) NOT NULL,
    stock_actual INT NOT NULL,
    fecha_creacion DATETIME NOT NULL,
    PRIMARY KEY (producto_id)
) ENGINE=InnoDB;

-- 11. Tabla DETALLE_PEDIDO (Líneas de pedido para PRODUCTOS)
CREATE TABLE IF NOT EXISTS DETALLE_PEDIDO (
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (pedido_id, producto_id),
    FOREIGN KEY (pedido_id) REFERENCES PEDIDOS(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES PRODUCTOS(producto_id)
) ENGINE=InnoDB;



USE micoachfit_db;

-- ==================================================================
-- I. INSERCIÓN DE ROLES
-- ==================================================================
-- Reinsertamos roles (Admin=1, Entrenador=2, Alumno=3)
INSERT INTO ROLES (nombre_rol) VALUES
('Admin'),
('Entrenador'),
('Alumno');

-- ==================================================================
-- II. INSERCIÓN DE USUARIOS Y ENTRENADORES
-- ==================================================================

-- 1. USUARIO ADMIN (Rol_ID = 1)
INSERT INTO USUARIOS (nombre, apellido, email, password_hash, telefono, rol_id, entrenador_vinculado_id) VALUES
('admin', 'micoachfit', 'admin@micoachfit.com', 'admin123', '1123456789', 1, NULL);
SET @admin_id = LAST_INSERT_ID();


-- 2. USUARIO ENTRENADOR (Rol_ID = 2)
INSERT INTO USUARIOS (nombre, apellido, email, password_hash, telefono, rol_id, entrenador_vinculado_id) VALUES
('Entrenador', '1', 'entrenador1@micoachfit.com', 'entrenador1123', '1198765432', 2, NULL);
SET @entrenador1_usuario_id = LAST_INSERT_ID();


-- 3. CUENTA DE NEGOCIO ENTRENADOR TIAGO (FK a USUARIOS.usuario_id)
-- Usamos 'THCFIT' como nick_entrenador para vincular alumnos
INSERT INTO ENTRENADORES (nick_entrenador, fecha_registro, estado_suscripcion, usuario_admin_id) VALUES
('E1FIT', NOW(), 'Activo', @entrenador1_usuario_id);
SET @entrenador1_entrenador_id = LAST_INSERT_ID();


-- 4. ALUMNOS (Rol_ID = 3) VINCULADOS al Entrenador Tiago
-- Los alumnos tienen la FK entrenador_vinculado_id = @tiago_entrenador_id
INSERT INTO USUARIOS (nombre, apellido, email, password_hash, telefono, rol_id, entrenador_vinculado_id) VALUES
('Maximo', 'Lopez', 'maxi@alumno.com', 'hash_maxi', '1140001000', 3, @entrenador1_entrenador_id),
('Kiara', 'Perez', 'kiara@alumno.com', 'hash_kiara', '1140002000', 3, @entrenador1_entrenador_id),
('Carlos', 'Diaz', 'carlos@alumno.com', 'hash_carlos', '1140003000', 3, @entrenador1_entrenador_id),
('Dario', 'Gómez', 'dario@alumno.com', 'hash_dario', '1140004000', 3, @entrenador1_entrenador_id);



-- ==================================================================
-- III. INSERCIÓN DE PRODUCTOS (Tienda)
-- Todos inician con un stock de 5
-- ==================================================================
INSERT INTO PRODUCTOS (nombre, descripcion, precio_base, stock_actual, fecha_creacion) VALUES
('PowerFuel', 'Bebida energética para atletas con electrolitos y vitaminas.', 4.50, 5, NOW()),
('T-shirt MiCoachFit', 'Camiseta deportiva de microfibra de secado rápido.', 25.00, 5, NOW()),
('ProBar', 'Barra energética de 20 gr. con alto contenido proteico.', 3.75, 5, NOW()),
('Rodillo MiCoachFit', 'Rodillo masajeador de espuma densa para liberación miofascial.', 35.00, 5, NOW()),
('Mat MiCoachFit', 'Colchoneta de alta densidad para ejercicios de piso.', 45.00, 5, NOW()),
('Zapatillas Deportivas MiCoachFit', 'Zapatillas de entrenamiento de alto rendimiento con amortiguación y soporte.', 89.99, 5, NOW());



-- Listar todos los Usuarios --

SELECT
    U.usuario_id,
    U.nombre,
    U.apellido,
    U.email,
    R.nombre_rol AS Rol,
    -- Usamos el nick_entrenador para identificar la agencia vinculada
    IFNULL(E.nick_entrenador, 'Ninguno') AS Entrenador_Vinculado
FROM
    USUARIOS AS U
INNER JOIN
    ROLES AS R ON U.rol_id = R.rol_id
LEFT JOIN
    ENTRENADORES AS E ON U.entrenador_vinculado_id = E.entrenador_id
ORDER BY
    R.nombre_rol, U.apellido;
    



-- Listar todos los Productos --


SELECT
    producto_id,
    nombre AS Producto,
    descripcion,
    precio_base AS Precio,
    stock_actual AS Stock
FROM
    PRODUCTOS
ORDER BY
    producto_id;



-- Listar Alumnos de un Entrenador --


SELECT
    U.usuario_id,
    U.nombre,
    U.apellido,
    U.email,
    E.nick_entrenador AS Entrenador_ID_Vinculado
FROM
    USUARIOS AS U
INNER JOIN
    ROLES AS R ON U.rol_id = R.rol_id
INNER JOIN
    ENTRENADORES AS E ON U.entrenador_vinculado_id = E.entrenador_id
WHERE
    R.nombre_rol = 'Alumno' 
    AND E.nick_entrenador = 'E1FIT' -- Filtra por el nick del entrenador
ORDER BY
    U.apellido;
    
