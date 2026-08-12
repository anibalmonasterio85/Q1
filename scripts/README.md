# Scripts de Mantenimiento

Este directorio agrupa utilidades y scripts de soporte del proyecto.

## Archivos principales

* `init_database.py` — Crea y configura la base de datos inicial.
* `health_check.py` — Verifica configuración, dependencias y acceso a servicios.
* `apply_migration.py` — Aplica migraciones SQL y cambios estructurales.
* `reset_admin.py` — Resetea la contraseña del administrador.
* `replace_emojis.py` — Reemplaza emojis por iconos en las plantillas.
* `restaurar_cuentas.py` — Genera cuentas de usuario y restablece datos de prueba.
* `setup.py` — Configuración de entorno inicial, instalación de dependencias y preparativos.

## Uso típico

```bash
python scripts/init_database.py
python scripts/health_check.py
python scripts/restaurar_cuentas.py
```

> Nota: los scripts de despliegue se movieron a `deployment/start.ps1` y `deployment/stop.ps1`.
