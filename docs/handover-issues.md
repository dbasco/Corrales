# Handover a CODE — issues propuestos

Lotes de trabajo listos para abrir como issues de GitHub y ejecutar con Claude Code
(p. ej. mencionando a `@claude` en cada issue). Cada uno es autocontenido.

> **Estado 2026-07-23 (segunda pasada).** **#6 HECHO** (fuentes propias) y **#8 HECHO**
> (`contacto.php`). Quedan **#7** (banner de cookies) y la parte de GTM de **#9** — y ambos
> dejan de ser bloqueantes si se publica sin activar la analítica: con el ID de GTM de ejemplo
> la web no escribe ninguna cookie.
> El grueso de trabajo restante son los idiomas (#1 EN, #2 DE, #3 FR): hoy solo existe `content/es`,
> y la campaña de birding apunta a Reino Unido y Alemania.

---

## #1 · Traducir la web a EN (English) — **HECHO (2026-07-23)**
**Hecho:** `content/en/*.json` (13 páginas) + `content/ui.en.json`. 26 URLs generadas.
Verificado: cero enlaces internos rotos, un solo `h1` por página, `title` y `meta_description`
únicos en las 26, `hreflang` es/en/x-default coherente. **Pendiente: revisión visual de las
páginas EN** (la QA de esta sesión fue estructural).

**Nota para #2 (DE) y #3 (FR):** la traducción es **todo o nada**. Con solo la home traducida,
el inicio EN enlazaba a 12 páginas inexistentes: la rejilla de joyas y el menú apuntan a todas
las páginas del idioma, existan o no. No dejar un idioma a medias en `main`.

**Contexto original:** el sitio está completo en ES (`content/es/*.json`, `content/ui.es.json`).
**Tarea:** crear `content/en/<page_id>.json` para las 12 páginas y `content/ui.en.json`, con el
mismo esquema que ES (traducir valores, no claves).
**Requisitos:**
- Tono llano, natural para lector de habla inglesa (mercado birding UK incluido). NO traducción literal.
- `title` y `meta_description` reescritos para SEO en inglés (keywords: *fish traps, tidal, Rota,
  Cádiz, birding, natural monument*), no calcados del español.
- Reutilizar como referencia la landing EN de referencia en `docs/deliverables/web/Landing_Rota_Birding_UK_EN.html` (marca vieja; solo copy/estructura).
- Mantener los `yt` de vídeo y las rutas de imagen igual que en ES.
**Aceptación:** `python3 build.py` sin errores; `/en/…` con `desc` no vacía en las 12 páginas;
`hreflang` correcto; un solo `h1`; validar con el script de `docs/` o revisión manual.

## #2 · Traducir la web a DE (Deutsch)
Igual que #1 para alemán. Referencia: `docs/deliverables/web/Landing_Rota_Birding_DE.html` y `docs/deliverables/guias/Rota_Birding_Documentary_DE.srt` (referencia). Keywords SEO DE: *Fischfallen, Gezeiten, Vogelbeobachtung, Naturdenkmal, Rota*.

## #3 · Traducir la web a FR (Français)
Igual que #1 para francés. Keywords SEO FR: *pêcheries à marée, ornithologie, monument naturel, Rota*.

## #4 · Decidir y fijar slugs pendientes
`via-verde` y `pozos-del-galgo` están marcados `slug_pending` en `site.config.json`.
Confirmar con Daniel si se traducen o se mantienen como topónimo, y actualizar `slugs` en los 4 idiomas.
Regenerar y comprobar que `sitemap.xml`/`hreflang` siguen coherentes.

## #5 · Mejorar el banco de imágenes  — **PARCIAL (2026-07-23)**
> Hecho: 5 de las 6 joyas en degradado ya tienen foto (camaleón, jardín botánico, vía verde,
> pinar, pozos del galgo) y el inicio tiene mosaico. **Falta: dunas (sin foto) y sustituir las
> de aves** por material de `Fotos/Birdwatching`. `joya-pinar.jpg` es de 761 px y conviene
> reemplazarla. Confirmar que la pasarela asignada a pozos del galgo es ese sitio.
- Sustituir `assets/img/joya-aves.jpg` y `joya-aves-hero.jpg` por una foto nítida de ave del
  archivo `Fotos/Birdwatching` (por hábitat). Ver `assets/img/SOURCES.md`.
- Añadir foto real a cada joya cuando haya material (pinar, dunas, camaleón, etc.), sustituyendo
  el héroe de degradado por `img` en su JSON. Optimizar con `scripts/optimize_from_download.py`.
**Aceptación:** todas las imágenes 200–400 KB, ~2000px, con `width`/`height` en el HTML.

## #6 · Self-hostear las fuentes (Cinzel, Spectral) — **HECHO (2026-07-23)**
~~Descargar los `.woff2`…~~ Hecho: `assets/fonts/` (108 KB, subset latin), `@font-face` en
`base.css`, preload en `build.py`, enlaces a Google retirados. Verificado en Chromium: cero
peticiones a terceros salvo GTM.

## #7 · Cookies + consentimiento (Consent Mode v2)
Añadir banner de consentimiento y Google Consent Mode v2 antes de activar GTM/GA4/Ads en producción.
Página `/cookies/` (nueva plantilla `legal`). Coordinar con `privacidad`.

## #8 · Conectar el formulario de contacto — **HECHO (2026-07-23)**
~~El formulario de `contacto` es de referencia (no envía)…~~ Hecho con `contacto.php` propio
(el hosting tiene PHP), sin servicio externo. Ver `02-DECISIONES.md`.
**Queda por confirmar con el hosting:** que `mail()` esté activa y que exista
`web@loscorralesderota.com` como remitente.

## #9 · Poner IDs reales de Google y datos legales — **PARCIAL (2026-07-23)**
- `site.config.json` → `tracking.gtm_id` sigue en `GTM-XXXXXXX`. **PENDIENTE.**
- ~~Rellenar CIF, nº de registro y domicilio~~ → **HECHO**: CIF G72275449 y registro
  11-1-11400 (Sección 1ª) en `aviso-legal` y `privacidad`. Ya no queda ningún `[pendiente]`.

---

## Motor de reservas (`reservas/`, subdominio propio)

> Arquitectura en `docs/reservas-arquitectura.md`. Funcional en `02-DECISIONES.md`.
> **La disponibilidad la decide el equipo**: no hay asistente de mareas, no lo implementes.
> Cada lote acaba con `php -l` limpio y el CI en verde (job `reservas`).

## #10 · Esquema, configuración y capa de datos — **HECHO (2026-07-23)**
`reservas/` con `migraciones/001_esquema.sql` (10 tablas + el tipo de visita «corrales» sembrado),
`config.example.php`, `src/Config.php`, `src/Db.php` (PDO, `transaccion()`, `bloquearPase()`),
`migrar.php` y `README.md`. CI: sintaxis PHP, `config.php` no versionado, migraciones sin
prefijos repetidos. **Sin probar contra una base de datos real** — falta ejecutar `migrar.php`
en el hosting.

## #11 · Panel: días, pases y aforo
Login (`password_hash`, sesión, roles `gestor` y `mostrador`), calendario por tipo de visita,
alta de pase suelto, **creación en lote** (rango de fechas + días de la semana + horas),
duplicar una semana en la siguiente, editar/anular pase o día entero, cambiar aforo.
Lista del día exportable e imprimible. Todo cambio deja rastro en `auditoria`.
**Aceptación:** abrir un mes de sábados y domingos con dos pases diarios en menos de un minuto;
anular un pase no borra sus reservas, las pasa a `anulada`.

## #12 · Flujo público en ES
Elegir tipo → día → pase → nombre, email, personas y consentimiento → código de 6 dígitos →
confirmada, con localizador y enlace de gestión. Cancelación del visitante desde ese enlace.
Reserva desde el panel a nombre de un tercero (`origen = 'panel'`), que descuenta plazas igual.
**Regla dura:** el aforo se toca solo dentro de `Db::transaccion()` + `Db::bloquearPase()`.
**Aceptación:** un test que lance dos reservas simultáneas sobre la última plaza y demuestre
que una gana y la otra recibe «sin plazas». Sin ese test, el lote no está hecho.

## #13 · Cola de correo y crons
`Correo.php` con transporte intercambiable (`smtp` vía PHPMailer / `registro` para pruebas),
plantillas en `idiomas/`, y los crons: enviar la cola cada 5 min, caducar reservas sin confirmar,
recordatorio 24 h antes, avisos de anulación, borrado a los 12 meses y copia de seguridad diaria.
**Nada de envío síncrono dentro de la petición.**
**Pendiente externo:** confirmar el buzón remitente y sus credenciales SMTP en el hosting.

## #14 · EN, DE y FR
Interfaz y correos en los cuatro idiomas, heredando el idioma del enlace de entrada y
guardándolo en la reserva. `noindex` y `robots.txt` propio del subdominio.

## #15 · *Opcional:* mareas informativas e informes
Importar las pleamares y bajamares de Rota a la tabla `mareas` y mostrar la hora de bajamar
junto a cada día en el calendario del panel. **No valida ni propone nada.** Antes de importar,
comprobar las condiciones de uso de la fuente (Puertos del Estado / IHM).

---

### Definición de «hecho» para cualquier issue
`python3 build.py` OK · sin romper reglas duras (ver `CLAUDE.md`) · `hreflang`/`canonical`/`sitemap`
coherentes · un solo `h1` por página · imágenes con dimensiones · revisado sirviendo `dist/`.
