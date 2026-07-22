# Arquitectura web — Los Corrales de Rota

> Decisiones técnicas cerradas sobre cómo se construye y sirve la web.
> **Ámbito:** solo la manera de trabajar la página. La estrategia y el plan de comunicación se trabajan aparte.

## Alojamiento

- La web se traslada a un **servidor propio** (fuera de Google Sites).
- Esto elimina las limitaciones de Google Sites: control total de SEO, rutas limpias, sin `noindex` forzado, despliegue del HTML premium tal cual.

## Formato de las páginas

- **HTML autocontenidos**, estáticos.
- Prioridad de diseño: **máxima relevancia SEO** y **máxima velocidad**.
- El HTML plano servido desde disco/CDN da los mejores Core Web Vitals sin backend.
- Se reutiliza el sistema de marca ya establecido (bloque `<style>` verbatim entre páginas; solo cambia el copy).

## Estructura de la web

- Una **web-hub** como destino de la campaña general "todo Rota" (menú completo, marca, footer del 100% a conservación).
- De ella cuelgan **landings específicas**, una por segmento/campaña, cada una destino de su campaña dedicada.
- Cada landing: engancha a su público con mensaje afinado, encadena al resto de joyas, y termina en el CTA común de reserva de visita a los corrales.

## Multiidioma — regla clave

Cuatro idiomas: **ES, EN, DE, FR**.

**Regla:** una página = un idioma = una URL. **NO** meter los 4 idiomas en un solo HTML conmutados por JS (mezcla el DOM, diluye relevancia, pierde URLs indexables).

Patrón de URLs (español en la raíz):

```
/aves/          (ES)
/en/birding/    (EN)
/de/vogel/      (DE)
/fr/oiseaux/    (FR)
```

- Cada URL es un HTML autocontenido independiente, en su idioma.
- Enlazadas entre sí con etiquetas **`hreflang`**.
- Así cada idioma rankea en su mercado y se mantiene el HTML puro, rápido y autocontenido.

## Selección de idioma

- **Autoselección** por idioma del navegador (`navigator.language`): un pelín de JS **redirige** a la versión correcta la primera visita.
- **Selector manual** visible: simplemente enlaces a las otras 3 URLs.
- La preferencia se **recuerda** (localStorage o cookie) para no volver a redirigir.

## Mapa de URLs (cerrado)

Patrón definitivo: **español en la raíz** + `/en/ /de/ /fr/` (no los cuatro simétricos). Cada URL es un HTML autocontenido en su idioma, enlazado por `hreflang`.

```
/                     Hub "todo Rota" (ES)
├─ /aves/             Landing joya · aves
├─ /pinar/            Landing joya · pinar
├─ /dunas/            Landing joya · dunas
├─ /camaleon/         Landing joya · camaleón
├─ /via-verde/        Landing joya · vía verde
├─ /pozos-del-galgo/  Landing joya · pozos del galgo
├─ /jardin-botanico/  Landing joya · jardín botánico
├─ /playas/           Landing joya · playas
├─ /visita/           Página de la visita a los corrales (nodo)
├─ /apoyar/           socios y donaciones
├─ /contacto/
└─ /aviso-legal/  ·  /privacidad/
```

- **Sección vs página:** `apoyar` y `contacto` son secciones ancladas del hub (no multiplican URLs). `visita` sí es página propia porque enlaza al motor de reservas.
- **hreflang:** `es`→`/`, `en`→`/en/`, `de`→`/de/`, `fr`→`/fr/`, `x-default`→`/`. EN/DE/FR replican el mismo árbol con slugs traducidos (aves: `/en/birding/`, `/de/vogel/`, `/fr/oiseaux/`).
- **Publicación por olas:** las landings de joya son nivel 3 (estacionales); la estructura se prevé entera pero las páginas se publican por temporada, no las 8 de golpe.

## Reserva de visitas — el nodo

La reserva es el nodo al que devuelven todas las joyas y la **única parte con estado** del sitio. Se aísla para no tocar los Core Web Vitals del resto.

- **`/visita/`** (y `/en/ /de/ /fr/`): página **estática** del sitio. Explica y "vende" la visita (qué es, cómo funciona, calendario de mareas); su CTA "Reservar" salta a la app.
- **App de reservas:** componente dinámico **separado**, en subdominio propio **`reservas.loscorralesderota.com`**. Backend propio (servidor + BD); el resto del sitio sigue siendo HTML estático. Definición completa en `02-DECISIONES.md`.

## Imágenes

**Ficheros externos (`img/…`), no base64 incrustado.** El base64 hunde el LCP (el one-pager pesaba 4,5 MB por las fotos embebidas). Coherente con la prioridad dura de velocidad. JPG ~2000px, 200–400 KB.

## Vídeo

Integración por **fachada ligera + `youtube-nocookie` + datos estructurados `VideoObject`**: no se carga el reproductor pesado hasta el clic (evita cookies, protege Core Web Vitals). Canal en `02-DECISIONES.md` › YouTube.

## Pendiente de decidir

- Slugs traducidos (EN/DE/FR) de las 7 joyas además de aves. Casos con nombre propio local a resolver: `pozos-del-galgo` y `via-verde` (¿se traducen o se mantienen?).
