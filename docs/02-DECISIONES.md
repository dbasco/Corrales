# 02 · Decisiones — Los Corrales de Rota

> Lo que ya está cerrado y por qué. El "qué ya no se discute".
> Si una decisión se revierte, se anota aquí con fecha — no se borra.
> Última revisión: 2026-07-22

---

## Web y arquitectura técnica

> **Estado de la web (2026-07-22):** v1 ES construida y en `main` (repo). El generador se
> reescribió desde cero para dar ritmo con foto (splits, diagrama del corral, bandas) en vez
> del apilado tipo «PowerPoint». Reglas duras y modelo de bloques en `CLAUDE.md`; inventario en
> `01-ACTIVOS.md`. Las decisiones de abajo no cambian; se han respetado en la implementación.

Ver detalle completo en `web-arquitectura-corrales.md`. Resumen:

- **Servidor propio**, fuera de Google Sites. Motivo: control de SEO, rutas limpias, sin `noindex` forzado.
- **HTML autocontenidos y estáticos.** Prioridad: máxima relevancia SEO y máxima velocidad (Core Web Vitals sin backend).
- **Arquitectura hub + landings:** una web-hub (campaña general "todo Rota") de la que cuelgan landings por segmento, cada una destino de su campaña, todas terminando en el CTA de reserva de visita a los corrales.
- **Multiidioma ES/EN/DE/FR con regla dura:** una página = un idioma = una URL. NO 4 idiomas en un HTML por JS. URLs separadas enlazadas con `hreflang`.
- **Idioma:** autoselección por navegador (redirección) + selector manual + preferencia recordada.
- **Patrón de carpetas: español en raíz** + `/en/ /de/ /fr/` (cerrado, no los cuatro simétricos). Mapa de URLs completo en `web-arquitectura-corrales.md`.
- **Imágenes como ficheros externos** (`img/…`), no base64: el base64 hunde el LCP. JPG ~2000px, 200–400 KB.

## Monumento Natural — página propia y menú (2026-07-22)

> La web nombraba «Monumento Natural» varias veces sin explicar la figura (hallazgo de una auditoría externa). Se cierra creando contenido, no ingeniería nueva salvo dos extensiones menores del generador.

- **Página propia `/monumento-natural/`** con la explicación completa: qué es la figura (categoría legal de espacio protegido), su carácter **ecocultural** (naturaleza + patrimonio humano a la vez), qué protege (franja intermareal, muros, pradera de fanerógamas), biodiversidad, paisaje y el papel de la asociación. Fuente de partida: la página homónima de la web oficial (google sites), reescrita en llano.
- **Al menú principal como primer ítem:** *El monumento · La visita · Joyas de Rota · Contacto*. El monumento es la identidad del sitio, no una joya. (Cambia la decisión previa de menú de 3 ítems.)
- **Teaser en el home** tras el diagrama: define la figura en corto y enlaza a la página (mejor recorrido «qué es → por qué importa»).
- **Extensiones del generador** (`build.py`): tipo de página `monumento` (recibe esquema `TouristAttraction`) y bloque `svgfile` (inlina un SVG de `templates/`). Nuevo activo `templates/corral-corte.svg`: corte transversal del corral en paleta de marca.

### Notas de datos — **manda la web oficial** (loscorralesderota.com), decidido 2026-07-22
Regla: ante cualquier discrepancia de datos, la web oficial es la autoridad (por encima de auditorías o fuentes externas).
- **Fecha:** **23 de octubre de 2001** (la da la página del monumento de la web oficial). Se usa en la página del monumento. Supersede la fecha del Decreto 226/2001 «de 2 de octubre» que citaba la auditoría; si alguna vez hace falta la referencia legal, es el Decreto 226/2001 (BOJA 135, 22/11/2001).
- **Origen:** **época romana** (la web oficial lo afirma en home y en «descubre»). Aplicado en home y en la página del monumento. (Deja sin efecto mi cautela anterior de no fijar el origen.)
- **«El primero de Andalucía»:** se mantiene (la web oficial lo afirma).
- **Corrales activos:** se mantiene **8** (config `corrales_activos: 8`). La web oficial no da número de activos, así que no contradice; la fuente autoritativa es la propia asociación.

