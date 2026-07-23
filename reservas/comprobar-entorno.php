<?php
declare(strict_types=1);

/*
 * comprobar-entorno.php — diagnostico del servidor para el motor de reservas.
 *
 * Uso por linea de comandos (preferido):
 *     php comprobar-entorno.php
 *
 * Uso por web (si no hay SSH): edita CLAVE_WEB aqui abajo, pon una cadena larga,
 * sube el fichero y visita  https://reservas.…/comprobar-entorno.php?clave=LOQUEPUSISTE
 * BORRA EL FICHERO DEL SERVIDOR EN CUANTO TERMINES: revela informacion util a un atacante.
 *
 * No modifica nada. Lo unico que escribe es una tabla temporal que borra al salir.
 */

const CLAVE_WEB = '';

$cli = PHP_SAPI === 'cli';
if (!$cli) {
    if (CLAVE_WEB === '' || !isset($_GET['clave']) || !hash_equals(CLAVE_WEB, (string) $_GET['clave'])) {
        http_response_code(404);
        exit;
    }
    header('Content-Type: text/plain; charset=utf-8');
}

$fallos = 0;
$avisos = 0;

function titulo(string $t): void
{
    echo "\n" . $t . "\n" . str_repeat('-', strlen($t)) . "\n";
}

function ok(string $t, string $detalle = ''): void
{
    echo '  [ OK ]   ' . $t . ($detalle !== '' ? '  ' . $detalle : '') . "\n";
}

function aviso(string $t, string $detalle = ''): void
{
    global $avisos;
    $avisos++;
    echo '  [AVISO]  ' . $t . ($detalle !== '' ? '  ' . $detalle : '') . "\n";
}

function fallo(string $t, string $detalle = ''): void
{
    global $fallos;
    $fallos++;
    echo '  [FALLO]  ' . $t . ($detalle !== '' ? '  ' . $detalle : '') . "\n";
}

echo "Motor de reservas - Los Corrales de Rota\n";
echo 'Comprobacion del entorno - ' . date('Y-m-d H:i:s') . "\n";

titulo('1. PHP');

$version = PHP_VERSION;
if (version_compare($version, '8.1.0', '>=')) {
    ok('Version de PHP', $version);
} elseif (version_compare($version, '8.0.0', '>=')) {
    aviso('Version de PHP', $version . ' (funciona, pero 8.1+ es lo recomendado)');
} else {
    fallo('Version de PHP', $version . ' (hace falta 8.0 como minimo)');
}

echo '  ' . str_repeat(' ', 9) . 'SAPI: ' . PHP_SAPI . "\n";

$extensiones = ['pdo', 'pdo_mysql', 'json', 'filter', 'session', 'hash', 'ctype', 'openssl'];
foreach ($extensiones as $ext) {
    if (extension_loaded($ext)) {
        ok('Extension ' . $ext);
    } else {
        fallo('Extension ' . $ext, 'no cargada');
    }
}

if (extension_loaded('mbstring')) {
    ok('Extension mbstring', '(opcional, presente)');
} else {
    aviso('Extension mbstring', 'no cargada; el codigo no depende de ella, pero conviene');
}

$zona = date_default_timezone_get();
if ($zona === 'Europe/Madrid') {
    ok('Zona horaria', $zona);
} else {
    aviso('Zona horaria', $zona . ' (deberia ser Europe/Madrid; se puede fijar en php.ini o en el codigo)');
}

$memoria = ini_get('memory_limit');
echo '  ' . str_repeat(' ', 9) . 'memory_limit: ' . $memoria . '   max_execution_time: ' . ini_get('max_execution_time') . "\n";

$deshabilitadas = array_filter(array_map('trim', explode(',', (string) ini_get('disable_functions'))));
if ($deshabilitadas) {
    echo '  ' . str_repeat(' ', 9) . 'Funciones deshabilitadas: ' . implode(', ', $deshabilitadas) . "\n";
}

titulo('2. Configuracion de la app');

$rutaConfig = __DIR__ . '/config.php';
$hayConfig = is_file($rutaConfig);

if (!$hayConfig) {
    fallo('config.php', 'no existe; copia config.example.php a config.php y rellenalo');
} else {
    ok('config.php', 'presente');

    $permisos = substr(sprintf('%o', fileperms($rutaConfig)), -4);
    if (in_array($permisos, ['0600', '0640', '0644', '0400', '0440'], true)) {
        ok('Permisos de config.php', $permisos);
    } else {
        aviso('Permisos de config.php', $permisos . ' (lo razonable es 0640 o 0600)');
    }

    require_once __DIR__ . '/src/Config.php';
    require_once __DIR__ . '/src/Db.php';

    $faltan = [];
    foreach (['bd.host', 'bd.nombre', 'bd.usuario', 'app.url'] as $clave) {
        if ((string) Config::get($clave, '') === '') {
            $faltan[] = $clave;
        }
    }
    if ($faltan) {
        fallo('Valores sin rellenar en config.php', implode(', ', $faltan));
    } else {
        ok('Valores minimos de config.php', 'rellenados');
    }
}

titulo('3. Base de datos');

