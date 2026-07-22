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
  - `obsoleto` — sustituido; se conserva por historial, no se usa → va a `_obsoleto/`
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

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `los-corrales-de-rota-web.html` | activo | alta | Web pública de una página con fotos reales embebidas. Base del futuro hub. | 2026-07-20 |
| `Landing_Rota_Birding_UK_EN.html` | activo | alta | Landing birding monolingüe EN. Será la base de la landing /en/birding multiidioma. Pasará a `obsoleto` cuando exista la versión servidor. | 2026-07-20 |
| `Landing_Rota_Birding_DE.html` | activo | alta | Landing birding monolingüe DE. Idem, base de /de/vogel. | 2026-07-20 |

### Guías

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `Guia_Aves_Rota_Los_Corrales_EN.pdf` | activo | alta | Guía de aves lead-magnet, 12 pág A4, inglés. Muchas láminas son placeholders pendientes de foto. | 2026-07-20 |
| `Rota_Birding_Documentary_DE.srt` | activo | media | Subtítulos en alemán del documental. | 2026-07-20 |

### Impresos

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `cartel-bizum-corrales-de-rota.html` | activo | media | Cartel de donación Bizum. Código ONG de 5 dígitos pendiente (placeholder). | 2026-07-20 |
| `triptico-corrales-de-rota.html` | activo | media | Tríptico bilingüe ES/EN A4 para hoteles. Slots de foto/testimonio/hotel marcados como placeholder. | 2026-07-20 |

### Planes

| Activo | Estado | Relevancia | Notas | Revisado |
|---|---|---|---|---|
| `Plan_Maestro_Rota_Birding_ES.html` | activo | alta | Plan maestro en español (HTML). | 2026-07-20 |
| `plan-ejecutivo-corrales-de-rota.html` | activo | alta | Plan ejecutivo de acciones 60 días con anexo Google Ads. | 2026-07-20 |
| `Rota_Birdwatching_Campaign_Plan.md` | activo | alta | Plan de campaña de birding UK/DE (markdown, extenso). | 2026-07-20 |
| `plan-comunicacion-corrales-INTERNO.html` | activo | alta | Documento ejecutivo interno de visión del plan de comunicación, para alinear al equipo operativo antes del detalle. HTML autocontenido con marca, diagramas (mareas, nodo de joyas), Gantt anual y fotos reales. Lenguaje llano, sin jerga. Es visión, no plan con fechas. | 2026-07-20 |

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