## Reservas de visitas — estado actual (2026-07-22)

- **Por ahora, las visitas a los corrales se gestionan EXCLUSIVAMENTE por la Oficina de Turismo de Rota** (tel. 956 846345, turismorota@gmail.com). La asociación guía la visita; la reserva la lleva Turismo. No hay reserva por email de la asociación ni "reserva online".
- **El motor de reservas propio queda APLAZADO** — no se desarrolla ahora. Su definición de alto nivel (abajo) se conserva para cuando se retome.
- **En la web v1**, la sección de reserva de `/visita/` dirige a la Oficina de Turismo de Rota (teléfono y correo); se quitó "reserva online próximamente" y el email de la asociación como canal de reserva.
- **Las joyas NO llevan botón de reserva** (no se reservan): su CTA es "La visita a los corrales" y lleva a `/visita/`. Lo único reservable es la visita a los corrales.
- **"Aves" no ocupa sitio en el menú principal**: es una joya más; se llega por "Joyas de Rota". El menú queda: La visita · Joyas de Rota · Contacto.

## App de reservas (aplazada)

> Definición de alto nivel cerrada el 2026-07-22. La reserva es el nodo al que devuelven todas las joyas. Encaje en la web en `web-arquitectura-corrales.md`.

- **A medida, hecha con IA — no SaaS.** Ningún SaaS gestiona bien la disponibilidad por marea. Contrapartida asumida: es la única pieza con backend propio (servidor + BD); el resto del sitio sigue estático.
- **Subdominio propio:** `reservas.loscorralesderota.com`, aislada del sitio estático para no tocar su rendimiento. Interfaz y correos en ES/EN/DE/FR; hereda el idioma con el que llega el visitante.
- **Gratis, sin cobro.** La app NO lleva pasarela. Los ingresos son siempre por donativo, por su vía aparte (Bizum/tarjeta), nunca acoplados al flujo de reserva.
- **Catálogo de tipos de visita.** La "visita a los corrales" es el primer tipo de un catálogo. Cada tipo: nombre, descripción, características (duración, qué incluye, guía, idioma), aforo por defecto y si **depende de marea**. Más adelante se dan de alta otras joyas sin tocar código.
- **Disponibilidad manual con asistente de mareas.** Modelo: tipo de visita → día → pase (con aforo). El admin abre los días; para los tipos "depende de marea" (corrales) el asistente propone las ventanas de bajamar visitables a partir de la tabla de mareas de Rota, y el admin las acepta o ajusta. Nada se publica solo. Los tipos que no dependen de marea se abren con horario normal.
- **Aforo por personas**, configurable por pase; cada reserva descuenta su nº de personas.
- **Confirmación por código.** Flujo: tipo → día → pase → nombre + email + nº personas → recibe un **código por email** → lo introduce → reserva confirmada + email con los datos y enlace de cancelación. Sin confirmar, la reserva queda pendiente y caduca.
- **Cancelación:** (a) el admin anula un pase o un día entero (marea, tiempo) → todas las reservas de ese pase pasan a canceladas y se avisa por email a cada afectado; (b) el visitante cancela su reserva desde el enlace del email y libera sus plazas.
- **Único pendiente técnico:** servicio de **email transaccional** (código, confirmación y avisos de cancelación).

## Donaciones y pagos

