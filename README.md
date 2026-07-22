# Los Corrales de Rota — web v1

Sitio estático multiidioma (ES/EN/DE/FR) de la Asociación de Corraleros y Pescadores a Pie
«Los Corrales de Rota». HTML autocontenidos servidos desde servidor propio, con el sistema
de marca **Monumento**. Máxima prioridad: SEO y velocidad (Core Web Vitals sin backend).

**Alcance v1:** todo el sitio **menos el motor de reservas**. La página `/visita/` sí existe;
su CTA «Reservar» degrada a contacto directo (email) con nota «reservas online, próximamente».
La app de reservas vivirá aparte, en `reservas.loscorralesderota.com`.

## Cómo funciona

Generador estático en Python (sin dependencias para construir; `Pillow` solo para optimizar fotos).
Una página = un idioma = una URL. El bloque de estilo Monumento (`templates/base.css`) se **inlinea
verbatim** en cada página; entre idiomas **solo cambia el copy**.

```
python3 build.py          # genera dist/ (48 páginas + sitemap.xml + robots.txt + favicon.svg)
```

Servir en local para revisar:

```
cd dist && python3 -m http.server 8099   # http://localhost:8099
```

## Estructura

```
site.config.json        Dominio, idiomas, páginas, slugs por idioma, IDs de tracking (GTM/GA4/Ads)
build.py                Generador: head/SEO/hreflang/JSON-LD/GTM + nav + footer + secciones
templates/base.css      Sistema de marca Monumento (CANÓNICO — no editar los tokens :root)
content/ui.<lang>.json  Strings de interfaz (nav, footer, CTA) por idioma
content/<lang>/*.json   Copy por página y por idioma (una plantilla por página)
assets/img/             Fotos optimizadas (~2000px, 200–400 KB) + logo + og:image
assets/img/SOURCES.md   Mapa de cada imagen a su archivo de origen en Drive
scripts/                Utilidades (optimización de imágenes)
docs/                   SEO/analítica y lista de issues de handover para CODE
dist/                   Salida generada (gitignored; la produce build.py)
```

## URLs (mapa cerrado)

ES en la raíz; `/en/ /de/ /fr/` con slugs traducidos, enlazados por `hreflang`.

```
/                    Hub «todo Rota»              (+ /en/ /de/ /fr/)
/visita/             La visita (nodo)             (+ visit / besuch / visite)
/aves/               Joya · aves                  (+ birding / vogel / oiseaux)
/pinar/ /dunas/ /camaleon/ /via-verde/ /pozos-del-galgo/ /jardin-botanico/ /playas/
/aviso-legal/ /privacidad/
```

`apoyar` y `contacto` son secciones ancladas del hub, no páginas propias.

## Estado

- **ES: completo** (hub, visita y aves con contenido a fondo; 7 joyas sobrias; legales en borrador).
- **EN/DE/FR: pendientes de traducción** → ver `docs/handover-issues.md` (lote para CODE).
- Fotos: hub, visita y aves con foto real; las 7 joyas restantes con héroe de degradado de marca
  (publicación por olas; se enriquecen por temporada).
- Tracking: Google Tag Manager cableado en todas las páginas con `GTM-XXXXXXX` de placeholder.

Ver `CLAUDE.md` para el brief completo de continuación.
