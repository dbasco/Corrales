# 01 · Activos — Los Corrales de Rota

> Inventario de todo lo producido y del archivo fotográfico, con su estado.
> **El estado de un activo vive aquí, no en el fichero suelto.** Un HTML en una carpeta no sabe si es el bueno; este índice sí.
> Última revisión: 2026-07-22

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
| Web v1 — repo (`build.py` + `templates/base.css` + `templates/site.css` + `content/es/*.json` + `site.config.json`) | activo | alta | Sitio estático Monumento. **ES completo: 13 páginas** (inicio, **el monumento**, la visita, 8 joyas, aviso legal y privacidad en borrador). Generador **reescrito desde cero el 2026-07-22**: bloques de ritmo (split foto/texto, diagram del corral, cta al nodo, turismo, keys, **svgfile**) para evitar el efecto «PowerPoint»; SEO/hreflang/JSON-LD/GTM/fachada de vídeo reutilizados; imágenes con `width`/`height` (Pillow, anti-CLS). Reserva por Oficina de Turismo (sin reserva online); sin donaciones en v1; «Aves» fuera del menú. Menú: **El monumento · La visita · Joyas de Rota · Contacto**. Contenido de joyas desde la serie «Más allá del mar». Pendiente: EN/DE/FR, datos legales reales, ID de GTM, cookies. | 2026-07-22 |
| Página `/monumento-natural/` (`content/es/monumento-natural.json`) | activo | alta | **Nueva 2026-07-22.** Explica la figura del Monumento Natural (categoría legal, carácter **ecocultural**, qué protege) que antes se nombraba sin definir. Bloques: hero (foto) → *Un monumento que está vivo* (prose) → **corte SVG del corral** (`templates/corral-corte.svg`, bloque `svgfile`) → biodiversidad (keys) → paisaje (band) → *Sin manos no hay monumento* (split) → nodo a la visita. En el menú y con teaser en el home tras el diagrama. Fotos reutilizadas del archivo ya optimizado (atardecer, aéreo, muro); se pueden sustituir por tomas dedicadas del Drive. Reescrita en llano a partir de la web oficial (google sites). | 2026-07-22 |
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
- **App de reservas** (`reservas.loscorralesderota.com`): a medida, subdominio propio, backend + BD. Catálogo de tipos de visita, disponibilidad manual con asistente de mareas, confirmación por email, cancelación con aviso, gratis (sin pasarela). Definición en `02-DECISIONES.md`; pendiente el servicio de email transaccional.
- Word del plan, CSV de Google Ads, dashboard KPI, one-pager.
