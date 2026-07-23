<?php
declare(strict_types=1);

/*
 * migrar.php — aplica las migraciones pendientes de migraciones/*.sql.
 *
 * Uso:  php migrar.php          aplica lo que falte
 *       php migrar.php --estado solo informa, no toca nada
 *
 * Solo por linea de comandos: no debe quedar accesible por web.
 */

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}

require_once __DIR__ . '/src/Config.php';
require_once __DIR__ . '/src/Db.php';

$soloEstado = in_array('--estado', $argv, true);

Db::conn()->exec(
    'CREATE TABLE IF NOT EXISTS migraciones (
        fichero  VARCHAR(120) NOT NULL,
        aplicada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (fichero)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci'
);

$aplicadas = [];
foreach (Db::filas('SELECT fichero FROM migraciones') as $fila) {
    $aplicadas[$fila['fichero']] = true;
}

$ficheros = glob(__DIR__ . '/migraciones/*.sql') ?: [];
sort($ficheros);

$pendientes = 0;
foreach ($ficheros as $ruta) {
    $nombre = basename($ruta);

    if (isset($aplicadas[$nombre])) {
        echo "  ok   $nombre\n";
        continue;
    }

    $pendientes++;

    if ($soloEstado) {
        echo "  --   $nombre (pendiente)\n";
        continue;
    }

    $sql = file_get_contents($ruta);
    if ($sql === false || trim($sql) === '') {
        fwrite(STDERR, "No se pudo leer $nombre\n");
        exit(1);
    }

    try {
        Db::conn()->exec($sql);
        Db::ejecutar('INSERT INTO migraciones (fichero) VALUES (?)', [$nombre]);
        echo "  +    $nombre aplicada\n";
    } catch (Throwable $e) {
        fwrite(STDERR, "FALLO en $nombre: " . $e->getMessage() . "\n");
        fwrite(STDERR, "Nada mas se ha aplicado. Corrige y vuelve a ejecutar.\n");
        exit(1);
    }
}

if ($pendientes === 0) {
    echo "Sin migraciones pendientes.\n";
} elseif ($soloEstado) {
    echo "$pendientes pendiente(s).\n";
} else {
    echo "Listo: $pendientes aplicada(s).\n";
}
