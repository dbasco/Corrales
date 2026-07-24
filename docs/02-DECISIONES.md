# 02 · Decisiones — Los Corrales de Rota

> Lo que ya está cerrado y por qué. El "qué ya no se discute".
> Si una decisión se revierte, se anota aquí con fecha — no se borra.
> Última revisión: 2026-07-23

---

## Web y arquitectura técnica

> **Estado de la web (2026-07-23):** v1 ES construida y en `main` (13 páginas). El generador se
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
- **Corrales activos:** ~~se mantiene **8**~~ → **corregido a 5 el 2026-07-24** por la asociación (config `corrales_activos: 5`). La web oficial no da número de activos; la fuente autoritativa es la propia asociación. Aplicado en `site.config.json`, la banda de cifras y los dos textos de la home (ES y EN).

## Reservas de visitas — estado actual (2026-07-22)

- **Por ahora, las visitas a los corrales se gestionan EXCLUSIVAMENTE por la Oficina de Turismo de Rota** (tel. 956 846345, turismorota@gmail.com). La asociación guía la visita; la reserva la lleva Turismo. No hay reserva por email de la asociación ni "reserva online".
- ~~**El motor de reservas propio queda APLAZADO** — no se desarrolla ahora. Su definición de alto nivel (abajo) se conserva para cuando se retome.~~ **Retomado el 2026-07-23:** se desarrolla ya (ver «App de reservas» y `reservas-arquitectura.md`). Hasta que esté en marcha, el punto de arriba sigue vigente: la reserva la lleva Turismo y la web v1 no tiene botón «Reservar».
- **En la web v1**, la sección de reserva de `/visita/` dirige a la Oficina de Turismo de Rota (teléfono y correo); se quitó "reserva online próximamente" y el email de la asociación como canal de reserva.
- **Las joyas NO llevan botón de reserva** (no se reservan): su CTA es "La visita a los corrales" y lleva a `/visita/`. Lo único reservable es la visita a los corrales.
- **"Aves" no ocupa sitio en el menú principal**: es una joya más; se llega por "Joyas de Rota". El menú queda: La visita · Joyas de Rota · Contacto.

## App de reservas

> Definición de alto nivel cerrada el 2026-07-22. La reserva es el nodo al que devuelven todas las joyas. Encaje en la web en `web-arquitectura-corrales.md`.
> **Se retoma el 2026-07-23** (deja de estar aplazada). El **cómo** se implementa está en
> `reservas-arquitectura.md`; abajo, la revisión que cambia el modelo de disponibilidad.

- **A medida, hecha con IA — no SaaS.** Ningún SaaS gestiona bien la disponibilidad por marea. Contrapartida asumida: es la única pieza con backend propio (servidor + BD); el resto del sitio sigue estático.
- **Subdominio propio:** `reservas.loscorralesderota.com`, aislada del sitio estático para no tocar su rendimiento. Interfaz y correos en ES/EN/DE/FR; hereda el idioma con el que llega el visitante.
- **Gratis, sin cobro.** La app NO lleva pasarela. Los ingresos son siempre por donativo, por su vía aparte (Bizum/tarjeta), nunca acoplados al flujo de reserva.
- **Catálogo de tipos de visita.** La "visita a los corrales" es el primer tipo de un catálogo. Cada tipo: nombre, descripción, características (duración, qué incluye, guía, idioma) y aforo por defecto. Más adelante se dan de alta otras joyas sin tocar código.
- ~~**Disponibilidad manual con asistente de mareas.** Modelo: tipo de visita → día → pase (con aforo). El admin abre los días; para los tipos "depende de marea" (corrales) el asistente propone las ventanas de bajamar visitables a partir de la tabla de mareas de Rota, y el admin las acepta o ajusta. Nada se publica solo. Los tipos que no dependen de marea se abren con horario normal.~~ **Superado el 2026-07-23** — ver la revisión al final de esta sección. Se mantiene el modelo tipo de visita → día → pase (con aforo); cae el asistente.
- **Aforo por personas**, configurable por pase; cada reserva descuenta su nº de personas.
- **Confirmación por código.** Flujo: tipo → día → pase → nombre + email + nº personas → recibe un **código por email** → lo introduce → reserva confirmada + email con los datos y enlace de cancelación. Sin confirmar, la reserva queda pendiente y caduca.
- **Cancelación:** (a) el admin anula un pase o un día entero (marea, tiempo) → todas las reservas de ese pase pasan a canceladas y se avisa por email a cada afectado; (b) el visitante cancela su reserva desde el enlace del email y libera sus plazas.
- **Email transaccional** (código, confirmación y avisos): resuelto en `reservas-arquitectura.md` — cola en BD + cron, SMTP autenticado del propio dominio con PHPMailer, con Brevo/Mailjet como alternativa si falla la entregabilidad. Queda confirmar el buzón remitente y sus credenciales en el hosting.