- **En la web v1 NO hay donaciones (2026-07-22).** Se quitó la sección "Apoyar" del hub y su enlace del menú: una sección de donar no funcional (sin código Bizum ni pasarela) no se publica. Se reactivará cuando estén el código ONG de Bizum y la pasarela de tarjeta. El mensaje de misión "100 % a conservación" se mantiene en footer y texto (identidad, no petición de donar). El modelo de donación definido se conserva abajo.
- **Dos vías:** Bizum (gratis para locales; requiere código ONG de 5 dígitos asignado por banco, posiblemente condicionado a declaración de utilidad pública) + tarjeta (para visitantes internacionales y comunidad de la base naval de Rota).
- **Pasarela de tarjeta: PENDIENTE** — elección entre PayPal y Stripe. Al decidir, se añade botón de tarjeta junto al panel Bizum en la sección "Apoyar".
- **Zelle descartado.** Motivo: requiere cuentas bancarias en EE. UU. en ambos lados.

## YouTube

- **No se crea canal oficial de la asociación.** El canal personal de Andrés Barba se mantiene tal cual, con acuerdo informal de uso y crédito.
- **YouTube Nonprofit Program evaluado y rechazado.** Motivo: el botón Donate es solo para EE. UU.; sin funciones relevantes para una asociación española.
- **Canal confirmado:** @AndresBarbaRota (ID `UC0hM62nay3JEDGFhZV6MvQw`). Andrés Barba es socio; cesión desinteresada; sus vídeos promocionan el monumento.
- **Método de integración en la web:** fachada ligera + `youtube-nocookie` + datos estructurados `VideoObject` (no se carga el reproductor pesado hasta el clic; evita cookies y protege Core Web Vitals).

## Marca / diseño

> Reabierto y decidido desde cero el 2026-07-22. El sistema anterior (foam/teal + Fraunces/Hanken/Space Mono) no venía de un ejercicio de marca: se heredó de los deliverables de la campaña de birding y quedó anotado como "establecido" sin justificación. Se descartó por leer genérico ("look de diseño AI") y poco propio de una institución tradicional y oficial.

**Decisión: dirección "Monumento".** Elegida por el equipo frente a otras dos direcciones (Bajamar naturalista, Corral cálido/artesanal) y a dos variantes de color más claras (Ibicenca, Florida Keys). Carácter buscado: cálido y marinero, sobrio, sin marrón ni fondos "eléctricos".

- **Logo:** el propio corral — muro de piedra seca (arco de cantos), agua retenida y línea de marea. Isotipo geométrico, independiente de la paleta. Variantes: color, negativo, monocromo, favicon; lockups horizontal y vertical.
- **Paleta Monumento:** sal `#F4F1E9` (fondo), roca mojada `#23201C` (texto/trazo), pizarra-mar `#35494E` (marca/agua/enlaces), piedra seca `#9A8F7C` (neutro), hierro/óxido `#A85A32` (acento único). Surface `#FCFAF4`.
- **Tipografías:** Cinzel (capitales romanas — marca y titulares fuertes) + Spectral (titulares de sección y texto). Se elimina la tercera tipografía (mono); el rol de kicker/datos lo hace Spectral en versalitas espaciadas.
- **Tipografía por medio:** web/PDF usan Cinzel + Spectral; Office (Word/PowerPoint) usa Cambria (viene instalada, fiel; titulares en versalitas espaciadas), con opción de instalar Cinzel/Spectral para fidelidad total; email usa Georgia y la marca la lleva el logo como imagen. Detalle en `deliverables/marca/marca-aplicacion-doc-ppt-email.md`.
- **Patrones:** sin cambios estructurales (kicker eyebrows, botones pill, nav sticky con blur, hero full-bleed con degradado veil, banda de stats, rejilla de tarjetas); solo cambia la piel.
- **Fuente de verdad:** `deliverables/marca/sistema-de-marca-monumento.html` (tokens `:root` + logo + componentes). Pegar el bloque `:root` verbatim en cada HTML.
- **Tono:** lenguaje llano, sin metáforas ni títulos grandilocuentes.
- **Pendiente:** re-piel de los deliverables existentes (web, guías, impresos, planes), que aún usan la paleta/tipografía heredadas.

## Estrategia — base acordada (no cerrada)

> Esto es la base sobre la que se construye el plan; el plan en sí sigue abierto.
> Aprobada como "buena por ahora" y plasmada en el documento ejecutivo interno
> (`deliverables/planes/plan-comunicacion-corrales-INTERNO.html`).

