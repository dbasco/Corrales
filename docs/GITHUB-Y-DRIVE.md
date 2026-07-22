# Qué hay en GitHub y qué función tiene el Drive

> Estado a 2026-07-22. Resume cómo está montado el proyecto tras trasladar todo a GitHub.

## En una línea

- **GitHub (`dbasco/Corrales`) es la fuente de verdad única del proyecto:** el código de la web,
  el contenido, la marca, los deliverables y los índices de decisiones.
- **Google Drive queda solo como archivo fotográfico y multimedia** (las fotos crudas pesadas).
  Todo lo demás que había en Drive ya está copiado en GitHub.

---

## GitHub — repo `dbasco/Corrales` (privado)

Es el hogar completo del proyecto: la web **y** su documentación.

```
Corrales/
├── build.py                 Generador estático (Python, stdlib; Pillow solo para fotos)
├── site.config.json         Dominio, idiomas, páginas/slugs, IDs de tracking (GTM/GA4/Ads)
├── CLAUDE.md                Reglas duras + modelo de contenido (léelo antes de tocar)
├── README.md                Resumen de la web y cómo construirla
├── .github/workflows/       CI: construye dist/ como artefacto en cada push
├── templates/
│   ├── base.css             SISTEMA DE MARCA MONUMENTO (canónico; no se tocan los tokens :root)
│   └── site.css             Componentes de ritmo (split, diagram, cta, turismo, keys)
├── content/
│   ├── ui.es.json           Strings de interfaz (nav, footer, CTAs) en español
│   └── es/*.json            Copy por página en español (12 páginas)
├── assets/img/              Fotos OPTIMIZADAS para web (~2000 px, <400 KB) + logo + og:image
├── scripts/                 optimize_from_download.py (redimensiona fotos)
├── docs/                    BASE DE CONOCIMIENTO (trasladada del Drive)
│   ├── 00-INDICE-PROYECTO.md    Punto de entrada: qué es, personas, estructura
│   ├── 01-ACTIVOS.md           Inventario de deliverables y del archivo fotográfico
│   ├── 02-DECISIONES.md        Decisiones cerradas y su porqué (FUENTE DE VERDAD)
│   ├── web-arquitectura-corrales.md   Detalle técnico de la web
│   ├── handover-issues.md      Lotes de trabajo pendientes
│   ├── README.md               Mapa de la carpeta docs/
│   ├── deliverables/           Marca, web, guías, impresos y planes (migrados de Drive)
│   │   ├── marca/   (sistema Monumento, logos SVG, plantillas doc/ppt/email)
│   │   ├── web/     (one-pager y landings de birding EN/DE — legado/referencia)
│   │   ├── guias/   (guía de aves PDF, subtítulos)
│   │   ├── impresos/(cartel Bizum, tríptico)
│   │   └── planes/  (plan maestro, ejecutivo, comunicación, campaña)
│   └── _fuentes/               Insumos sin clasificar (inventario del canal de YouTube)
└── dist/                    Salida generada por build.py (gitignored; NO se versiona)
```

**Qué manda dentro del repo:**
- Las **decisiones** viven en `docs/02-DECISIONES.md` (y los otros índices). Si algo se cierra o
  cambia, se anota ahí.
- El **diseño** es `templates/base.css` (sistema Monumento). No se editan sus tokens `:root`.
- La **web** se genera con `build.py` a partir de `site.config.json` + `content/**` + `templates/base.css` + `templates/site.css`.

**Conexión:** clon/push con un PAT (necesita scope `repo` + `workflow`, porque hay un workflow de
CI). Detalle en el handover de reinicio.

---

## Google Drive — qué función tiene AHORA

Antes el Drive era la fuente de verdad (los índices vivían allí). **Ya no.** Su único papel es:

**Archivo fotográfico y multimedia** — la carpeta **`Fotos/`**:
- `Fotos/Corrales/` — tomas de los corrales (dron, panorámicas, atardeceres, vídeos). ~75 ficheros.
- `Fotos/Birdwatching/` — aves organizadas por hábitat y especie (marismas, marinas, rapaces,
  insectívoras, herbívoras).

Son los **originales pesados (2–29 MB)**, que **no** deben ir a git (engordan el repo). Por eso se
quedan en Drive. Los fotógrafos colaboradores siguen alimentando esta carpeta.

**Todo lo demás que había en Drive ya está en GitHub.** Los índices, los deliverables (marca,
planes, guías, impresos) y `_fuentes/` se copiaron a `docs/` del repo. Las copias siguen existiendo
en Drive, pero son **legado**: no son la fuente de verdad y no hay que editarlas esperando que
cuenten. El trabajo se hace en GitHub.

---

## Cómo fluye el trabajo

- **Decisiones y documentos** → se escriben/actualizan en **GitHub** (`docs/`).
- **Fotos para la web** → salen del **Drive** (`Fotos/`), pero **no se pueden tirar por el conector
  de Drive** (devuelve la imagen como base64 y satura la sesión de trabajo). El flujo es:
  descargar de Drive → pasar en un **ZIP** → **optimizar** (~2000 px, 200–400 KB) → guardar en
  `assets/img/` del repo. El original pesado se queda en Drive.
- **La web** se construye desde el repo (`python3 build.py`) y se despliega como HTML estático.

---

## Resumen

| | GitHub (`dbasco/Corrales`) | Google Drive |
|---|---|---|
| **Rol** | Fuente de verdad del proyecto | Archivo fotográfico crudo |
| **Contiene** | Web, contenido, marca, deliverables, índices/decisiones | `Fotos/` (Corrales + Birdwatching) |
| **Fotos** | Versiones optimizadas para web (`assets/img/`) | Originales pesados (2–29 MB) |
| **Se edita aquí** | Sí, todo | No (solo entran fotos nuevas) |
