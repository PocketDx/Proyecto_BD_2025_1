-- ======================================
-- MODELO RELACIONAL - SISTEMA BIBLIOTECA UNIVERSITARIA
-- ======================================

CREATE DATABASE IF NOT EXISTS Biblioteca
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
USE Biblioteca;

-- ------------------------------------------------------
-- 1. CategoriaLibro
-- ------------------------------------------------------
CREATE TABLE CategoriaLibro (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre_categoria VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 2. Libro
-- ------------------------------------------------------
CREATE TABLE Libro (
  isbn CHAR(13) PRIMARY KEY,
  titulo VARCHAR(255) NOT NULL,
  autor VARCHAR(100) NOT NULL,
  editorial VARCHAR(100),
  anio_publicacion YEAR NOT NULL,
  id_categoria INT,
  CONSTRAINT fk_libro_categoria
    FOREIGN KEY (id_categoria)
    REFERENCES CategoriaLibro(id_categoria)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 3. UbicacionEstanteria
-- ------------------------------------------------------
CREATE TABLE UbicacionEstanteria (
  id_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
  pasillo VARCHAR(10) NOT NULL,
  estante VARCHAR(10) NOT NULL,
  nivel   VARCHAR(10) NOT NULL,
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 4. EstadoCopia
-- ------------------------------------------------------
CREATE TABLE EstadoCopia (
  id_estado INT AUTO_INCREMENT PRIMARY KEY,
  id_copia INT NOT NULL,
  estado ENUM('Disponible', 'Prestado', 'Reservado') NOT NULL,
  fecha_estado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT fk_estado_copia
    FOREIGN KEY (id_copia)
    REFERENCES Copia(id_copia)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Trigger para actualizar el estado de la copia
DELIMITER $$

CREATE TRIGGER trg_actualizar_estado_copia
AFTER INSERT ON EstadoCopia
FOR EACH ROW
BEGIN
  UPDATE Copia
  SET estado_actual = NEW.estado
  WHERE id_copia = NEW.id_copia;
END$$

DELIMITER ;

-- ------------------------------------------------------
-- 5. Copia
-- ------------------------------------------------------
CREATE TABLE Copia (
  id_copia INT AUTO_INCREMENT PRIMARY KEY,
  isbn CHAR(13) NOT NULL,
  codigo_interno VARCHAR(30) NOT NULL UNIQUE,
  id_ubicacion INT NOT NULL,
  estado_actual ENUM('Disponible','Prestado','Reservado') NOT NULL DEFAULT 'Disponible',
  CONSTRAINT fk_copia_libro
    FOREIGN KEY (isbn)
    REFERENCES Libro(isbn)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_copia_ubicacion
    FOREIGN KEY (id_ubicacion)
    REFERENCES UbicacionEstanteria(id_ubicacion)
    ON DELETE RESTRICT
    ON UPDATE CASCADE

) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 6. Usuario
-- ------------------------------------------------------
CREATE TABLE Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(100) NOT NULL UNIQUE,
  identificacion VARCHAR(20) NOT NULL UNIQUE,
  tipo_usuario ENUM('Estudiante','Docente') NOT NULL,
  fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
  estado ENUM('Activo','Bloqueado') NOT NULL DEFAULT 'Activo',
  saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00
  
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 7. Prestamo
-- ------------------------------------------------------
CREATE TABLE Prestamo (
  id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_copia INT NOT NULL,
  fecha_prestamo DATE NOT NULL DEFAULT CURRENT_DATE,
  fecha_limite DATE NOT NULL,
  estado ENUM('Activo','Devuelto','Retrasado') NOT NULL DEFAULT 'Activo',
  costo DECIMAL(10,2) NOT NULL DEFAULT 5000.00,
  CONSTRAINT fk_prestamo_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_prestamo_copia
    FOREIGN KEY (id_copia)
    REFERENCES Copia(id_copia)
    ON DELETE CASCADE
    ON UPDATE CASCADE

) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 8. Devolucion
-- ------------------------------------------------------
CREATE TABLE Devolucion (
  id_devolucion INT AUTO_INCREMENT PRIMARY KEY,
  id_prestamo INT NOT NULL UNIQUE,
  fecha_devolucion DATE NOT NULL,
  dias_retraso INT NOT NULL DEFAULT 0 CHECK (dias_retraso >= 0),
  monto_multa DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  CONSTRAINT fk_devolucion_prestamo
    FOREIGN KEY (id_prestamo)
    REFERENCES Prestamo(id_prestamo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 9. TipoMulta
-- ------------------------------------------------------
CREATE TABLE TipoMulta (
  id_tipo_multa INT AUTO_INCREMENT PRIMARY KEY,
  descripcion VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 10. Multa
-- ------------------------------------------------------
CREATE TABLE Multa (
  id_multa INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_tipo_multa INT NOT NULL,
  fecha DATE NOT NULL DEFAULT CURRENT_DATE,
  monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
  CONSTRAINT fk_multa_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_multa_tipo
    FOREIGN KEY (id_tipo_multa)
    REFERENCES TipoMulta(id_tipo_multa)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 11. Reserva
-- ------------------------------------------------------
CREATE TABLE Reserva (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  isbn CHAR(13) NOT NULL,
  fecha_reserva DATE NOT NULL DEFAULT CURRENT_DATE,
  activa BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT fk_reserva_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_reserva_libro
    FOREIGN KEY (isbn)
    REFERENCES Libro(isbn)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 12. TipoPago
-- ------------------------------------------------------
CREATE TABLE TipoPago (
  id_tipo_pago INT AUTO_INCREMENT PRIMARY KEY,
  descripcion VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 13. Pago
-- ------------------------------------------------------
CREATE TABLE Pago (
  id_pago INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_tipo_pago INT NOT NULL,
  fecha DATE NOT NULL DEFAULT CURRENT_DATE,
  monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
  CONSTRAINT fk_pago_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_pago_tipo
    FOREIGN KEY (id_tipo_pago)
    REFERENCES TipoPago(id_tipo_pago)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 14. ReposicionLibro
-- ------------------------------------------------------
CREATE TABLE ReposicionLibro (
  id_reposicion INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_copia INT NOT NULL,
  fecha DATE NOT NULL DEFAULT CURRENT_DATE,
  monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
  CONSTRAINT fk_reposicion_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_reposicion_copia
    FOREIGN KEY (id_copia)
    REFERENCES Copia(id_copia)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 15. Rol
-- ------------------------------------------------------
CREATE TABLE Rol (
  id_rol INT AUTO_INCREMENT PRIMARY KEY,
  nombre_rol ENUM('Administrador','Bibliotecario','Asistente')
    NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 16. Empleado
-- ------------------------------------------------------
CREATE TABLE Empleado (
  id_empleado INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  usuario VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(255) NOT NULL,
  id_rol INT NOT NULL,
  CONSTRAINT fk_empleado_rol
    FOREIGN KEY (id_rol)
    REFERENCES Rol(id_rol)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 17. SesionAuditoria
-- ------------------------------------------------------
CREATE TABLE SesionAuditoria (
  id_sesion INT AUTO_INCREMENT PRIMARY KEY,
  id_empleado INT NOT NULL,
  inicio_sesion DATETIME NOT NULL,
  fin_sesion DATETIME,
  CONSTRAINT fk_sesion_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES Empleado(id_empleado)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 18. Auditoria
-- ------------------------------------------------------
CREATE TABLE Auditoria (
  id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion INT NOT NULL,
  tabla_afectada VARCHAR(50) NOT NULL,
  accion ENUM('INSERT','UPDATE','DELETE') NOT NULL,
  registro_id INT NOT NULL,
  fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_auditoria_sesion
    FOREIGN KEY (id_sesion)
    REFERENCES SesionAuditoria(id_sesion)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 19. Informe
-- ------------------------------------------------------
CREATE TABLE Informe (
  id_informe INT AUTO_INCREMENT PRIMARY KEY,
  tipo ENUM('Libros más prestados',
            'Usuarios con más multas',
            'Inventario',
            'Estado reservas',
            'Préstamos retrasados') NOT NULL,
  periodo DATE NOT NULL,
  generado_por INT NOT NULL,
  detalles TEXT,
  CONSTRAINT fk_informe_empleado
    FOREIGN KEY (generado_por)
    REFERENCES Empleado(id_empleado)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------
-- 20. HistorialAcciones
-- ------------------------------------------------------
CREATE TABLE HistorialAcciones (
  id_historial INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  accion ENUM('Préstamo','Multa','Devolución') NOT NULL,
  fecha DATE NOT NULL DEFAULT CURRENT_DATE,
  detalle TEXT,
  CONSTRAINT fk_historial_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;
