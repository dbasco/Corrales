<?php
/*
 * contacto.php — receptor del formulario de contacto de loscorralesderota.com
 *
 * Va en la RAÍZ del servidor, junto a index.html. Es el único fichero dinámico
 * del sitio; las páginas siguen siendo HTML estático.
 *
 * Flujo: el formulario hace POST aquí -> se valida -> se envía el correo ->
 * se vuelve a la página de origen con ?envio=ok o ?envio=error#contacto, y el
 * JS de la página muestra el aviso.
 *
 * Requiere que la función mail() de PHP esté activa en el hosting (lo normal en
 * hosting compartido). Si el hosting exige SMTP autenticado, hay que sustituir
 * la llamada a mail() por PHPMailer; el resto del fichero no cambia.
 */

// ---------- Configuración (debe coincidir con "forms" de site.config.json) ----------
$DESTINO  = 'info@loscorralesderota.com';
$REMITE   = 'web@loscorralesderota.com';   // debe ser del propio dominio: si no, spam
$VOLVER_A = '/#contacto';                  // por si no llega la página de origen

// ---------- Solo POST ----------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . $VOLVER_A, true, 303);
    exit;
}

// A dónde volver: la página desde la que se envió, si es de este mismo sitio.
$origen = $VOLVER_A;
if (!empty($_SERVER['HTTP_REFERER'])) {
    $r = parse_url($_SERVER['HTTP_REFERER']);
    if (!empty($r['host']) && !empty($_SERVER['HTTP_HOST']) && $r['host'] === $_SERVER['HTTP_HOST']) {
        $origen = $r['path'] ?? '/';
    }
}
function volver($origen, $estado) {
    $sep = (strpos($origen, '?') === false) ? '?' : '&';
    header('Location: ' . $origen . $sep . 'envio=' . $estado . '#contacto', true, 303);
    exit;
}

// ---------- Trampa antispam ----------
// Campo invisible para personas. Si viene relleno, es un bot: se responde "ok"
// para no darle pistas, pero no se envía nada.
if (!empty($_POST['apellido2'])) {
    volver($origen, 'ok');
}

// ---------- Validación ----------
$nombre  = trim($_POST['nombre']  ?? '');
$email   = trim($_POST['email']   ?? '');
$mensaje = trim($_POST['mensaje'] ?? '');
$consent = !empty($_POST['consent']);

// Longitud en caracteres si hay mbstring; si no, en bytes (basta como tope).
function largo($s) { return function_exists('mb_strlen') ? mb_strlen($s, 'UTF-8') : strlen($s); }

if ($nombre === '' || $mensaje === '' || !$consent
    || !filter_var($email, FILTER_VALIDATE_EMAIL)
    || largo($nombre) > 80 || largo($email) > 120 || largo($mensaje) > 3000) {
    volver($origen, 'error');
}

// Inyección de cabeceras: cualquier salto de línea en nombre o email es un ataque.
if (preg_match('/[\r\n]/', $nombre . $email)) {
    volver($origen, 'error');
}

// ---------- Correo ----------
$asunto = 'Contacto web — ' . $nombre;

$cuerpo = "Mensaje enviado desde el formulario de loscorralesderota.com\n\n"
        . "Nombre: $nombre\n"
        . "Email:  $email\n"
        . "Fecha:  " . date('d/m/Y H:i') . "\n"
        . "IP:     " . ($_SERVER['REMOTE_ADDR'] ?? '-') . "\n"
        . str_repeat('-', 50) . "\n\n"
        . $mensaje . "\n";

$cabeceras = [
    'From: Web Corrales de Rota <' . $REMITE . '>',
    'Reply-To: ' . $nombre . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
];

$ok = @mail($DESTINO, '=?UTF-8?B?' . base64_encode($asunto) . '?=', $cuerpo, implode("\r\n", $cabeceras));

volver($origen, $ok ? 'ok' : 'error');
