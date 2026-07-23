# Arquitectura del motor de reservas — Los Corrales de Rota

> Cómo se implementa la app de reservas. El **qué** (funcional) está cerrado desde el
> 2026-07-22 en `02-DECISIONES.md`; este documento es el **cómo**, acordado el 2026-07-23.
> **Ámbito:** solo la app del subdominio. La web estática no se toca.
> Última revisión: 2026-07-23

---

## Resumen

App a medida en el subdominio `reservas.loscorralesderota.com`, aislada del sitio estático.
Gratis, sin pasarela. La disponibilidad la fija el equipo a mano: **no hay cálculo de mareas
que decida nada**. La marea es información de apoyo, y va al final del desarrollo.

## 1. Plataforma

**PHP 8 + MySQL/MariaDB en el mismo hosting compartido, sin framework, sin build.**

Motivo: el hosting ya sirve PHP (`contacto.php`) y **está confirmado que el plan incluye MySQL,
cron y SMTP autenticado**. Un VPS con Node o Python añadiría coste y, sobre todo, un servidor
que alguien tendría que parchear; la asociación no tiene quien lo haga. Con PHP el mantenimiento
del sistema operativo es del hosting.

- Subdominio propio con su carpeta y su base de datos. Si la app cae, la web sigue en pie.
- Acceso a datos con **PDO y sentencias preparadas**. Sin ORM.
- Plan B si algún día falta MySQL o cron: SQLite fuera del *docroot* y disparo de tareas al
  final de la petición. El cambio queda en el DSN porque toda la BD pasa por `Db.php`.

## 2. Estructura del código

```
reservas/                      (mismo repo; build.py ignora esta carpeta)
├── public/                    ← docroot del subdominio
│   ├── index.php              front controller público
│   ├── admin.php              front controller del panel
│   └── assets/                base.css (marca verbatim) + logo
├── src/
│   ├── Router.php             enrutado mínimo por patrón
│   ├── Db.php                 PDO
│   ├── Disponibilidad.php     días, pases, aforo, creación en lote
│   ├── Reserva.php            máquina de estados
│   ├── Correo.php             transporte + cola
│   ├── Auth.php               sesión y roles
│   ├── I18n.php               strings por idioma
│   └── Mareas.php             solo consulta informativa (fase 6)
├── vistas/                    plantillas PHP (público y panel)
├── idiomas/{es,en,de,fr}.php  interfaz y plantillas de email
├── migraciones/               001_esquema.sql, 002_… numeradas
├── cron/                      caducar.php · enviar_correo.php · backup.php
├── config.example.php         versionado; el real vive en el servidor, gitignored
└── tests/                     aforo, estados, envío
```

`config.php` con las credenciales de BD y SMTP **nunca entra en git**.

## 3. Modelo de datos

- `tipos_visita` — `activo`, `duracion_min`, `aforo_defecto`, `orden`.
- `tipos_visita_i18n` — nombre, descripción, qué incluye, notas, por idioma. Dar de alta otra
  joya es insertar filas, no tocar código.
- `dias` — `tipo_id`, `fecha`, `estado` (abierto/cancelado), `nota`.
- `pases` — `dia_id`, `hora_inicio`, `hora_fin`, `aforo`, `plazas_ocupadas`, `idioma_guia`,
  `estado`.
- `reservas` — `pase_id`, `localizador`, nombre, email, teléfono, `personas`, `idioma`,
  `estado`, `token_gestion`, `origen` (web/panel), consentimiento, marcas de tiempo.
- `codigos` — código de 6 dígitos, caducidad, intentos.
- `correo_cola` — destinatario, plantilla, datos, intentos, estado.
- `usuarios` y `auditoria` — quién anuló qué y cuándo.
- `mareas` — `fecha`, `hora`, `tipo`, `altura_m`. **Informativa, fase 6.** Ninguna otra tabla
  depende de ella.

`plazas_ocupadas` es campo materializado en `pases`, no un `COUNT` al vuelo: es lo que permite
bloquear la fila.

## 4. Disponibilidad: la decide el equipo

**Si hay visita, qué día y a qué hora lo decide el equipo.** No hay asistente que proponga ni
regla automática que valide. Esto sustituye a la definición del 2026-07-22 (ver nota en
`02-DECISIONES.md`).

Lo que sí hace falta es que abrir fechas sea rápido y no un formulario por pase:

- **Pase suelto:** día, hora, aforo, idioma.
- **Creación en lote:** rango de fechas + días de la semana + horas.
  «Del 1 al 31 de octubre, sábados y domingos, a las 11:00 y a las 13:00.»
- **Duplicar una semana** en la siguiente, para corregir lo que cambie en vez de empezar de cero.
- **Editar o anular** cualquier pase después, sin tocar el resto.

