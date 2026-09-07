CREATE DATABASE IF NOT EXISTS comercial;
USE comercial;

CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    telefono VARCHAR(9) NOT NULL,
    correo VARCHAR(255) NULL,
    id_rol INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    CONSTRAINT fk_usuarios_rol FOREIGN KEY (id_rol) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    id_categoria INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    CONSTRAINT fk_productos_categoria FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(9) NOT NULL,
    correo VARCHAR(150) NULL,
    direccion VARCHAR(255) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_pago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    id_cliente INT NOT NULL,
    id_usuario INT NOT NULL,
    id_tipo_pago INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    CONSTRAINT fk_ventas_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    CONSTRAINT fk_ventas_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    CONSTRAINT fk_ventas_tipo_pago FOREIGN KEY (id_tipo_pago) REFERENCES tipo_pago(id)
);

CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    CONSTRAINT fk_detalle_venta FOREIGN KEY (id_venta) REFERENCES ventas(id),
    CONSTRAINT fk_detalle_producto FOREIGN KEY (id_producto) REFERENCES productos(id)
);

INSERT INTO roles (id, nombre, descripcion, created_at, updated_at)
SELECT 1, 'Admin', 'Administrador del sistema', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE nombre = 'Admin');

INSERT INTO roles (id, nombre, descripcion, created_at, updated_at)
SELECT 2, 'Vendedor', 'Usuario encargado de realizar ventas', NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE nombre = 'Vendedor');
