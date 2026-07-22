# Origen de las imágenes

Todas provienen del archivo del proyecto en Google Drive (carpeta **Corrales de Rota / Fotos**),
optimizadas con `scripts/optimize_from_download.py` (JPG ~2000px, 200–400 KB).

| Fichero | Uso | Origen en Drive (Fotos/) | Drive fileId |
|---|---|---|---|
| `corrales-hero.jpg` | Hero del hub `/` | Corrales/`Corrales-01.jpg` | `1PhbNY05C989Y3iDEWZc9iS_PbjQwaHSS` |
| `og-default.jpg` | og:image por defecto | Corrales/`Corrales-01.jpg` | `1PhbNY05C989Y3iDEWZc9iS_PbjQwaHSS` |
| `visita-hero.jpg` | Hero de `/visita/` | Corrales/`corrales-tarde-1.png` | `1JNfKJbr4_nqIxViTlO3VS_7oWU16JZJ-` |
| `joya-aves-hero.jpg` | Hero de `/aves/` | Birdwatching/aves marinas/`4266…_n.jpg` | `1bt_jcrNCAyGZePPRdfGrEYr8Y6ifeB96` |
| `joya-aves.jpg` | Tarjeta joya «aves» en el hub | (idem anterior) | `1bt_jcrNCAyGZePPRdfGrEYr8Y6ifeB96` |
| `logo-corrales.png` | `logo` de la ficha Organization (JSON-LD) | Generado del isotipo Monumento | — |

## Pendiente (issue #5)

- **Aves:** la foto actual es de baja calidad (origen redes). Sustituir por una nítida de
  `Fotos/Birdwatching` (subcarpetas por hábitat: rapaces, insectívoras, marinas/limícolas,
  marismas, herbívoras).
- **7 joyas restantes** (pinar, dunas, camaleón, vía verde, pozos del galgo, jardín botánico,
  playas): hoy usan héroe de degradado de marca. Añadir foto real cuando el colaborador
  multimedia la aporte (publicación por olas). Buenas panorámicas de dron de los corrales en
  `Fotos/Corrales/` (varios `DJI_*` y `dji_fly_*_pano.jpg`).

## Cómo optimizar una nueva

Las fotos **no** se tiran por el conector de Drive (devuelve base64 y satura la sesión).

1. Descargar el original de Drive y pasarlo en un **ZIP** al entorno de trabajo.
2. `python3 scripts/optimize_from_download.py <ruta_imagen> assets/img/<nombre>.jpg <ancho_px> <calidad>`
   (p. ej. `… joya-pinar-hero.jpg 2000 82`) → JPG ~2000 px, 200–400 KB.
3. Referenciar la ruta `/assets/img/<nombre>.jpg` en el JSON de contenido de la página.
   El original pesado se queda en Drive.

## Actualización 2026-07-22 — fotos reales integradas

Sustituido el héroe de `/aves/` (antes era la foto de una hoja manuscrita, no un ave) y añadida
fotografía real en hub, visita, aves y playas. Optimizadas a ~2000 px / 200–400 KB desde
`Fotos/Corrales` y `Fotos/Birdwatching` del Drive.

| Fichero | Uso | Origen (Fotos/) |
|---|---|---|
| `joya-aves-hero.jpg` | Héroe de `/aves/` (sustituye el manuscrito) | Birdwatching · cigüeñuela `DSC_1994` |
| `joya-aves.jpg` | Tarjeta joya «aves» (hub) + galería aves | Birdwatching · espátula `DSC_4903` |
| `ave-garza.jpg` · `ave-flamenco.jpg` · `ave-cernicalo.jpg` | Galería de `/aves/` | Birdwatching (garza real, flamencos, cernícalo primilla) |
| `corrales-aereo.jpg` | Banda del hub | Corrales · `DJI_20260627200935_0033_D` |
| `corrales-muro.jpg` | Figura «muros que pescan» (hub) | Corrales · `IMG_5300` |
| `corrales-atardecer.jpg` | Figura de `/playas/` | Corrales · `IMG_1608` |
| `visita-gente.jpg` | Figura de `/visita/` | Corrales · `IMG_1591` |
| `playa-hero.jpg` | Héroe y tarjeta de `/playas/` | Corrales · `dji_fly_…0022_pano` |

Pendiente: fotos propias de pinar, dunas, camaleón, vía verde, pozos del galgo y jardín botánico
(no existen en el archivo); esas 6 joyas siguen con héroe de degradado de marca.