### Revisión 2026-07-23 — la disponibilidad la decide el equipo; la marea es informativa

**Si hay visita, qué día y a qué hora lo decide el equipo.** No hay cálculo de mareas que abra,
cierre ni valide nada. La información de marea es orientativa y no afecta a las reservas.

- **Cae el asistente de mareas** como motor de disponibilidad, y con él el umbral de altura, los
  márgenes de seguridad, el cálculo de la curva y la calibración con los corraleros. Era la pieza
  más cara e incierta del desarrollo.
- **Lo sustituye la creación en lote de pases** en el panel (rango de fechas + días de la semana +
  horas, duplicar una semana en la siguiente, editar o anular cualquier pase suelto después).
  Bastante más barato de construir.
- **La marea queda como columna informativa** en el calendario del panel — la hora de la bajamar
  prevista, a la vista de quien decide. No valida ni propone. Va al final del desarrollo y, si
  estorba o la fuente de datos no acompaña, se cae sin consecuencias.
- El motivo original de «a medida y no SaaS» era que ningún SaaS gestiona bien la disponibilidad
  por marea. Ese motivo decae, pero la decisión **se mantiene** por los otros: gratis sin pasarela,
  catálogo propio de tipos de visita, cuatro idiomas y coste cero de licencias. No se reabre.
- **Reserva a nombre de un tercero** desde el panel, para quien llama por teléfono o se presenta:
  descuenta plazas igual que una reserva web, así el aforo publicado nunca miente. Pantalla
  genérica, sirva quien sirva ese canal. Cómo se reparte el canal con la Oficina de Turismo es
  asunto de la asociación y no condiciona el desarrollo.

Confirmado además que el hosting incluye **MySQL, cron y SMTP autenticado**, que es lo que
sostiene la elección de plataforma (PHP 8 + MySQL en el hosting actual) en `reservas-arquitectura.md`.

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

## Diagrama de mareas: ilustraciones IA con rótulos en HTML (2026-07-23)

Las tres escenas del bloque `diagram` del inicio pasan de SVG esquemático a **ilustración**
(estilo grabado, generada con Google Gemini a petición de la asociación).

- **Regla aplicada: la ilustración no lleva texto.** Los rótulos y pies siguen en HTML, así
  que se traducen a EN/DE/FR sin regenerar imágenes, se leen en móvil y son accesibles.
  Se descartó la primera versión de la lámina, que traía todo el texto incrustado.
- `build.py`: un `step` del diagrama con `img` usa la ilustración; sin `img`, cae al SVG.
  El cambio es reversible.
- Al recortar se quitaron la rosa de los vientos, la barra de escala (mal graduada) y el
  destello de Gemini.

### Abierto — dos puntos que decide la asociación
1. **El muro sale más alto de lo que es.** El texto del propio inicio dice «un muro *bajo*
   de piedra seca» y la ilustración muestra una fábrica alta con cimentación. Contradicción
   entre lo que se lee y lo que se ve, y entre la lámina y lo que el visitante encuentra.
   Se puede regenerar pidiendo un muro a la altura de la cintura, sin cimientos profundos.
2. **Declarar o no que la ilustración es generada con IA.** Recomendación: hacerlo en el pie
   o en créditos. Es una web patrimonial y la transparencia protege la credibilidad; además
   las imágenes llevan la marca invisible SynthID de Google, detectable por terceros.

