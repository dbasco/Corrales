# CLAUDE.md — brief de continuación (Los Corrales de Rota, web v1)

Este repositorio es la web v1 de la Asociación «Los Corrales de Rota», y además el hogar
único del proyecto. La fuente de verdad (estrategia, marca, decisiones) vive **ahora en este
repositorio**, bajo `docs/`: `docs/00-INDICE-PROYECTO.md` (punto de entrada), `docs/01-ACTIVOS.md`,
`docs/02-DECISIONES.md` y `docs/web-arquitectura-corrales.md`. Lee el índice entero antes de
tocar nada; si algo aquí contradice esos índices, mandan los índices. Lo único que permanece en
Google Drive (carpeta **Corrales de Rota**) es el archivo fotográfico `Fotos/`, por peso.

## Reglas duras (no negociables)

1. **Una página = un idioma = una URL.** Nada de conmutar 4 idiomas por JS en un solo HTML.
   Cada URL es un HTML autocontenido en su idioma, enlazado con `hreflang`.
2. **HTML autocontenido y estático.** Prioridad absoluta: SEO y velocidad (Core Web Vitals
   sin backend). Nada de frameworks JS, nada de hidratación, nada de build de SPA.
3. **Sistema de marca Monumento, verbatim.** El bloque `templates/base.css` (tokens `:root`
   + componentes) se inlinea igual en todas las páginas. **No se editan los tokens.** Entre
   idiomas solo cambia el copy.
4. **Imágenes como ficheros externos** (`/assets/img/…`), nunca base64 incrustado
   (hunde el LCP). JPG ~2000px, 200–400 KB. Siempre con `width`/`height` para no romper CLS.
5. **Vídeo con fachada + `youtube-nocookie` + `VideoObject`.** No cargar el reproductor
   pesado hasta el clic (ya implementado en `build.py`).
6. **El motor de reservas NO entra en v1.** No lo implementes. El CTA «Reservar» de `/visita/`
   degrada a contacto directo.

## Cómo se construye

`python3 build.py` lee `site.config.json` + `content/**` + `templates/base.css` y escribe `dist/`.
Sin dependencias para construir (solo stdlib). `Pillow` únicamente para el pipeline de imágenes.
Verifica siempre con `python3 build.py` y sirviendo `dist/` (`python3 -m http.server`).

### Modelo de contenido

Cada página tiene un JSON por idioma en `content/<lang>/<page_id>.json`:

```json
{
  "title": "…",                     // <title> y og:title (único por página/idioma)
  "meta_description": "…",          // meta description y og:description (única)
  "hero": {
    "kicker": "…", "h1": "…", "sub": "…",
    "img": "/assets/img/x.jpg", "img_alt": "…",   // o, sin foto: "grad": "grad-pizarra|grad-stone|grad-oxido"
    "cta1": "…", "cta1_href": "…(opcional)",
    "cta2": "…(opcional)", "cta2_href": "…(opcional)"
  },
  "sections": [ { "type": "...", ... } ]
}
```

Tipos de bloque disponibles (ver `build.py` para el contrato exacto):
`prose` (kicker/h2/lead/paras[]/anchor), `stats` (items[]{n,l}), `jewels` (rejilla de las 8 joyas),
`video` (yt/title/desc/date/alt), `faq` (items[]{q,a}), `support` (Bizum/tarjeta), `contact`.

Strings de interfaz (nav, footer, CTA de reservar, «Saltar al contenido») en `content/ui.<lang>.json`.

### SEO ya implementado (mantener)

`<title>` y `meta description` únicos · `canonical` · `hreflang` (es/en/de/fr + `x-default`→ES) ·
Open Graph + Twitter Card · JSON-LD (`NGO`, `WebSite`, `TouristAttraction`, `BreadcrumbList`,
`VideoObject`, `FAQPage`) · `sitemap.xml` con `xhtml:link` alternates · `robots.txt` · un solo `h1`
por página · breadcrumb visible · imágenes con dimensiones y `loading`/`fetchpriority`.

### Analítica / Google (lo que pidió el cliente)

Google Tag Manager en todas las páginas (`<script>` en `<head>` + `<noscript>` tras `<body>`).
El contenedor es el único punto de entrada: desde GTM se añaden **GA4** y **Google Ads**
(conversiones/remarketing) sin tocar el HTML.

- Pon el ID real en `site.config.json` → `tracking.gtm_id` (`GTM-XXXXXXX`) y regenera.
- `ga4_id` y `google_ads_id` quedan de referencia por si se prefiere `gtag.js` directo.
- Antes de publicar: **aviso de cookies + consentimiento** (Consent Mode v2) — pendiente, ver issues.

## Trabajo pendiente (orden sugerido) — ver `docs/handover-issues.md`

1. **Traducir EN, DE, FR.** Portar cada `content/es/*.json` a `content/{en,de,fr}/*.json` con el
   MISMO esquema (traducir valores, no claves). Crear `content/ui.{en,de,fr}.json`. Mantener el
   tono llano, sin metáforas ni grandilocuencia. Revisar que `title`/`meta_description` sean
   naturales en cada idioma (no traducción literal) para SEO por mercado.
2. **Slugs pendientes de decisión** (`via-verde`, `pozos-del-galgo`): confirmar con Daniel antes
   de fijarlos. Están marcados con `slug_pending` en `site.config.json`.
3. **Fotos:** sustituir la foto de aves por una mejor del archivo `Fotos/Birdwatching`; añadir
   fotos reales a las 7 joyas cuando lleguen (publicación por olas). Ver `assets/img/SOURCES.md`.
4. **Fuentes self-hosted:** pasar Cinzel/Spectral a `@font-face` local (hoy vía Google Fonts CDN).
5. **Cookies/consentimiento** (Consent Mode v2) + página de cookies.
6. **Formulario de contacto:** conectar a `info@loscorralesderota.com` (endpoint o servicio).
7. Rellenar datos legales reales (CIF, registro) en aviso-legal y privacidad.

## Qué NO hacer

- No introducir dependencias de build ni frameworks. No romper la regla «una URL = un idioma».
- No editar los tokens `:root` del sistema Monumento.
- No incrustar imágenes en base64. No autoplay de vídeo. No implementar el motor de reservas.
- No inventar datos (números de socios, fechas, especies) que no estén respaldados por los índices.
