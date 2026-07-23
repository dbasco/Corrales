<?php
declare(strict_types=1);

require_once __DIR__ . '/Config.php';

/**
 * Acceso a la base de datos. Todo pasa por aqui: sentencias preparadas siempre,
 * sin excepcion. Si algun dia hay que cambiar MySQL por SQLite, el cambio vive
 * en conn() y en ningun otro sitio.
 */
final class Db
{
    private static ?PDO $pdo = null;

    public static function conn(): PDO
    {
        if (self::$pdo === null) {
            $bd  = Config::get('bd', []);
            $dsn = sprintf(
                'mysql:host=%s;dbname=%s;charset=%s',
                $bd['host'] ?? 'localhost',
                $bd['nombre'] ?? '',
                $bd['charset'] ?? 'utf8mb4'
            );
            self::$pdo = new PDO($dsn, $bd['usuario'] ?? '', $bd['clave'] ?? '', [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
            ]);
        }
        return self::$pdo;
    }

    public static function filas(string $sql, array $params = []): array
    {
        $st = self::conn()->prepare($sql);
        $st->execute($params);
        return $st->fetchAll();
    }

    public static function fila(string $sql, array $params = []): ?array
    {
        $st = self::conn()->prepare($sql);
        $st->execute($params);
        $fila = $st->fetch();
        return $fila === false ? null : $fila;
    }

    /** Devuelve el numero de filas afectadas. */
    public static function ejecutar(string $sql, array $params = []): int
    {
        $st = self::conn()->prepare($sql);
        $st->execute($params);
        return $st->rowCount();
    }

    /** Devuelve el id insertado. */
    public static function insertar(string $sql, array $params = []): int
    {
        self::ejecutar($sql, $params);
        return (int) self::conn()->lastInsertId();
    }

    /**
     * Ejecuta $fn dentro de una transaccion. Si ya hay una abierta, se limita a
     * ejecutarla (no anida). Cualquier excepcion deshace los cambios.
     *
     * @return mixed lo que devuelva $fn
     */
    public static function transaccion(callable $fn)
    {
        $pdo = self::conn();
        if ($pdo->inTransaction()) {
            return $fn($pdo);
        }
        $pdo->beginTransaction();
        try {
            $resultado = $fn($pdo);
            $pdo->commit();
            return $resultado;
        } catch (Throwable $e) {
            $pdo->rollBack();
            throw $e;
        }
    }

    /**
     * Bloquea la fila del pase y la devuelve. ESTA ES LA PIEZA CRITICA DEL AFORO:
     * sin este bloqueo, dos personas reservando a la vez sobre las ultimas plazas
     * leen el mismo plazas_ocupadas y se produce sobreventa.
     *
     * Solo tiene efecto dentro de una transaccion, asi que se exige.
     */
    public static function bloquearPase(int $paseId): ?array
    {
        if (!self::conn()->inTransaction()) {
            throw new LogicException('bloquearPase() debe llamarse dentro de Db::transaccion().');
        }
        return self::fila(
            'SELECT p.*, d.fecha, d.estado AS estado_dia, d.tipo_id
               FROM pases p
               JOIN dias d ON d.id = p.dia_id
              WHERE p.id = ?
              FOR UPDATE',
            [$paseId]
        );
    }

    public static function plazasLibres(array $pase): int
    {
        return max(0, (int) $pase['aforo'] - (int) $pase['plazas_ocupadas']);
    }
}
