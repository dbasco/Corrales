# 00 · Índice del proyecto — Los Corrales de Rota

> **Punto de entrada.** Empieza siempre por aquí. Este fichero explica qué es el proyecto, quién es quién, y dónde vive cada cosa.
> Última revisión: 2026-07-23

---

## Qué es este proyecto

Estrategia digital, de marketing y de captación de fondos para la **Asociación de Corraleros y Pescadores a Pie "Los Corrales de Rota"** (Rota, Cádiz).

La asociación es custodia de los corrales de Rota — arte de pesca tradicional sobre la franja intermareal, **primer Monumento Natural de Andalucía** (declarado 2001). Organización sin ánimo de lucro; el 100 % de la recaudación va a conservación del monumento.

- ~400 socios · fundada en 2014 · 5 corrales activos
- Menú de la web: **El monumento · La visita · Joyas de Rota · Contacto**
- Web pública: loscorralesderota.com
- Contacto: info@loscorralesderota.com

## Personas

| Rol | Persona |
|---|---|
| Gestión del proyecto / estrategia | Daniel |
| Presidente | David Campos |
| Vicepresidente y creador de contenido YouTube | Andrés Barba |
| Biólogo colaborador | Adrián Ruiz |
| Fotógrafo colaborador | Antonio Gallardo (Alma y Luz Fotografías) |
| Fotógrafo colaborador | Alejandro Magariño (@maga_fauna) |

## Mapa de ficheros índice

Este proyecto se documenta con tres índices. Consúltalos al empezar cualquier trabajo:

| Fichero | Qué contiene | Cambia cuando… |
|---|---|---|
| **00-INDICE-PROYECTO.md** (este) | Mapa de entrada, personas, estructura | Casi nunca |
| **01-ACTIVOS.md** | Inventario de deliverables y del archivo fotográfico, con su estado | Se produce o revisa algo |
| **02-DECISIONES.md** | Decisiones cerradas y su porqué (web, donaciones, YouTube, marca…) | Se cierra o revierte una decisión |

El **plan de comunicación / estrategia** todavía está en construcción; cuando se cierre tendrá su propio fichero (`03-PLAN.md`).

## Estructura del repositorio

Todo el proyecto vive en el repo `dbasco/Corrales` (GitHub). El Drive **solo** guarda el archivo
fotográfico (`Fotos/`, originales pesados). Ver `GITHUB-Y-DRIVE.md`.

```
Corrales/
├── build.py                 Generador estático de la web
├── site.config.json         Dominio, idiomas, páginas/slugs, tracking
├── CLAUDE.md                 Reglas duras + modelo de contenido de la web
├── templates/
│   ├── base.css             Marca Monumento (canónico; no se tocan los tokens :root)
│   ├── site.css             Componentes de ritmo (split, diagram, gallery, cta, keys)
│   └── corral-corte.svg     Corte del corral (fuera de la web; reservado para el PDF)
├── content/
│   ├── ui.es.json           Strings de interfaz
│   └── es/*.json            Copy por página (ES, 13 páginas)
├── assets/img/              Fotos optimizadas para web + logo + og
├── scripts/                 Utilidades (optimización de imágenes,
│                            build_local_preview.py → copia con rutas relativas)
├── docs/
│   ├── 00-INDICE-PROYECTO.md · 01-ACTIVOS.md · 02-DECISIONES.md
│   ├── web-arquitectura-corrales.md · reservas-arquitectura.md
│   ├── handover-issues.md · GITHUB-Y-DRIVE.md
│   ├── deliverables/        Marca, web, guías, impresos, planes
│   └── _fuentes/            Insumos sin clasificar (volcado de la web oficial,
│                             inventario de YouTube)
└── dist/                    Salida de build.py (gitignored)
```

### Reglas de la estructura
- Los índices (`00`, `01`, `02`) y `CLAUDE.md` mandan. Si algo se cierra o cambia, se anota en el
  índice que corresponda. **El estado de un activo vive en `01-ACTIVOS.md`, no en el fichero suelto.**
- `deliverables/` agrupa **por tipo** (marca, web, guías, impresos, planes), no por idioma ni campaña.
- El estado se marca (`activo` / `referencia` / `obsoleto`) en `01-ACTIVOS.md`; los ficheros no se borran.

### Fotos (Drive)
Los fotógrafos colaboradores sueltan fotos y vídeos nuevos en el Drive, carpeta **`Fotos/`**
(`Corrales/` y `Birdwatching/`, por hábitat/especie). Para la web se optimizan y se guardan en
`assets/img/` del repo; el original pesado se queda en Drive. **No** se usa el conector de Drive
(el base64 satura la sesión): descargar → ZIP → optimizar. Detalle en `GITHUB-Y-DRIVE.md`.
