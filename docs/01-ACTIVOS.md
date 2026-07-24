# 01 · Activos — Los Corrales de Rota

> Inventario de todo lo producido y del archivo fotográfico, con su estado.
> **El estado de un activo vive aquí, no en el fichero suelto.** Un HTML en una carpeta no sabe si es el bueno; este índice sí.
> Última revisión: 2026-07-23

---

## Cómo se lee la ficha de un activo

Cada activo tiene:

- **Estado** (vigencia — dónde está en su ciclo de vida):
  - `borrador` — en construcción, no usar aún
  - `activo` — es la versión buena, fuente de verdad hoy
  - `publicado` — activo y además desplegado/en producción
  - `referencia` — no es el activo vigente, pero se conserva por copy/estructura reutilizable
  - `obsoleto` — sustituido; se conserva en el repo por historial, no se usa (el estado vive aquí, el fichero no se mueve)
  - `archivado` — ya no aplica al proyecto
- **Relevancia** (cuánto importa ahora): `alta` / `media` / `baja`
- **sustituye_a / sustituido_por** — rastro entre versiones
- **revisado** — fecha de última revisión

**Pertinencia** (¿sigue encajando con la estrategia?) no es un campo sino una revisión periódica: si la estrategia cambió y el activo ya no la sirve, pasa a `obsoleto`.

---

## Deliverables

### Marca

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `sistema-de-marca-monumento.html` | activo | alta | Sistema de marca canónico (dirección Monumento). Tokens `:root`, logo, tipografía (Cinzel+Spectral) y componentes. Fuente de verdad de la marca. | 2026-07-22 |
| `logo/` (isotipo · negativo · monocromo · favicon · lockup horizontal, SVG) | activo | alta | Pack de logo en colores Monumento. Isotipo geométrico: muro de piedra + agua + línea de marea. | 2026-07-22 |
| `marca/` (plantillas docx · pptx · email + firma + nota de aplicación + fuentes + PNG) | activo | alta | Extensión del sistema Monumento a documentos, presentaciones y email. Tipografía por medio (Cinzel/Spectral · Cambria · Georgia). | 2026-07-22 |
| `direcciones-de-marca-corrales.html`, `variantes-color-corrales.html` | archivado | baja | Comparadores de las 3 direcciones y de las variantes de color. Historial de la decisión de marca → `_fuentes/`. | 2026-07-22 |

### Web

