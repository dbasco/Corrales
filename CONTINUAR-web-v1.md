# CONTINUAR — Web v1 «Los Corrales de Rota» (para retomar en un chat normal)

> Este documento existe porque la web v1 se construyó en un chat de **Cowork**, cuyo sandbox
> tiene GitHub capado (proxy que solo alcanza repos «adjuntados» a la sesión, y esta se abrió
> sin ninguno). En un **chat normal de Claude Code** (donde el repo es la carpeta de trabajo)
> el push funciona sin problema. Aquí tienes todo el estado para continuar allí sin perder nada.

---

## 0) Lo primero: subir el repo a GitHub

El paquete trae la carpeta `corrales/` que **ya es un repo git** con el commit inicial y el remoto
configurado. En el chat/terminal nuevo:

```
cd corrales
git push -u origin main
```

- Repo destino: **https://github.com/dbasco/Corrales** (GitHub ignora mayúsculas; el remoto quedó
  como `dbasco/corrales`, resuelve igual).
- Si pide credenciales: usuario `dbasco`, contraseña = tu PAT.
- Si dice «non-fast-forward» (creaste el repo con README): `git push -u origin main --force`
  (es tuyo y está vacío).
- **SEGURIDAD:** el PAT `ghp_…` que usaste quedó escrito en el chat de Cowork. **Rótalo** en
  GitHub → Settings → Developer settings → Tokens en cuanto termines.

---

## 1) Qué es esto

Web v1 de la Asociación de Corraleros y Pescadores a Pie «Los Corrales de Rota» (Rota, Cádiz).
Sitio **estático multiidioma (ES/EN/DE/FR)**, HTML autocontenidos servidos desde servidor propio,
con el sistema de marca **Monumento**. Prioridad: SEO y velocidad (Core Web Vitals sin backend).

**Alcance v1 = todo el sitio MENOS el motor de reservas.** La página `/visita/` sí existe; su CTA
«Reservar» degrada a contacto (email) con nota «reservas online, próximamente». La app de reservas
irá aparte, en `reservas.loscorralesderota.com` (definición en el Drive, `02-DECISIONES.md`).

Fuente de verdad del proyecto: Google Drive, carpeta **Corrales de Rota**, índices
`00-INDICE-PROYECTO.md`, `01-ACTIVOS.md`, `02-DECISIONES.md`, `web-arquitectura-corrales.md`.

---

## 2) Estado actual (qué está hecho y qué falta)

**Hecho:**
- Generador estático en Python (`build.py`, sin dependencias; `Pillow` solo para fotos).
- Sistema Monumento verbatim en `templates/base.css` (tokens `:root` + componentes).
- **Español COMPLETO:** hub, visita y aves a fondo (con foto y vídeo reales); 7 joyas sobrias
  (héroe de degradado, publicación por olas); aviso-legal y privacidad en borrador.
- SEO técnico en las 48 páginas: `hreflang` (es/en/de/fr + x-default), canonical, JSON-LD
  (NGO, WebSite, TouristAttraction, BreadcrumbList, VideoObject, FAQPage), Open Graph, un solo `h1`,
  `sitemap.xml` (48 URLs, 240 alternates), `robots.txt`, `favicon.svg`. Validado: 0 enlaces rotos.
- **Google Tag Manager** cableado en todas las páginas (head + noscript), ID placeholder `GTM-XXXXXXX`.
- Fotos reales optimizadas (corrales al atardecer, aves) y vídeos reales del canal de Andrés
  (`6d7-eABEOuc` visita guiada, `GMsm0N-mUU4` consejos, `hVISRxkWAAI` aves).

