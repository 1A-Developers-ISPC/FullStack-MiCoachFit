CREATE DATABASE IF NOT EXISTS micoachfit_db;

USE micoachfit_db;

-- Tabla para Roles
CREATE TABLE IF NOT EXISTS roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla para Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    password VARCHAR(20) NOT NULL,
    id_rol INT NOT NULL,
    CONSTRAINT fk_id_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- Insertar roles iniciales
INSERT INTO roles (nombre_rol) VALUES ('admin'), ('usuario')
ON DUPLICATE KEY UPDATE nombre_rol=VALUES(nombre_rol);

-- Insertar usuarios iniciales
INSERT INTO usuarios (nombre, apellido, email, nombre_usuario, telefono, password, id_rol)
VALUES 
	('Maximino', 'Moyano',  'maxi1@email.com', 'maximoyano', '351111111', 'max123', (SELECT id_rol FROM roles WHERE nombre_rol = 'usuario')),
	('Dario', 'Bosque',  'dario1@email.com', 'dariobosque', '351111112', 'dar123', (SELECT id_rol FROM roles WHERE nombre_rol = 'admin'))
ON DUPLICATE KEY UPDATE
    nombre = VALUES(nombre), apellido = VALUES(apellido), email = VALUES(email),
    telefono = VALUES(telefono), password = VALUES(password), id_rol = VALUES(id_rol);
    
-- Para visualizar las tablas
SELECT * FROM usuarios;
SELECT * FROM roles;