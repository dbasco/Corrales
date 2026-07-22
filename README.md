# Los Corrales de Rota — web

Repositorio de la web de la Asociación de Corraleros y Pescadores a Pie
«Los Corrales de Rota» (Rota, Cádiz) y hogar único del proyecto. Sitio estático
multiidioma con el sistema de marca **Monumento**. Prioridad dura: SEO y velocidad
(Core Web Vitals sin backend).

> **Estado (2026-07-22):** web **v1 en español completa** (12 páginas). El generador
> se reconstruyó desde cero para dar ritmo con foto (splits, diagrama de cómo pesca
> un corral, bandas a sangre) en lugar del apilado tipo «PowerPoint» anterior.
> EN/DE/FR pendientes de traducción (ver `docs/handover-issues.md`).

## Cómo se construye

```
pip install pillow          # solo para dimensiones de imagen (anti-CLS)
python3 build.py            # genera dist/
cd dist && python3 -m http.server 8099   # previsualizar en http://localhost:8099
```

`build.py` lee `site.config.json` + `content/**` + `templates/base.css` +
`templates/site.css` y escribe `dist/`. Una página = un idioma = una URL. `base.css`
es la marca (verbatim, tokens `:root` intactos); `site.css` añade los componentes de
ritmo. Solo se generan idiomas con contenido: hoy solo ES → 12 páginas, sin páginas vacías.

## Estructura

```
site.config.json        Dominio, idiomas, páginas, slugs, IDs de tracking (GTM/GA4/Ads)
build.py                Generador: SEO/hreflang/JSON-LD/GTM + nav + footer + bloques de ritmo
templates/base.css      Sistema de marca Monumento (CANÓNICO — no editar los tokens :root)
templates/site.css      Componentes de ritmo (split, diagram, cta, turismo, keys, pull)
content/ui.<lang>.json  Strings de interfaz (nav, footer, CTA) por idioma
content/<lang>/*.json   Copy por página y por idioma
assets/img/             Fotos optimizadas (~2000px, 200–400 KB) + logo + og:image
scripts/                Utilidades (optimización de imágenes)
docs/                   Fuente de verdad: índices, decisiones, arquitectura, _fuentes, deliverables
dist/                   Salida generada (gitignored)
```

## Páginas (ES)

```
/                    Hub «todo Rota»
/visita/             La visita (el nodo; reserva por la Oficina de Turismo de Rota)
/aves/  /pinar/  /dunas/  /camaleon/  /via-verde/  /pozos-del-galgo/  /jardin-botanico/  /playas/
/aviso-legal/  /privacidad/   (borrador, datos legales pendientes)
```

## Reglas duras y pendientes

Ver `CLAUDE.md` (reglas y modelo de contenido) y `docs/02-DECISIONES.md`. En resumen:
una URL = un idioma, HTML estático, marca Monumento verbatim, imágenes externas con
dimensiones, vídeo con fachada, sin motor de reservas ni donaciones en v1.
Pendiente: traducciones EN/DE/FR, datos legales reales, ID de GTM real, consentimiento
de cookies y formulario de contacto operativo (`docs/handover-issues.md`).