**Falta (delegado a CODE — ver `docs/handover-issues.md`, 9 issues):**
1. Traducir a **EN** (issue #1) — el grueso; usa como referencia `Landing_Rota_Birding_UK_EN.html` del Drive.
2. Traducir a **DE** (issue #2).
3. Traducir a **FR** (issue #3).
4. Fijar slugs pendientes `via-verde` y `pozos-del-galgo` (issue #4) — decisión de Daniel.
5. Mejorar la foto de aves (baja calidad) y añadir fotos a las 7 joyas (issue #5).
6. Self-host de fuentes Cinzel/Spectral (issue #6).
7. Cookies + Consent Mode v2 antes de publicar (issue #7).
8. Conectar el formulario de contacto a `info@loscorralesderota.com` (issue #8).
9. IDs reales de Google (`site.config.json`) + datos legales reales (issue #9).

---

## 3) Cómo se construye y se revisa

```
python3 build.py            # genera dist/ (48 páginas + sitemap + robots + favicon)
cd dist && python3 -m http.server 8099   # revisar en http://localhost:8099
```

Para ver el ES en local: el hub `/` autoredirige por idioma del navegador; abre con locale `es`
o entra directo a una página (p. ej. `/visita/`).

---

## 4) Estructura del repo

```
site.config.json     Dominio (loscorralesderota.com), idiomas, 12 páginas, slugs por idioma, IDs GTM/GA4/Ads
build.py             Generador (una URL = un idioma; inlinea base.css; head/SEO/hreflang/JSON-LD/GTM)
templates/base.css   Sistema Monumento CANÓNICO (no editar los tokens :root)
content/ui.<lang>.json   Strings de interfaz por idioma (solo existe ui.es.json; faltan en/de/fr)
content/<lang>/*.json    Copy por página e idioma (solo existe content/es/; faltan en/de/fr)
assets/img/          Fotos optimizadas + logo + og:image (+ SOURCES.md con el origen en Drive)
scripts/             optimize_from_download.py (redimensiona fotos de Drive a ~2000px 200-400KB)
docs/handover-issues.md  Los 9 issues para CODE
CLAUDE.md            Brief de reglas duras + modelo de contenido (léelo antes de tocar)
.github/workflows/build.yml  CI: construye dist y lo sube como artefacto
dist/                Salida generada (gitignored; la produce build.py)
```

---

## 5) Reglas duras (no romper)

1. Una página = un idioma = una URL. Nada de 4 idiomas por JS en un HTML.
2. HTML autocontenido y estático. Sin frameworks. SEO y velocidad por encima de todo.
3. Sistema Monumento verbatim: no editar los tokens `:root` de `templates/base.css`.
4. Imágenes como ficheros externos (`/assets/img/…`), nunca base64. JPG ~2000px, 200-400 KB, con `width`/`height`.
5. Vídeo con fachada + `youtube-nocookie` + `VideoObject` (ya implementado).
6. El motor de reservas NO entra en v1.

Detalle completo y modelo de contenido (esquema de los JSON por página) en **`CLAUDE.md`**.

---

## 6) Decisiones y datos que hacen falta de Daniel

- **Slugs** de `via-verde` (provisional greenway/gruener-weg/voie-verte) y `pozos-del-galgo`
  (provisional: topónimo sin traducir). Confirmar.
- **GTM ID real** para `site.config.json` → `tracking.gtm_id`.
- **Datos legales**: CIF, nº de registro de asociaciones, domicilio (para aviso-legal y privacidad).
- **Código ONG Bizum** (5 dígitos) y decisión de pasarela de tarjeta (PayPal vs Stripe) — hoy placeholders.
- Mejor foto de aves (archivo `Fotos/Birdwatching` en Drive).

---

## 7) Índices del Drive a reemplazar

En el chat de Cowork se generaron las versiones actualizadas de `01-ACTIVOS.md` y `02-DECISIONES.md`
(añaden la web v1, GTM, GitHub/CODE, slugs). Están en `drive-update/` dentro del paquete. Reemplaza
con ellas las de la raíz del Drive «Corrales de Rota» (el conector no sobrescribe .md en sitio).

---

## 8) Por qué el chat de Cowork no pudo hacer el push (para que no se repita)

Cowork corre en un sandbox en la nube; su proxy de salida solo deja llegar a GitHub los repos
adjuntados a la sesión (mecanismo `add_repo`), y esta sesión se abrió sin ninguno. Ni el token de
sesión ni un PAT lo saltan (el bloqueo es de red, no de permisos del token). En un chat normal de
Claude Code el repo es la carpeta de trabajo y esto no ocurre. Ahí es donde se continúa.
