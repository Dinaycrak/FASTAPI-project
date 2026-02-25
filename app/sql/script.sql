-- Crear base de datos
CREATE DATABASE prueba;


-- Crear tabla
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(20) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    edad INTEGER NOT NULL,
    usuario VARCHAR(20) NOT NULL,
    contrasena VARCHAR(20) NOT NULL,
    id_perfil INTEGER,
    FOREIGN KEY (id_perfil) REFERENCES perfil(id)
);

-- Insertar registro
INSERT INTO usuarios (nombre, apellido, cedula, edad, usuario, contrasena, id_perfil)
VALUES ('pedro', 'perez', '10102020', 30, 'pperez', '12345', 1);

INSERT INTO usuarios (nombre, apellido, cedula, edad, usuario, contrasena, id_perfil)
VALUES ('ana', 'acosta', '10102030', 30, 'aacosta', '12346', 1);

-- CREAR TABLA PERFIL
CREATE TABLE perfil (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    descripcion TEXT NOT NULL
);

-- Insertar registro
INSERT INTO perfil (nombre, descripcion)
VALUES ('administrador', "perfiladministrador");

-- CREAR TABLA CLIENT
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    primer_nombre VARCHAR(20) NOT NULL,
    segundo_nombre VARCHAR(20) NOT NULL,
    primer_apellido VARCHAR(20) NOT NULL,
    segundo_apellido VARCHAR(20) NOT NULL,
    id_tipo_documento INTEGER,
    n_documento VARCHAR(20) NOT NULL,
    correo VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_tipo_documento) REFERENCES tipo_documento(id)
);

INSERT INTO clientes (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, id_tipo_documento, n_documento, correo, telefono)
VALUES ('daniel', 'andres', 'Acosta', 'perez', 1, '10102020', 'danielacosta@gmail.com', '3004050300');

CREATE TABLE tipo_documento (
    id SERIAL PRIMARY KEY,
    nombre_tipo VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL
);

INSERT INTO tipo_documento (nombre_tipo, descripcion)
VALUES ('Cedula de Ciudadania', 'Es el documento que usan los ciudadanos mayores de 18 en colombia.');