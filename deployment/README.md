# Deployment

Este directorio agrupa los archivos de despliegue e infraestructura del proyecto.

## Archivos

* `deployment/nginx.conf` — Configuración del proxy reverso Nginx.
* `deployment/start.ps1` — Script PowerShell para iniciar el servidor web.
* `deployment/stop.ps1` — Script PowerShell para detener el servidor.

## Uso

```powershell
# Iniciar la aplicación
powershell -ExecutionPolicy Bypass -File deployment/start.ps1

# Detener la aplicación
powershell -ExecutionPolicy Bypass -File deployment/stop.ps1
```

## Nota

El `docker-compose.yml` y el `Dockerfile` siguen en la raíz para mantener compatibilidad con la mayoría de flujos de CI/CD y despliegues locales.