- **El techo de la actividad principal es estructural:** las visitas a los corrales solo pueden hacerse 2 veces al día por las mareas, y no siempre por el tiempo. No escala sola. Se rodea, no se fuerza.
- **Arquitectura de campañas en 3 niveles** (para el equipo se explica con la analogía de una tienda: rótulo / escaparate / carteles de temporada):
  1. Marca / paraguas — "quiénes somos" (el rótulo). Permanente. Los corraleros, monumento natural, 100 % a conservación. Da confianza, no vende actividad concreta.
  2. General "todo Rota" — el escaparate. Permanente. Menú completo, capta al indeciso, vende estancia larga.
  3. Segmentadas por joya — los carteles de temporada. Estacionales, targeting fino, cada una en su ventana; todas devuelven al nodo = visita a los corrales.
  - Los niveles 1 y 2 están encendidos todo el año y cuestan poco (web, redes, presencia). El nivel 3 se enciende/apaga por temporada y es donde va el esfuerzo y la posible inversión en publicidad.
- **Mecanismo de encadenamiento:** el visitante entra por una joya (lo que le interesa) → descubre el resto → alarga estancia → pasa por la visita a los corrales. Da igual la puerta de entrada; todas llevan al nodo.
- **Las joyas como imanes segmentados:** cada actividad atrae a un público concreto (aves→birders, vía verde→ciclistas, camaleón→familias, etc.) y desde ahí se le encadena el resto para alargar estancia y desestacionalizar. El propio calendario natural reparte los públicos por todo el año: el grueso de la actividad de naturaleza cae fuera del verano, sin forzarlo.
- **Todo dentro de Rota.** Descartado apoyar el discurso en Doñana y el Estrecho (no son actividades de la asociación).
- **El Ad Grant / publicidad de pago es un canal más, no el eje.** La web, el SEO y el contenido tiran igual o más, sin coste por clic. Tres objetivos paralelos: visitas/ingreso, socios+donaciones/sostenibilidad, notoriedad/patrimonio.
- **Los corrales como "escondite natural vivo"** hilan todos los deliverables y conectan la guía gratuita con la oferta de visitas guiadas.

### Pendiente de cerrar (el detalle del plan)
- Calendario mes a mes: qué campaña se activa y cuándo.
- Objetivos concretos y cómo se miden.
- Por qué joya se empieza (no se lanzan todas a la vez).

## Modo de trabajo

- Deliverables como HTML autocontenidos bilingües/multiidioma, renderizados a PDF cuando hace falta.
- Sistema de marca reutilizado verbatim (mismos bloques `<style>`), solo cambia el copy entre idiomas.
- QA visual página a página tras generar (sirviendo `dist/` o el PDF).
- El proyecto vive en el repo `dbasco/Corrales`; el estado de los activos se lleva en `01-ACTIVOS.md`. El Drive solo aporta fotos.

## Imágenes: `height:auto` en la regla base (2026-07-22)

Los atributos `width`/`height` que `build.py` inyecta en cada `<img>` (anti-CLS) fijaban
también la **altura usada**, porque la regla base era `img{max-width:100%;display:block}`
sin `height:auto`. Consecuencia: `aspect-ratio` no surtía efecto y las fotos de los bloques
`split` salían verticales (484×1012 en vez de 484×363), dejando la columna de texto con
~620 px de hueco. Detectado revisando en local.

- `templates/base.css`: `img{max-width:100%;height:auto;display:block}`. `.hero .bg`,
  `.band .bg` y `.video img` fijan su propia altura, así que no les afecta.
- `templates/site.css`: `.figure img` acotada a 820 px de ancho, para que una foto cuadrada
  no ocupe la pantalla entera ni se amplíe por encima de su resolución nativa.

Regla general: ninguna imagen debe mostrarse más ancha que su resolución nativa.
Única excepción viva: `joya-pinar.jpg` (761 px) en el hero de la joya del pinar.