if (!$hayConfig) {
    echo "  (saltado: sin config.php no se puede conectar)\n";
} else {
    try {
        $pdo = Db::conn();
        $servidor = (string) $pdo->getAttribute(PDO::ATTR_SERVER_VERSION);
        ok('Conexion', $servidor);

        $esMaria = stripos($servidor, 'mariadb') !== false;
        $numero  = (string) preg_replace('/[^0-9.].*$/', '', $servidor);
        if ($esMaria) {
            version_compare($numero, '10.3', '>=')
                ? ok('Version de MariaDB', $numero)
                : fallo('Version de MariaDB', $numero . ' (hace falta 10.3+)');
        } else {
            version_compare($numero, '5.7', '>=')
                ? ok('Version de MySQL', $numero)
                : fallo('Version de MySQL', $numero . ' (hace falta 5.7+)');
        }

        $innodb = Db::fila("SHOW ENGINES WHERE Engine = 'InnoDB'");
        if ($innodb && in_array(strtoupper((string) $innodb['Support']), ['YES', 'DEFAULT'], true)) {
            ok('Motor InnoDB', $innodb['Support']);
        } else {
            fallo('Motor InnoDB', 'no disponible; sin InnoDB no hay transacciones ni claves foraneas');
        }

        $charset = Db::fila("SHOW VARIABLES LIKE 'character_set_database'");
        if ($charset && stripos((string) $charset['Value'], 'utf8mb4') !== false) {
            ok('Juego de caracteres de la BD', (string) $charset['Value']);
        } else {
            aviso('Juego de caracteres de la BD', ($charset['Value'] ?? '?') . ' (se recomienda utf8mb4)');
        }

        // Permisos: crear, indexar, insertar en transaccion y borrar.
        try {
            $pdo->exec('CREATE TABLE IF NOT EXISTS _prueba_entorno (
                id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                v  VARCHAR(20) NULL,
                PRIMARY KEY (id),
                KEY ix_v (v)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4');
            ok('Permiso CREATE + INDEX');

            $pdo->beginTransaction();
            $pdo->exec("INSERT INTO _prueba_entorno (v) VALUES ('x')");
            $pdo->rollBack();
            $quedan = Db::fila('SELECT COUNT(*) AS n FROM _prueba_entorno');
            if ((int) $quedan['n'] === 0) {
                ok('Transacciones', 'el rollback funciona de verdad');
            } else {
                fallo('Transacciones', 'el rollback no deshizo la insercion: la tabla no es transaccional');
            }

            $pdo->exec('DROP TABLE _prueba_entorno');
            ok('Permiso DROP');
        } catch (Throwable $e) {
            fallo('Permisos sobre la base de datos', $e->getMessage());
        }

        try {
            $tablas = Db::filas('SHOW TABLES');
            $n = count($tablas);
            if ($n === 0) {
                ok('Estado del esquema', 'base de datos vacia, lista para migrar.php');
            } else {
                $hayMigraciones = Db::fila("SHOW TABLES LIKE 'migraciones'");
                $hayMigraciones
                    ? ok('Estado del esquema', $n . ' tablas; migraciones ya aplicadas')
                    : aviso('Estado del esquema', $n . ' tablas y ninguna es "migraciones": la BD no esta vacia');
            }
        } catch (Throwable $e) {
            aviso('No se pudo listar tablas', $e->getMessage());
        }
    } catch (Throwable $e) {
        fallo('Conexion a la base de datos', $e->getMessage());
    }
}

titulo('4. Correo');

if (function_exists('mail')) {
    ok('Funcion mail()', 'disponible (la app no la usa: envia por SMTP)');
} else {
    aviso('Funcion mail()', 'no disponible (no es bloqueante: la app envia por SMTP)');
}

if ($hayConfig) {
    $host   = (string) Config::get('correo.smtp.host', '');
    $puerto = (int) Config::get('correo.smtp.puerto', 0);
    if ($host === '' || $puerto === 0) {
        aviso('SMTP en config.php', 'sin rellenar todavia');
    } else {
        $err = 0;
        $msg = '';
        $con = @fsockopen(($puerto === 465 ? 'ssl://' : '') . $host, $puerto, $err, $msg, 8);
        if ($con) {
            $saludo = (string) fgets($con, 512);
            fclose($con);
            ok('Conexion al SMTP', $host . ':' . $puerto . '  ' . trim($saludo));
        } else {
            fallo('Conexion al SMTP', $host . ':' . $puerto . '  ' . $msg . ' (puerto de salida cerrado?)');
        }
    }
}

titulo('5. Ficheros y rutas');

echo '  ' . str_repeat(' ', 9) . 'Carpeta de la app: ' . __DIR__ . "\n";
if (!$cli) {
    echo '  ' . str_repeat(' ', 9) . 'Docroot declarado: ' . ($_SERVER['DOCUMENT_ROOT'] ?? '?') . "\n";
    $docroot = realpath((string) ($_SERVER['DOCUMENT_ROOT'] ?? ''));
    $publico = realpath(__DIR__ . '/public');
    if ($docroot && $publico && rtrim($docroot, '/') === rtrim($publico, '/')) {
        ok('Docroot', 'apunta a reservas/public/, correcto');
    } else {
        aviso('Docroot', 'no apunta a reservas/public/; hay que corregirlo o proteger las carpetas con .htaccess');
    }
}

foreach (['src', 'migraciones', 'public'] as $carpeta) {
    is_dir(__DIR__ . '/' . $carpeta)
        ? ok('Carpeta ' . $carpeta)
        : fallo('Carpeta ' . $carpeta, 'no existe: subida incompleta?');
}

titulo('Resumen');

echo "  Fallos: $fallos    Avisos: $avisos\n";
if ($fallos === 0) {
    echo "  Entorno apto. Siguiente paso: php migrar.php\n";
} else {
    echo "  Hay que resolver los fallos antes de continuar.\n";
}
echo "\n";

exit($fallos === 0 ? 0 : 1);
