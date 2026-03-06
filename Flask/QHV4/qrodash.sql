CREATE DATABASE qrodash;
USE qrodash;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    municipio VARCHAR(100),
    apodo VARCHAR(50),
    foto_perfil VARCHAR(255),
    estado ENUM('activo','inactivo') DEFAULT 'activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE semillas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('fruta','verdura') NOT NULL,
    municipios VARCHAR(255),
    clima ENUM('templado','frío','cálido'),
    vitaminas VARCHAR(10),
    temporada ENUM('primavera','verano','otoño','invierno'),
    imagen VARCHAR(255),
    estado ENUM('activo','inactivo') DEFAULT 'activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE moderadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    rol ENUM('admin','diseñador') NOT NULL,
    foto_perfil VARCHAR(255),
    estado ENUM('activo','inactivo') DEFAULT 'activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contenido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slider ENUM('slider1','slider2','slider3','slider4','slider5') NOT NULL,
    titulo_inicial VARCHAR(150) NOT NULL,
    conector VARCHAR(50),
    titulo_final VARCHAR(150),
    anuncio TEXT,
    notas TEXT,
    imagen VARCHAR(255),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM usuarios;
SELECT * FROM moderadores;
SELECT * FROM semillas;
SELECT * FROM contenido;

ALTER TABLE usuarios MODIFY estado TINYINT(1) DEFAULT 1;
ALTER TABLE moderadores MODIFY estado TINYINT(1) DEFAULT 1;
ALTER TABLE semillas MODIFY estado TINYINT(1) DEFAULT 1;
ALTER TABLE contenido MODIFY estado TINYINT(1) DEFAULT 1;





DELIMITER $$

CREATE FUNCTION nombrecompleto(
    nombre VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100)
)
RETURNS VARCHAR(300)
DETERMINISTIC
BEGIN
    RETURN CONCAT(nombre, ' ', apellido_paterno, ' ', apellido_materno);
END$$

DELIMITER ;

SELECT * FROM usuarios_eliminados;
CREATE TABLE usuarios_eliminados (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    email VARCHAR(150),
    municipio VARCHAR(100),
    apodo VARCHAR(50),
    foto_perfil VARCHAR(255),
    estado TINYINT(1),
    creado_en TIMESTAMP,
    eliminado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER soft_delete_usuario
AFTER UPDATE ON usuarios
FOR EACH ROW
BEGIN
    IF OLD.estado = 1 AND NEW.estado = 0 THEN
        INSERT INTO usuarios_eliminados 
        (id, nombre, apellido_paterno, apellido_materno, email, municipio, apodo, foto_perfil, estado, creado_en)
        VALUES
        (OLD.id, OLD.nombre, OLD.apellido_paterno, OLD.apellido_materno, OLD.email, OLD.municipio, OLD.apodo, OLD.foto_perfil, OLD.estado, OLD.creado_en);
    END IF;
END$$

DELIMITER ;




SELECT * FROM usuarios_eliminados;

DELIMITER $$

CREATE TRIGGER before_delete_usuario
BEFORE DELETE ON usuarios
FOR EACH ROW
BEGIN
    INSERT INTO usuarios_eliminados 
    (id, nombre, apellido_paterno, apellido_materno, email, municipio, apodo, foto_perfil, estado, creado_en)
    VALUES
    (OLD.id, OLD.nombre, OLD.apellido_paterno, OLD.apellido_materno, OLD.email, OLD.municipio, OLD.apodo, OLD.foto_perfil, OLD.estado, OLD.creado_en);
END$$

DELIMITER ;