La web v1 vive en **este repositorio** (sitio estático generado), no en Drive. Reglas y modelo de
contenido en `CLAUDE.md`; arquitectura en `web-arquitectura-corrales.md`.

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| Web v1 — repo (`build.py` + `templates/base.css` + `templates/site.css` + `content/es/*.json` + `site.config.json`) | activo | alta | Sitio estático Monumento. **ES + EN completos: 13 páginas cada uno** (inicio, el monumento, la visita, 8 joyas, aviso legal y privacidad). Generador reescrito el 2026-07-22: bloques de ritmo (split, diagram, gallery, band, cta, keys, svgfile); SEO/hreflang/JSON-LD/GTM/fachada de vídeo; imágenes con `width`/`height` (anti-CLS). Reserva por Oficina de Turismo (sin reserva online); **sin donaciones en v1**; «Aves» fuera del menú. Menú: **El monumento · La visita · Joyas de Rota · Contacto**. **Revisión 2026-07-23:** corregidos cuatro fallos detectados revisando en local — fotos de `split` verticales (`height:auto`), scroll horizontal en móvil por el panel del menú, ritmo vertical incoherente entre secciones y contraste 1,71 en el botón de la barra. **Revisión 2026-07-23 (segunda pasada):** fuentes self-hosted (sin Google Fonts), formulario conectado a `contacto.php`, contraste del kicker a AA y modo `--preview` para pruebas en servidor. **Etiqueta de Google puesta (2026-07-24):** Ads `AW-17862259314` por gtag.js en las 26 páginas (`tracking.provider: "gtag"`); no hay contenedor GTM. **Bloqueante que queda: banner de cookies + Consent Mode v2**, ahora obligatorio porque la etiqueta es real y escribe cookies. **EN completo (2026-07-23): 13 páginas más, 26 URLs.** Pendiente: DE/FR. Datos legales (CIF y registro) ya rellenados. | 2026-07-23 |
| Página `/monumento-natural/` (`content/es/monumento-natural.json`) | activo | alta | **Nueva 2026-07-22.** Explica la figura del Monumento Natural (categoría legal, carácter **ecocultural**, qué protege) que antes se nombraba sin definir. Bloques: hero (**panorámica aérea**, `corrales-panoramica.jpg`) → *Un monumento que está vivo* (prose) → **corte SVG del corral** (`templates/corral-corte.svg`, bloque `svgfile`) → biodiversidad (keys) → **foto del pez guitarra** (figure) → paisaje (band) → *Sin manos no hay monumento* (split) → nodo a la visita. En el menú y con teaser en el home tras el diagrama. Reescrita en llano a partir de la web oficial (google sites). | 2026-07-22 |
| Archivo fotográfico de la web oficial (25 imágenes, `Archivo.zip`) | activo | alta | **Recibido 2026-07-22.** 14 optimizadas e integradas en `assets/img/` (tabla en `assets/img/SOURCES.md`). Cubre 5 de las 6 joyas que estaban en degradado: camaleón, jardín botánico, vía verde, pinar y pozos del galgo (**asignación a confirmar**). Alimenta también el **mosaico del inicio** (6 fotos). **Sigue sin foto: dunas.** `joya-pinar.jpg` es de solo 761 px: en el hero se amplía un 68 %. No usar `corrales_14.png` (escudo de la Base Naval de Rota). En reserva: corrales_07 y 08. | 2026-07-23 |
| `los-corrales-de-rota-web.html` (Drive) | obsoleto | baja | One-page de Drive con fotos embebidas en base64. **Superado por la web v1 del repo.** Se conserva como referencia histórica. | 2026-07-22 |
| `Landing_Rota_Birding_UK_EN.html` (Drive) | referencia | media | Landing birding monolingüe EN. Referencia para traducir la web a EN (handover-issues #1); no se sirve tal cual. | 2026-07-22 |
| `Landing_Rota_Birding_DE.html` (Drive) | referencia | media | Landing birding monolingüe DE. Referencia para la traducción DE (handover-issues #2). | 2026-07-22 |

### Guías

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `Guia_Aves_Rota_Los_Corrales_EN.pdf` | referencia | media | Guía de aves lead-magnet, 12 pág A4, inglés. De la campaña de birding (estrategia superada) y con la **marca vieja** (foam/teal); muchas láminas son placeholders. Se conserva por copy EN y listas de especies. | 2026-07-22 |
| `Rota_Birding_Documentary_DE.srt` | referencia | baja | Subtítulos en alemán del documental de birding. Referencia para la traducción DE. | 2026-07-22 |

### Impresos

> Ambos usan la **marca heredada** (foam/teal + Fraunces/Hanken/Space Mono): **pendientes de re-piel** a Monumento antes de usarse.

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `cartel-bizum-corrales-de-rota.html` | referencia | media | Cartel de donación Bizum. **Las donaciones no entran en la web v1** (se reactivan con el código ONG + pasarela). Marca vieja, pendiente de re-piel. | 2026-07-22 |
| `triptico-corrales-de-rota.html` | referencia | baja | Tríptico ES/EN A4 para hoteles, de la campaña de birding. Marca vieja, pendiente de re-piel; slots de foto/testimonio/hotel como placeholder. | 2026-07-22 |

### Planes

> **Estrategia vigente: «Todo dentro de Rota»** (ver `02-DECISIONES.md`). La antigua campaña premium
> de birding **UK/DE apoyada en Doñana y el Estrecho quedó superada**; los planes que la desarrollan
> se conservan como **referencia** (copy, estructura, listas de especies), no como plan actual.

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| Ilustraciones de las mareas (`corral-fase-1/2/3`) | activo | alta | **Nuevas 2026-07-23.** Tres escenas (pleamar, bajando, bajamar) en estilo grabado, **generadas con IA (Google Gemini)** por encargo de la asociación y pedidas **sin texto**: los rótulos van en HTML, así que se traducen y son accesibles. Viven en el bloque `diagram` de `/monumento-natural/`. Recortadas para quitar rosa de los vientos, barra de escala mal graduada y el destello de Gemini. **Abierto:** el muro sale más alto de lo que es (el texto dice «muro bajo») y si se declara el uso de IA. | 2026-07-23 |
| `assets/fonts/` (Cinzel variable + Spectral 400/500/600/700, woff2) | activo | alta | **Nuevo 2026-07-23.** Fuentes de marca subseteadas a latin, 108 KB. Sustituyen al CDN de Google Fonts. Cubren ES/EN/DE/FR (verificado). | 2026-07-23 |
| `web-requisitos-servidor-y-despliegue.html` (deliverables/tecnicos) | activo | alta | **Nuevo 2026-07-23.** Gemelo del de reservas, para la web estatica: requisitos del alojamiento (raiz del dominio, compresion, MIME woff2, cache, TLS, PHP para contacto.php, correo), preguntas al proveedor, publicacion paso a paso (generar o descargar el artefacto del CI, pruebas con --preview, rsync a produccion), verificaciones (la primera: que no se haya subido el build de pruebas), informe de vuelta, problemas frecuentes, .htaccess de ejemplo y anexo de salida de Google Sites con DNS y redirecciones 301. Marca Monumento, imprimible. | 2026-07-23 |
| `reservas-requisitos-servidor-y-despliegue.html` (deliverables/tecnicos) | activo | alta | **Nuevo 2026-07-23.** Requisitos del entorno del servidor (PHP, BD, cron, SMTP, DNS/TLS) e instrucciones paso a paso para quien administre el servidor: acceso al repo, subdominio, base de datos, `config.php`, diagnostico, migracion, verificaciones (esquema, claves foraneas, exposicion de ficheros, bloqueo de aforo), informe de vuelta, problemas frecuentes y anexo `.htaccess`. Marca Monumento, imprimible. | 2026-07-23 |
| `reservas/comprobar-entorno.php` | activo | alta | **Nuevo 2026-07-23.** Diagnostico del servidor: version de PHP, extensiones, conexion y motor de la BD, permisos reales (crea y borra tabla de prueba, comprueba que el rollback deshace), zona horaria y salida SMTP. CLI, o web con clave. No modifica nada. | 2026-07-23 |
| `contacto.php` | activo | alta | **Nuevo 2026-07-23.** Receptor del formulario de contacto. Único fichero dinámico del sitio; va en la raíz del servidor. Validación, antispam y consentimiento. Requiere `mail()` activa en el hosting (**por confirmar**). | 2026-07-23 |
| `scripts/build_local_preview.py` | activo | media | Genera `dist-local/`: copia de `dist/` con rutas relativas, navegable a doble clic (`file://`) sin servidor. Solo para revisión; a producción va `dist/` con rutas absolutas. | 2026-07-23 |
| `templates/corral-corte.svg` | referencia | baja | Corte transversal del corral en paleta de marca. **Retirado de la web** el 2026-07-23: las ilustraciones del diagrama contaban lo mismo. Se conserva para la guía en PDF. | 2026-07-23 |
| `plan-comunicacion-corrales-INTERNO.html` | activo | alta | **Plan vigente.** Visión del plan de comunicación «Todo dentro de Rota» para alinear al equipo: marca, diagramas (mareas, nodo de joyas), Gantt anual, fotos reales. Lenguaje llano. Es visión, no plan con fechas. | 2026-07-22 |
| `plan-ejecutivo-corrales-de-rota.html` | activo | media | Acciones a 60 días con anexo Google Ads. Revisar contra la estrategia vigente (el Ad Grant es un canal más, no el eje). | 2026-07-22 |
| `Plan_Maestro_Rota_Birding_ES.html` | referencia | media | Plan maestro (ES) de la campaña de birding. **Estrategia superada** por «Todo dentro de Rota»; se conserva como referencia. | 2026-07-22 |
| `Rota_Birdwatching_Campaign_Plan.md` | referencia | media | Plan de campaña de birding UK/DE (extenso: keywords, anuncios, hoteles). **Estrategia superada** (Doñana/Estrecho descartados); útil como referencia de copy EN y estructura. | 2026-07-22 |

---

## Archivo fotográfico

Vive en la carpeta compartida **Birdwatching** (dentro de `fotos/`), alimentada por los fotógrafos colaboradores. Organizada por taxonomía/hábitat.

### Estado por hábitat (carpetas con material)

- **aves insectívoras** — abundante: alcaudón, currucas, golondrinas, mirlos, petirrojos, tarabillas, colirrojo, papamoscas, abejaruco, abubilla, ruiseñor pechiazul, etc.
- **aves rapaces** — águila calzada, cernícalo primilla (material nuevo, valioso).
- **aves marinas / limícolas** — archibebe, zarapito trinador, chorlitejo patinegro, cormorán grande.
- **aves herbívoras** — tórtola turca, pinzones, gorriones, verderones, perdices, jilgueros, paloma torcaz, cotorras, etc.
- **aves de marismas, ríos y lagos** — flamencos, espátula, morito, garcetas, garza real, cigüeñas, cigüeñuela, martinete, martín pescador, polla de agua.
- **Corrales** — tomas de dron y generales del monumento (JPG, PNG, panorámicas, algún MP4).

### Huecos críticos (especies de la guía SIN foto propia)

Estas especies costeras sostienen el discurso "corrales = escondite natural vivo" y **no tienen carpeta/foto** en el archivo:

- Águila pescadora (osprey)
- Gaviota de Audouin
- Gaviota picofina
- Charranes / pagazas (terns)
- Ibis eremita (Northern Bald Ibis)
- Vencejo moro (little swift)
- Rabilargo (azure-winged magpie)

> **Tensión estratégica documentada:** el archivo real empuja hacia pinar + marisma + rapaces, mientras la narrativa de campaña está anclada en la franja intermareal y las gaviotas del corral. Decisión pendiente en 02-DECISIONES.md.

---

## Fuentes / insumos

Materia prima en `_fuentes/` (notas, borradores, volcados sin clasificar). No son deliverables; se minan para producirlos.

| Insumo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `inventario_AndresBarba_youtube.md` | activo | media | Volcado del canal de Andrés Barba (@AndresBarbaRota): 41 vídeos en formato largo, ~204.500 visualizaciones acumuladas, con URL/duración/visualizaciones/etiquetas/descripción. La serie "Más allá del mar" (ep. 1–7) mapea casi 1:1 sobre las joyas (pinar, botánico, pozos del galgo, dunas, aves, camaleón, vía verde). Vídeos 5 y 31 son de aves, con listas de especies por temporada/hábitat reutilizables para guía y landing; documentan en vídeo las especies costeras marcadas como huecos sin foto. Vídeos 10/29/39/40 sobre la visita a los corrales (el nodo). Limitación: solo 4 vídeos (2–5) con transcripción completa extraída; el resto es ASR no extraíble o subtítulos manuales que no cargaron, así que sirve como mapa + descripciones, no como texto hablado. Ojo al reutilizar el ep. 5: apoya el discurso en Doñana (descartada). | 2026-07-21 |

---

## Pendientes de activo

- Re-piel de los deliverables existentes (web, guías, impresos, planes) al sistema de marca Monumento.
- Edición alemana de la guía de aves (PDF).
- Versiones multiidioma (ES/EN/DE/FR) de hub y landings para servidor.
- **App de reservas** (`reservas.loscorralesderota.com`): a medida, subdominio propio, backend + BD. **Retomada el 2026-07-23** (ya no está aplazada). PHP 8 + MySQL en el hosting actual, sin framework. Catálogo de tipos de visita, **disponibilidad decidida por el equipo** (creación de pases en lote; sin asistente de mareas: la marea es informativa), aforo con bloqueo transaccional, confirmación por código, cancelación con aviso, reserva a nombre de terceros desde el panel, gratis (sin pasarela). Funcional en `02-DECISIONES.md`; **implementación en `reservas-arquitectura.md`**. Sin código escrito todavía.
- Word del plan, CSV de Google Ads, dashboard KPI, one-pager.
