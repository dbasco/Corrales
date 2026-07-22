# 00 · Índice del proyecto — Los Corrales de Rota

> **Punto de entrada.** Empieza siempre por aquí. Este fichero explica qué es el proyecto, quién es quién, y dónde vive cada cosa.
> Última revisión: 2026-07-22

---

## Qué es este proyecto

Estrategia digital, de marketing y de captación de fondos para la **Asociación de Corraleros y Pescadores a Pie "Los Corrales de Rota"** (Rota, Cádiz).

La asociación es custodia de los corrales de Rota — arte de pesca tradicional sobre la franja intermareal, **primer Monumento Natural de Andalucía** (declarado 2001). Organización sin ánimo de lucro; el 100 % de la recaudación va a conservación del monumento.

- ~400 socios · fundada en 2014 · 8 corrales activos
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

## Estructura de carpetas del Drive

```
Corrales de Rota/
├── 00-INDICE-PROYECTO.md
├── 01-ACTIVOS.md
├── 02-DECISIONES.md
│
├── deliverables/ ← lo que se usa o se va a usar
│   ├── web/ (HTML de hub y landings)
│   ├── guias/ (guía de aves PDF y futuras ediciones)
│   ├── impresos/ (cartel Bizum, tríptico)
│   ├── marca/ (sistema de marca, logo, plantillas doc/ppt/email, fuentes)
│   └── planes/ (plan maestro, plan ejecutivo, campaign plan)
│
├── fotos/ ← archivo fotográfico y multimedia (insumos)
│   ├── corrales/
│   └── aves/ (por hábitat/especie)
│
├── _obsoleto/ ← versiones superadas; se conservan, no se usan
│
└── _fuentes/ ← materia prima: notas, borradores, insumos sueltos
```

### Reglas de la estructura
- Los índices `.md` viven en la **raíz**, siempre visibles.
- `deliverables/` agrupa **por tipo**, no por idioma ni campaña (un deliverable tendrá 4 idiomas; no se cuadruplica la estructura).
- **`_obsoleto/`** y **`_fuentes/`** con guion bajo para que caigan al fondo alfabéticamente y se distingan a simple vista.
- Cuando un activo pasa a estado `obsoleto` en 01-ACTIVOS.md, se **mueve** físicamente a `_obsoleto/`. Así `deliverables/` solo contiene cosas vivas.

### Dónde suelta insumos el colaborador multimedia
Fotos y vídeos nuevos van a **`fotos/`** (en la subcarpeta que corresponda) o a **`_fuentes/`** si aún no están clasificados. Nunca a `deliverables/`.
