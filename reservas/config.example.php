<?php
/*
 * config.example.php — plantilla de configuración del motor de reservas.
 *
 * Copiar a config.php EN EL SERVIDOR y rellenar. config.php está en .gitignore
 * y no debe subirse nunca: lleva credenciales de base de datos y de correo.
 */

return [

    'bd' => [
        'host'    => 'localhost',
        'nombre'  => '',
        'usuario' => '',
        'clave'   => '',
        'charset' => 'utf8mb4',
    ],

    'app' => [
        'url'             => 'https://reservas.loscorralesderota.com',
        'web'             => 'https://loscorralesderota.com',
        // 'produccion' o 'pruebas'. En pruebas se muestran los errores.
        'entorno'         => 'produccion',
        'idioma_defecto'  => 'es',
        'idiomas'         => ['es', 'en', 'de', 'fr'],
        // Minutos que aguanta una reserva sin confirmar antes de caducar.
        'minutos_para_confirmar' => 30,
        // Horas de antelación del correo de recordatorio.
        'horas_recordatorio'     => 24,
        // Meses que se conservan las reservas pasadas antes del borrado automático.
        'meses_retencion'        => 12,
    ],

    'correo' => [
        // 'smtp' (PHPMailer) o 'registro' (solo escribe en el log; para pruebas).
        'transporte'      => 'smtp',
        'remitente'       => 'web@loscorralesderota.com',
        'nombre_remitente' => 'Los Corrales de Rota',
        'responder_a'     => 'info@loscorralesderota.com',
        'smtp' => [
            'host'      => '',
            'puerto'    => 587,
            'seguridad' => 'tls',
            'usuario'   => '',
            'clave'     => '',
        ],
    ],

];
