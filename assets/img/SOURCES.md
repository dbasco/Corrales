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

1. Descargar el original de Drive (conector) → se guarda un JSON con el base64.
2. `python3 scripts/optimize_from_download.py <ruta_json> assets/img/<nombre>.jpg <ancho_px> <calidad>`
   (p. ej. `… joya-pinar-hero.jpg 2000 82`).
3. Referenciar la ruta en el JSON de contenido de la página.