## Reparto inicio / monumento y ritmo vertical (2026-07-23)

- **El «cómo funciona» se va a `/monumento-natural/`.** Las tres escenas ilustradas pasan
  del inicio a la página del monumento, que es donde toca explicar. Allí **sustituyen al
  corte SVG** (`templates/corral-corte.svg`), que contaba lo mismo: se retira de la web y
  se conserva en `templates/` para la guía en PDF.
- **El inicio gana un mosaico de seis fotos** (bloque `gallery`, «Piedra, agua y oficio») en
  el lugar que ocupaba el diagrama. El inicio vende, el monumento explica.

### Ritmo vertical entre secciones
Detectado a partir de una revisión en local: el aire superior e inferior de las secciones no
era coherente. La regla `main > section + section{padding-top:0}` anulaba el techo de toda
sección que siguiera a otra, y solo lo recuperaban las que llevan tono; el resultado era que
«Piedra, marea y trabajo a pie» y «Escríbenos» quedaban pegadas al bloque anterior, mientras
otras tenían 100 px. Además, entre dos secciones el aire se suma, así que donde no se
colapsaba salían 200 px, el doble del ritmo.

Ahora:
- Secciones **sin** tono: medio aire (`--sp * .55`). Dos seguidas dan ~110 px, el ritmo completo.
- Secciones **con** tono: aire entero; ahí es margen interior del bloque de color.
- Dos bloques del **mismo** fondo seguidos: se colapsa el techo del segundo (sin cambio de
  color, 200 px se leen como un hueco).

Resultado medido: separaciones de 110–155 px; solo quedan 200 px entre dos bloques de color
distinto, donde cada uno respira el suyo.

## Contraste de botones (2026-07-23)

Detectado revisando una captura: el botón **«Cómo visitar» de la barra de navegación** era
casi ilegible, **1,71 de contraste** (el mínimo AA es 4,5). Causa: `.navbar .links a` fijaba
`color:var(--roca)` y, por especificidad, pisaba el `color:var(--sal)` de `.btn-primary`.
El mismo botón fuera de la barra daba 8,40, lo que confirmaba el diagnóstico.

- `base.css`: los enlaces de la barra pasan a `.navbar .links a:not(.btn)`, en escritorio y
  en móvil. Los botones conservan su propio color. **1,71 → 8,40.**
- `.btn-accent` daba 4,46, justo por debajo del mínimo: su texto pasa de `--sal` a blanco
  puro. **4,46 → 5,03.** No se toca `--oxido`, solo el color de texto del componente.

Verificado en escritorio y en móvil con el menú abierto: todos los botones ≥ 4,5.

### Resuelto el 2026-07-23 — ver «Contraste del kicker sobre fondo claro» más abajo
_(se deja el diagnóstico original)_

### Abierto — los kickers no llegan al mínimo
Los kickers usan `--oxido` sobre fondos claros y se quedan cortos para texto pequeño:
surface 4,82 (pasa), **sal 4,46**, **sand 4,06**. El del hero va sobre el velo oscuro de la
foto y cumple de sobra (8,49).

No se cambia por decisión propia porque es color de marca. Si se quiere cumplir AA en los
tres fondos, el mínimo es **#9E5330** (5,39 / 4,98 / 4,54); **#98502E** deja más margen.
Afecta solo al color de texto del kicker, no al token `--oxido` ni a los botones.

## Fuentes servidas desde el propio dominio (2026-07-23)

Cinzel y Spectral se cargaban desde el CDN de Google Fonts: dos `preconnect` y una hoja
de estilos externa en la ruta crítica de cada página, y la IP de cada visitante enviada a
Google antes de consentir nada (hay jurisprudencia alemana al respecto, LG München I, 2022).

- Los `.ttf` se bajan de `google/fonts`, se subsetean a **latin** y se convierten a `woff2`:
  Cinzel variable (400–700, un solo fichero) y Spectral 400/500/600/700. **108 KB en total**,
  en `assets/fonts/`. Verificado que el subconjunto cubre ES/EN/DE/FR (`ß ñ ç œ ¿¡ «» — €`).