## 5. Flujo público y aforo

Estados: `pendiente → confirmada → (cancelada | anulada)`, más `caducada`.

Al elegir pase se crea la reserva en `pendiente` **descontando ya las plazas**, dentro de una
transacción con `SELECT … FOR UPDATE` sobre la fila del pase. Sin ese bloqueo, dos personas
reservando a la vez sobre las últimas plazas producen sobreventa: es el fallo clásico de las
apps de reservas y es la regla dura de esta app. Si no confirma en 30 minutos, el cron la caduca
y libera las plazas.

Confirmación: código de 6 dígitos por email, tres intentos, con caducidad. Confirmada, se envía
el correo con los datos y el enlace de gestión (`token_gestion` aleatorio largo, no adivinable).

Cancelación: el visitante desde su enlace (libera plazas), o el gestor anulando un pase o un día
entero — todas las reservas de ese pase pasan a `anulada` y se encola un aviso por afectado.

Recordatorio 24 h antes: sin cobro no hay coste de no presentarse, y ese email es la única
palanca contra las ausencias.

## 6. Panel

Sesión PHP, contraseña con `password_hash`, sin registro público.

- **Gestor** — abre y cierra días, crea pases sueltos o en lote, ajusta aforos, anula, ve y
  exporta la lista del día para llevarla impresa.
- **Reserva a nombre de un tercero** — para quien llama por teléfono o se presenta allí. Descuenta
  plazas igual que una reserva web, así el aforo publicado nunca miente. Es una pantalla genérica:
  sirva quien sirva ese canal.

## 7. Correo transaccional

**Cola en base de datos + envío por cron cada 5 minutos.** Nunca envío síncrono dentro de la
petición: en hosting compartido un SMTP lento cuelga el formulario y un fallo pierde el correo
sin dejar rastro.

`Correo.php` define la interfaz; el transporte se elige por configuración:

1. **SMTP autenticado del propio dominio con PHPMailer.** Opción de partida: los datos personales
   no salen del hosting, coherente con la línea seguida al self-hostear las fuentes.
2. **Brevo o Mailjet** si falla la entregabilidad contra Gmail y GMX — el mercado alemán y
   británico es el que más castiga un SPF flojo.

Cambiar de uno a otro es una línea de `config.php`. `mail()` a secas no se usa aquí: un código de
confirmación en spam es una reserva perdida.

## 8. Idiomas

Cuatro idiomas por prefijo de ruta (`/es/ /en/ /de/ /fr/`), heredando el que traiga el enlace de
origen y arrastrándolo hasta los correos, que se envían en el idioma de la reserva. Los textos
viven en `idiomas/*.php`; solo los de `tipos_visita_i18n` están en la BD.

La app va **`noindex` con `robots.txt` propio**: no compite en SEO, la que rankea es `/visita/`.
La regla «una página = un idioma = una URL» se mantiene aquí por coherencia de navegación, no por
posicionamiento.

## 9. Seguridad y protección de datos

Token CSRF en todo formulario, trampa antispam y límite por IP en el envío de códigos (mismo
patrón que `contacto.php`), PDO preparado siempre, HTTPS con HSTS, cabeceras CSP restrictivas.

Datos personales mínimos, consentimiento explícito enlazando a `/privacidad/`, borrado automático
de reservas pasadas a los 12 meses por cron, y anotación del tratamiento en el registro de
actividades. Copia diaria de la base de datos con retención, también por cron: una BD de reservas
sin copia es una temporada perdida a un fallo de disco.

## 10. Encaje con la web estática

`site.config.json` ya tiene `reservas_origin`. Al activar: el bloque `turismo` de `/visita/` se
sustituye por el CTA «Reservar» hacia el subdominio en el idioma correspondiente, y
`notes.reservas` se actualiza. Es cambio de contenido, no de generador.

En CI se añade `php -l` sobre todo `reservas/` y los tests de aforo y estados. Despliegue por
FTP/SSH del panel del hosting; `build.py` no toca esa carpeta.

## 11. Fases

1. Esquema, migraciones y capa PDO.
2. Panel: días, pases, creación en lote, aforo.
3. Flujo público en ES, con confirmación por código y bloqueo transaccional.
4. Cola de correo y crons (caducidad, avisos de anulación, recordatorio, copia de seguridad).
5. EN/DE/FR y correos traducidos.
6. *Opcional:* columna informativa de mareas en el calendario del panel e informes.

## 12. Abierto

- **Datos de marea (fase 6):** fuente y condiciones de uso (Puertos del Estado / Instituto
  Hidrográfico de la Marina) sin comprobar. Como es informativo, no bloquea nada.
- **Confirmar en el hosting** el buzón remitente y sus credenciales SMTP antes de la fase 4.
