# Los Corrales de Rota — web

Repositorio de la web de la Asociación de Corraleros y Pescadores a Pie
«Los Corrales de Rota» (Rota, Cádiz) y hogar único del proyecto.

> **Estado (2026-07-22): la web se ha reiniciado.** La implementación anterior
> (`content/`, `build.py`, páginas generadas) se retiró porque el resultado no
> valía: apilaba texto con divisores (efecto «PowerPoint»), no explicaba qué es
> un corral y desaprovechaba las fotos. Se reconstruye desde cero.
>
> Lo retirado queda en el historial de git (recuperable). La maquinaria SEO
> (title/description únicos, canonical, hreflang, Open Graph, JSON-LD, sitemap,
> GTM, fachada de vídeo) se rescatará del historial al reconstruir el generador,
> por ser requisito duro.

## Qué se conserva (intocable / fuente de verdad)

- `templates/base.css` — sistema de marca **Monumento** (tokens `:root` + componentes). No se editan los tokens.
- `assets/img/` — fotos ya optimizadas (~2000 px, 200–400 KB) + logo + og:image. `SOURCES.md` mapea cada una a su origen.
- `docs/**` — **fuente de verdad**: índices (`00`, `01-ACTIVOS`, `02-DECISIONES`, `web-arquitectura`), `deliverables/`, `_fuentes/`.
- `site.config.json` — dominio, idiomas, mapa de páginas/slugs, IDs de tracking (GTM/GA4/Ads).
- `scripts/` — utilidades (pipeline de optimización de imágenes con Pillow).
- `CLAUDE.md` — reglas duras y modelo de contenido de la web. Léelo antes de tocar la web.

## Reglas duras (de `CLAUDE.md` / `docs/02-DECISIONES.md`)

Una página = un idioma = una URL (enlazadas con `hreflang`) · HTML estático autocontenido,
sin frameworks, SEO y velocidad por encima de todo · marca Monumento verbatim · imágenes como
ficheros externos (nunca base64) · vídeo con fachada + `youtube-nocookie` + `VideoObject` ·
el motor de reservas **no** entra en v1 (la visita se reserva por la Oficina de Turismo de Rota).
