# Motor de reservas — Los Corrales de Rota

App de reservas del subdominio `reservas.loscorralesderota.com`. PHP 8 + MySQL,
sin framework. La web estática del dominio principal no depende de esto.

- **Arquitectura:** `docs/reservas-arquitectura.md` (raíz del repo).
- **Decisiones:** `docs/02-DECISIONES.md` › «App de reservas».
- **Fases y estado:** `docs/handover-issues.md` › lotes #10 a #14.

## Estado

Fase 1 hecha: esquema, configuración y capa de datos. Todavía **no hay app**:
ni panel, ni flujo público, ni correo.

## Instalar

1. Crear una base de datos vacía en el panel del hosting (utf8mb4).
2. Copiar `config.example.php` a `config.php` y rellenar base de datos y SMTP.
   `config.php` no se sube al repo: lleva credenciales.
3. Aplicar el esquema:

   ```
   php migrar.php            # aplica lo que falte
   php migrar.php --estado   # solo informa
   ```

4. Apuntar el subdominio a `reservas/public/`. **Solo `public/` debe ser accesible
   por web**; `src/`, `migraciones/`, `cron/` y `config.php` quedan fuera del
   docroot. Si el hosting no permite mover el docroot, hace falta un `.htaccess`
   que bloquee esas carpetas.

## Estructura

```
public/        docroot: index.php (público) y admin.php (panel)
src/           Config, Db y las clases de dominio
migraciones/   *.sql numeradas, se aplican una vez
cron/          tareas: caducar reservas, enviar correo, copia de seguridad
idiomas/       textos de interfaz y plantillas de email (es, en, de, fr)
vistas/        plantillas PHP
tests/         pruebas de aforo y estados
```

## Reglas del código

- **Sentencias preparadas siempre.** Todo pasa por `Db`.
- **El aforo se toca dentro de `Db::transaccion()` y con `Db::bloquearPase()`.**
  Sin ese bloqueo hay sobreventa en cuanto dos personas reserven a la vez.
- Nada de envío de correo dentro de la petición: se encola en `correo_cola` y lo
  manda el cron.
- Los textos visibles van en `idiomas/`, no incrustados en las vistas.
