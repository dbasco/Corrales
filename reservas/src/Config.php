<?php
declare(strict_types=1);

/**
 * Lee config.php (que vive solo en el servidor) y da acceso por ruta con puntos:
 * Config::get('bd.host'), Config::get('app.minutos_para_confirmar', 30).
 */
final class Config
{
    private static ?array $datos = null;

    public static function cargar(): array
    {
        if (self::$datos === null) {
            $ruta = dirname(__DIR__) . '/config.php';
            if (!is_file($ruta)) {
                throw new RuntimeException(
                    'Falta config.php. Copia config.example.php a config.php y rellenalo.'
                );
            }
            $datos = require $ruta;
            if (!is_array($datos)) {
                throw new RuntimeException('config.php debe devolver un array.');
            }
            self::$datos = $datos;
        }
        return self::$datos;
    }

    /**
     * @param mixed $defecto
     * @return mixed
     */
    public static function get(string $ruta, $defecto = null)
    {
        $valor = self::cargar();
        foreach (explode('.', $ruta) as $clave) {
            if (!is_array($valor) || !array_key_exists($clave, $valor)) {
                return $defecto;
            }
            $valor = $valor[$clave];
        }
        return $valor;
    }

    public static function esPruebas(): bool
    {
        return Config::get('app.entorno') === 'pruebas';
    }
}