- Los `@font-face` viven en `base.css` (que va inlineado); `build.py` precarga las dos de la
  primera pintura. Se retiran los tres `<link>` a Google.
- Comprobado en Chromium: las páginas **no hacen ninguna petición a terceros** salvo GTM.

## Formulario de contacto: `contacto.php` (2026-07-23)

El formulario era `onsubmit="return false"`: el visitante escribía, pulsaba Enviar y el
mensaje se perdía en silencio. Peor que no tenerlo.

- **Receptor propio en PHP** (`contacto.php` en la raíz), no un servicio externo: el hosting
  tiene PHP, así que no hace falta cuenta de terceros ni enviar datos personales fuera.
  Es el **único fichero dinámico**; las 13 páginas siguen siendo HTML estático.
- Validación en servidor, trampa antispam (campo invisible), protección contra inyección de
  cabeceras y **casilla de consentimiento obligatoria** enlazada a `/privacidad/`.
- El remitente debe ser una dirección del propio dominio (`web@loscorralesderota.com`); con
  el correo del visitante como remitente, el envío cae en spam. Su correo va en `Reply-To`.
- **Salvaguarda:** si `forms.endpoint` está vacío en `site.config.json`, el formulario no se
  pinta y en su lugar sale el email como enlace. No puede volver a publicarse un formulario mudo.
- No depende de la extensión *mbstring*, que no está garantizada en todos los hostings.
- **Pendiente de confirmar con el hosting:** que la función `mail()` esté activa. Si exige
  SMTP autenticado, se sustituye esa línea por PHPMailer; el resto del fichero no cambia.

## Modo pruebas del build (2026-07-23)

`python3 build.py --preview https://pruebas.ejemplo.com` construye el sitio apuntando a esa
URL en canonical/hreflang/og/sitemap, mete `noindex,nofollow` en todas las páginas y genera un
`robots.txt` bloqueado. Permite revisar en el servidor **sin cambiar el dominio** y sin que
Google indexe la copia como contenido duplicado. Sin el flag, la salida es la de producción.

Las rutas internas (`/visita/`, `/assets/…`) no llevan dominio, así que funcionan en cualquier
servidor **siempre que el sitio esté en la raíz**. En una subcarpeta (`dominio.com/prueba/`)
se rompen todas: la prueba tiene que ir en la raíz de un subdominio.

## Contraste del kicker sobre fondo claro (2026-07-23)

Cerrado el punto que quedaba abierto ayer: `.kicker` pasa de `--oxido` a **`#98502E`**.
Ratios medidos en el navegador: sal **5,28**, surface **5,71**, sand **4,81** (antes 4,46 /
4,82 / 4,06). Se cambia solo el color del componente; el token `--oxido` no se toca, así que
botones y filetes quedan igual.

### Abierto — el kicker sobre foto NO cumple, y no es por este cambio

Midiendo en el navegador (ocultando el texto, fotografiando los píxeles reales de detrás y
comparando contra el percentil 95 de luminancia) resulta que el kicker del hero, que usa
`#e0ad88` sobre la foto, **falla en 7 de 8 páginas**: entre 1,86 y 4,66. La cifra de «8,49»
que figuraba en la nota de ayer se calculó contra el velo en su punto más oscuro, pero el
kicker está en la parte alta del hero, donde el velo solo tiene un 15 % de opacidad.

Probadas las dos palancas por separado y cruzadas: **ninguna combinación salva el color
cálido**. Reforzar el velo hasta `.55` deja el kicker en 3,92. La única que pasa es velo
`.35/.60/.85` **más el kicker en `--sal`** (4,87), y eso significa que el kicker del hero deja
de ser cálido y pasa a ser del mismo color que el titular.

El titular (`--sal`) solo falla en el inicio (3,75), por el sol de la foto del atardecer;
con el velo reforzado sube a 5,33.

