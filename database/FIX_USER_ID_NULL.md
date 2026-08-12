# Fix para Error: Column 'user_id' cannot be null

## Problema
Al escanear un QR desconocido, la aplicación falla porque intenta insertar `user_id=NULL` en la tabla `accesos_log`, pero la columna estaba configurada como `NOT NULL`.

## Solución
Ejecuta este comando en MySQL para permitir valores NULL en la columna `user_id`:

```sql
USE qr_access;
ALTER TABLE accesos_log MODIFY COLUMN user_id INT NULL;
```

### Opción 1: Ejecutar directamente en MySQL
```bash
mysql -h localhost -P 3307 -u admin -p -e "USE qr_access; ALTER TABLE accesos_log MODIFY COLUMN user_id INT NULL;"
# Contraseña: admin
```

### Opción 2: Ejecutar el script de migración
```bash
mysql -h localhost -P 3307 -u admin -p qr_access < database/fix_user_id_nullable.sql
# Contraseña: admin
```

### Opción 3: Usar herramienta gráfica (MySQL Workbench)
1. Abre MySQL Workbench
2. Conéctate a `localhost:3307` con usuario `admin`
3. Ejecuta el contenido del archivo `database/fix_user_id_nullable.sql`

## Verificación
Después de aplicar la migración, prueba escanear un QR desconocido. Debería registrar el acceso como "denegado" sin errores de base de datos.

## Cambios en el código
- ✅ `web_panel/models/access_log.py` - ahora acepta parámetro `detalles`
- ✅ `web_panel/routes/scanner.py` - registra detalles del rechazo
