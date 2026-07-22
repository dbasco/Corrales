# Marca Monumento — aplicación en documentos, presentaciones y email

> Extensión del sistema de marca (`sistema-de-marca-monumento.html`) a los tres medios
> que no son web. La **paleta es idéntica** en todos; lo que cambia por medio es la
> **tipografía**, porque cada soporte resuelve las fuentes de forma distinta.

## Paleta (idéntica en los tres medios)

| Nombre | Hex | Uso |
|---|---|---|
| Sal | `#F4F1E9` | Fondo claro |
| Roca mojada | `#23201C` | Texto y trazo |
| Pizarra-mar | `#35494E` | Marca · fondos oscuros |
| Piedra seca | `#9A8F7C` | Neutro medio |
| Hierro/óxido | `#A85A32` | Acento único |
| Surface | `#FCFAF4` | Superficies sobre sal |

> **Impresión:** estos hex son RGB (pantalla). Para offset, convertir a CMYK y hacer
> prueba de color impresa — el óxido y la pizarra pueden virar.

## Tipografía por medio (la regla clave)

- **Web / PDF** — Cinzel (titulares fuertes, capitales) + Spectral (texto). Fidelidad total.
- **Office (Word y PowerPoint)** — **Cambria** como fuente de trabajo: viene instalada con
  Office y se renderiza fiel. Los titulares fuertes van en **versalitas con letra espaciada**
  (hacen de Cinzel). *Para fidelidad total:* instalar Cinzel y Spectral (gratis, Google Fonts)
  en los equipos y sustituir Cambria por ellas. No usar Cinzel/Spectral sin instalarlas: Office
  las cambiaría por una fuente cualquiera.
- **Email** — **Georgia** (web-safe, está en todos los clientes). La marca la lleva el **logo
  como imagen** (con las fuentes horneadas dentro). Nunca depender de fuentes web en email:
  Outlook y Gmail las descartan.

## Layout por medio

**Documentos (Word)** — A4, márgenes 1". Portada: logo + antetítulo óxido + título en
versalitas. Cuerpo: H1 pizarra, H2 roca, texto Cambria 11 pt izquierda. Cita destacada con
borde izquierdo óxido sobre surface. Tabla con cabecera pizarra/texto sal. Pie: URL ·
conservación · página.

**Presentaciones (PowerPoint, 16:9)** — estructura sándwich: portada, divisor y cierre en
fondo oscuro (pizarra o roca); contenido y cifras en fondo claro (sal/surface). Motivo visual:
el isotipo repetido en las oscuras. Un solo acento óxido por slide. **Sin franjas ni líneas de
acento** (delatan plantilla). Titulares 36 pt+; cuerpo 14-16 pt; alineación a la izquierda.

**Email (600 px)** — tablas + estilos inline. Cabecera clara con el logo; hero en pizarra con
botón *bulletproof* óxido; cuerpo claro; bloque "Apoyar"; pie en roca con la línea de
conservación. **Alojar el logo** en el servidor y referenciarlo por URL — no dejar el base64
del ejemplo (Gmail lo bloquea).

## Ficheros de esta extensión

- `plantilla-documento-monumento.docx` — plantilla de Word.
- `plantilla-presentacion-monumento.pptx` — plantilla de PowerPoint (5 diseños).
- `plantilla-email-monumento.html` — plantilla de email + `firma-email-monumento.html`.
- `fuentes/` — Cinzel y Spectral (TTF) para instalar en los equipos.
- Logo en `logo/` (SVG) y `png/` (PNG con fondo transparente para Office/email).
