-- 001_esquema.sql — Motor de reservas · esquema inicial
-- Los Corrales de Rota · 2026-07-23
-- Ver docs/reservas-arquitectura.md § 3. Se aplica con `php migrar.php`.
--
-- Convenciones: InnoDB + utf8mb4, claves foráneas explícitas, fechas y horas
-- separadas (el panel trabaja por día), JSON guardado en TEXT por compatibilidad
-- con MariaDB antiguas de hosting compartido.

CREATE TABLE tipos_visita (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  clave         VARCHAR(40)  NOT NULL,
  activo        TINYINT(1)   NOT NULL DEFAULT 1,
  duracion_min  SMALLINT UNSIGNED NOT NULL DEFAULT 60,
  aforo_defecto SMALLINT UNSIGNED NOT NULL DEFAULT 25,
  orden         SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  creado        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_tipos_clave (clave)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tipos_visita_i18n (
  tipo_id     INT UNSIGNED NOT NULL,
  idioma      CHAR(2)      NOT NULL,
  nombre      VARCHAR(120) NOT NULL,
  descripcion TEXT         NULL,
  incluye     TEXT         NULL,
  notas       TEXT         NULL,
  PRIMARY KEY (tipo_id, idioma),
  CONSTRAINT fk_i18n_tipo FOREIGN KEY (tipo_id) REFERENCES tipos_visita (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Un día abierto de un tipo de visita. Lo abre el equipo a mano; no hay cálculo
-- de mareas que lo decida (decisión 2026-07-23).
CREATE TABLE dias (
  id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
  tipo_id INT UNSIGNED NOT NULL,
  fecha   DATE         NOT NULL,
  estado  ENUM('abierto','cancelado') NOT NULL DEFAULT 'abierto',
  nota    VARCHAR(255) NULL,
  creado  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_dias_tipo_fecha (tipo_id, fecha),
  KEY ix_dias_fecha (fecha),
  CONSTRAINT fk_dias_tipo FOREIGN KEY (tipo_id) REFERENCES tipos_visita (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- plazas_ocupadas es campo materializado, NO un COUNT al vuelo: es la fila que se
-- bloquea con SELECT ... FOR UPDATE al reservar. Ver Db::bloquearPase().
CREATE TABLE pases (
  id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dia_id          INT UNSIGNED NOT NULL,
  hora_inicio     TIME         NOT NULL,
  hora_fin        TIME         NULL,
  aforo           SMALLINT UNSIGNED NOT NULL,
  plazas_ocupadas SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  idioma_guia     CHAR(2)      NULL,
  estado          ENUM('abierto','cerrado','anulado') NOT NULL DEFAULT 'abierto',
  creado          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_pases_dia_hora (dia_id, hora_inicio),
  KEY ix_pases_estado (estado),
  CONSTRAINT fk_pases_dia FOREIGN KEY (dia_id) REFERENCES dias (id) ON DELETE CASCADE,
  CONSTRAINT ck_pases_aforo CHECK (plazas_ocupadas <= aforo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- origen: 'web' la hace el visitante, 'panel' la apunta el equipo (teléfono o
-- mostrador). Ambas descuentan plazas igual.
CREATE TABLE reservas (
  id             INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pase_id        INT UNSIGNED NOT NULL,
  localizador    CHAR(8)      NOT NULL,
  nombre         VARCHAR(120) NOT NULL,
  email          VARCHAR(190) NOT NULL,
  telefono       VARCHAR(40)  NULL,
  personas       TINYINT UNSIGNED NOT NULL,
  idioma         CHAR(2)      NOT NULL DEFAULT 'es',
  estado         ENUM('pendiente','confirmada','cancelada','anulada','caducada') NOT NULL DEFAULT 'pendiente',
  token_gestion  CHAR(43)     NOT NULL,
  origen         ENUM('web','panel') NOT NULL DEFAULT 'web',
  consentimiento TINYINT(1)   NOT NULL DEFAULT 0,
  ip             VARBINARY(16) NULL,
  creada         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expira         DATETIME     NULL,
  confirmada     DATETIME     NULL,
  cancelada      DATETIME     NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_reservas_localizador (localizador),
  UNIQUE KEY uq_reservas_token (token_gestion),
  KEY ix_reservas_pase_estado (pase_id, estado),
  KEY ix_reservas_email (email),
  KEY ix_reservas_expira (estado, expira),
  CONSTRAINT fk_reservas_pase FOREIGN KEY (pase_id) REFERENCES pases (id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Código de 6 dígitos que confirma la reserva. Tres intentos y caduca.
CREATE TABLE codigos (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  reserva_id INT UNSIGNED NOT NULL,
  codigo     CHAR(6)      NOT NULL,
  expira     DATETIME     NOT NULL,
  intentos   TINYINT UNSIGNED NOT NULL DEFAULT 0,
  usado      TINYINT(1)   NOT NULL DEFAULT 0,
  creado     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY ix_codigos_reserva (reserva_id, usado),
  CONSTRAINT fk_codigos_reserva FOREIGN KEY (reserva_id) REFERENCES reservas (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Nada se envía dentro de la petición: se encola y lo manda el cron.
CREATE TABLE correo_cola (
  id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
  destinatario    VARCHAR(190) NOT NULL,
  idioma          CHAR(2)      NOT NULL DEFAULT 'es',
  plantilla       VARCHAR(40)  NOT NULL,
  datos           TEXT         NULL,
  estado          ENUM('pendiente','enviado','fallido') NOT NULL DEFAULT 'pendiente',
  intentos        TINYINT UNSIGNED NOT NULL DEFAULT 0,
  ultimo_error    VARCHAR(255) NULL,
  programado_para DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  creado          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  enviado         DATETIME     NULL,
  PRIMARY KEY (id),
  KEY ix_cola_pendientes (estado, programado_para)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuarios (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  usuario       VARCHAR(60)  NOT NULL,
  hash          VARCHAR(255) NOT NULL,
  nombre        VARCHAR(120) NOT NULL,
  rol           ENUM('gestor','mostrador') NOT NULL DEFAULT 'mostrador',
  activo        TINYINT(1)   NOT NULL DEFAULT 1,
  ultimo_acceso DATETIME     NULL,
  creado        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_usuarios_usuario (usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE auditoria (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  usuario_id INT UNSIGNED NULL,
  accion     VARCHAR(60)  NOT NULL,
  entidad    VARCHAR(40)  NOT NULL,
  entidad_id INT UNSIGNED NULL,
  detalle    TEXT         NULL,
  ip         VARBINARY(16) NULL,
  creado     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY ix_auditoria_entidad (entidad, entidad_id),
  CONSTRAINT fk_auditoria_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Informativa: la hora de bajamar a la vista del gestor en el calendario.
-- No valida, no bloquea, no propone. Ninguna otra tabla depende de esta.
CREATE TABLE mareas (
  fecha     DATE NOT NULL,
  hora      TIME NOT NULL,
  tipo      ENUM('pleamar','bajamar') NOT NULL,
  altura_m  DECIMAL(3,2) NULL,
  PRIMARY KEY (fecha, hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Primer tipo del catálogo: la visita a los corrales.
INSERT INTO tipos_visita (clave, activo, duracion_min, aforo_defecto, orden)
VALUES ('corrales', 1, 60, 25, 1);

INSERT INTO tipos_visita_i18n (tipo_id, idioma, nombre, descripcion) VALUES
  (1, 'es', 'La visita a los corrales', 'Una hora dentro del Monumento Natural, a pie, guiada por los corraleros.'),
  (1, 'en', 'The corrales guided visit', 'One hour inside the Natural Monument, on foot, guided by the corraleros.'),
  (1, 'de', 'Führung durch die Corrales', 'Eine Stunde zu Fuß im Naturdenkmal, geführt von den Corraleros.'),
  (1, 'fr', 'La visite des corrales', 'Une heure à pied dans le Monument Naturel, guidée par les corraleros.');
