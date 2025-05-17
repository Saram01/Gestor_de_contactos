

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL
);

CREATE TABLE contacto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    categoria VARCHAR(30),
    email VARCHAR(100) UNIQUE, 
    telefono VARCHAR(20) UNIQUE, 
    usuario_id INTEGER NOT NULL,
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE 
);

INSERT INTO usuario (nombre_usuario, email, contrasena) VALUES
('joel', 'joel@correo.com', 'contraseña_segura123'),
('maryjane', 'maryjane@correo.com', 'contraseña_segura456'),
('peterparker', 'peterparker@correo.com', 'contraseña_segura789'),
('Danteinferno', 'danteinferno@correo.com', 'dante123000'),
('Spartan', 'spartan@correo.com', 'halo2025');

INSERT INTO contacto (nombre, categoria, email, telefono, usuario_id) VALUES
('Juan Pérez', 'Amigos', 'juanperez@example.com', '1234567890', 1),
('Ana González', 'Familia', 'anagonzalez@example.com', '0987654321', 2),
('Carlos López', 'Trabajo', 'carloslopez@example.com', '1122334455', 3),
('María Rodríguez', 'Amigos', 'mariarodriguez@example.com', '2233445566', 1),
('Luis Hernández', 'Trabajo', 'luishernandez@example.com', '3344556677', 2),
('Gabriela Hurtado', 'Familia', 'gabriela123@correo.com', '3213332211', 3);