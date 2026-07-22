# Handover a CODE — issues propuestos

Lotes de trabajo listos para abrir como issues de GitHub y ejecutar con Claude Code
(p. ej. mencionando a `@claude` en cada issue). Cada uno es autocontenido. Empieza por el #1.

---

## #1 · Traducir la web a EN (English)
**Contexto:** el sitio está completo en ES (`content/es/*.json`, `content/ui.es.json`). Falta EN.
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

## #5 · Mejorar el banco de imágenes
- Sustituir `assets/img/joya-aves.jpg` y `joya-aves-hero.jpg` por una foto nítida de ave del
  archivo `Fotos/Birdwatching` (por hábitat). Ver `assets/img/SOURCES.md`.
- Añadir foto real a cada joya cuando haya material (pinar, dunas, camaleón, etc.), sustituyendo
  el héroe de degradado por `img` en su JSON. Optimizar con `scripts/optimize_from_download.py`.
**Aceptación:** todas las imágenes 200–400 KB, ~2000px, con `width`/`height` en el HTML.

## #6 · Self-hostear las fuentes (Cinzel, Spectral)
Descargar los `.woff2` de Cinzel y Spectral, servirlos desde `/assets/fonts/` con `@font-face`
(`font-display:swap`) y quitar la dependencia de Google Fonts del `<head>`. Objetivo: LCP y
privacidad (sin petición a fonts.gstatic).

## #7 · Cookies + consentimiento (Consent Mode v2)
Añadir banner de consentimiento y Google Consent Mode v2 antes de activar GTM/GA4/Ads en producción.
Página `/cookies/` (nueva plantilla `legal`). Coordinar con `privacidad`.

## #8 · Conectar el formulario de contacto
El formulario de `contacto` es de referencia (no envía). Conectarlo a `info@loscorralesderota.com`
(servicio tipo formspree/endpoint propio) con protección antispam. Sin backend pesado.

## #9 · Poner IDs reales de Google y datos legales
- `site.config.json` → `tracking.gtm_id` con el `GTM-XXXXXXX` real.
- Rellenar CIF, nº de registro de asociaciones y domicilio en `aviso-legal` y `privacidad`.

---

### Definición de «hecho» para cualquier issue
`python3 build.py` OK · sin romper reglas duras (ver `CLAUDE.md`) · `hreflang`/`canonical`/`sitemap`
coherentes · un solo `h1` por página · imágenes con dimensiones · revisado sirviendo `dist/`.