**No se toca nada por decisión propia: es un cambio de aspecto, no un ajuste técnico.**
Decide la asociación entre (a) kicker del hero en `--sal` + velo reforzado, que cumple AA y
oscurece algo las fotos, o (b) mantener el cálido asumiendo que ese rótulo no cumple.

## Selector de idioma compacto en la barra (2026-07-23)

Al entrar el inglés, la barra pasó a seis elementos y quedó densa. Medido a 1280 px (el
contenedor son 1080): ocupaba 633 px de 806 disponibles — **no se desbordaba**, pero
simulando las etiquetas en alemán la holgura bajaba a 74 px.

Se descartó quitar «Contacto» del menú: con 173 px libres sería resolver un problema que
todavía no existe. Queda como opción para cuando entre el alemán.

- En la barra, el selector muestra **solo el código** (`ES` / `EN` / `DE` / `FR`) con la flecha;
  el desplegable conserva los nombres completos. `aria-label` («Idioma: Español») da el
  contexto que el código por sí solo no da.
- El código va en versalitas espaciadas, como los kickers: se lee como dato, no como un
  quinto enlace compitiendo con los otros cuatro.
- **Ganancia real: el selector pasa de 59 a 32 px**; la barra, de 633 a 604. Holgura 173 → 201 px
  en español y 74 → 102 px en alemán. Menos de lo estimado antes de medirlo (había calculado
  unos 15 px para el selector, sin contar la flecha ni el hueco interno).
- La ventaja que se mantiene: **no crece con el idioma**. «Deutsch» y «Français» ocuparían lo
  mismo que «Español», y el código no.

## «100 % de lo recaudado»: acotar el origen (2026-07-23)

El pie decía «El 100 % de lo recaudado va a la conservación del monumento», sin decir *de
qué* recaudación. Como en la v1 no hay donaciones y la reserva la lleva la Oficina de
Turismo, en el pie de todas las páginas quedaba ambiguo e invitaba a preguntarse dónde donar.

La web oficial lo formula acotado, y esa es la fórmula buena: «el 100% de la recaudación
obtenida **a través de las actividades y visitas guiadas** se destina íntegramente a la
conservación, **reconstrucción y mantenimiento** del Monumento Natural» (nota de transparencia).

Aplicado: pie (`content/ui.es.json`) y las dos menciones de `visita.json` pasan a nombrar el
origen y los tres destinos. Home y monumento ya lo decían en contexto de visita guiada.
Acotar no debilita el mensaje: una nota de transparencia es más creíble cuanto más precisa.

## Etiqueta de Google: gtag.js de Google Ads, no contenedor GTM (2026-07-24)

El ingeniero de la cuenta entrega la etiqueta de Google de la cuenta de Ads —
**`AW-17862259314`**, snippet `gtag.js`— en vez de un contenedor GTM. Se aplica tal cual:
es lo que hay y lo que la cuenta necesita para medir conversiones y remarketing.

- `site.config.json` → `tracking.provider` pasa a **`"gtag"`** y `google_ads_id` a
  `AW-17862259314`. `gtm_id` se queda con el placeholder: el provider decide qué se inyecta,
  así que volver a GTM es cambiar una palabra si algún día llega el contenedor.
- `build.py` inyecta el bloque en el `<head>` de las 26 páginas, **una sola vez por página**,
  después de los `preload` de fuentes (async, no bloquea la primera pintura) y antes del CSS
  inline. Con `provider: "gtag"` no se pinta el `<noscript>` de GTM: gtag.js no lo usa.
- Los IDs con `XXXX` se ignoran: si un ID es placeholder no se inyecta nada. Evita repetir el
  caso anterior de estar sirviendo un `GTM-XXXXXXX` que fallaba contra Google en cada visita.
- Si más adelante se añade GA4, basta poner su `G-…` en `ga4_id`: el generador emite un
  `gtag('config', …)` por cada ID real, con Ads primero.
- **Consecuencia:** la etiqueta ahora es real y **escribe cookies de Google**. El banner de
  consentimiento (issue #7, Consent Mode v2) pasa de "opcional si no se activa la analítica" a
  **bloqueante para publicar** con la etiqueta cargando.
