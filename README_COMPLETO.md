# QR Access PRO 🔐

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-blue)

Sistema profesional de control de acceso mediante códigos QR dinámicos, diseñado para reemplazar tarjetas magnéticas con tecnología moderna de autenticación sin contacto. Implementa seguridad a nivel empresarial con hashing Scrypt, TOTP renovable cada 30 segundos, y gestión centralizada de credenciales mediante un panel administrativo web.

Perfecto para **empresas, oficinas, instalaciones industriales y organizaciones** que requieren control de acceso robusto, auditable y sin fricciones.

---

## 🌟 Características Principales

- **🔑 Identificación Sin Contacto**: Generación y lectura de códigos QR dinámicos con rotación TOTP cada 30 segundos para máxima seguridad.
- **🛡️ Seguridad Enterprise**: Hashing Scrypt para contraseñas, comunicación SSL/TLS, protección contra fuerza bruta con rate limiting integrado.
- **👥 Gestión Centralizada**: Panel administrativo para crear, editar, suspender y regenerar credenciales instantáneamente.
- **📋 Control Laboral**: Cálculo automático de turnos, reporte de horas trabajadas y detección de atrasos con análisis por usuario y período.
- **📊 Auditoría Completa**: Registro detallado de cada acceso (permitido/denegado), IP, timestamp y usuario asociado.
- **💾 Caché Distribuido**: Redis para optimizar performance y rate limiting sin requiere modificación de código.
- **📧 Notificaciones por Email**: Confirmación de registro, alertas de acceso denegado, y regeneración de credenciales.
- **📄 Exportación Múltiple**: PDF y Excel para reportes de accesos, nómina y estadísticas de turnos.
- **🎨 UI Dark Mode**: Interfaz moderna con gradientes y animaciones sutiles, totalmente responsive.
- **🐳 Dockerizable**: Configuración completa con Docker y Docker Compose para despliegue rápido.
- **📈 Escalable**: Arquitectura preparada para Redis, Nginx, Gunicorn y múltiples zonas de acceso con RBAC.

---

## 🏗️ Arquitectura del Proyecto

```
Q1/
├── web_panel/                   # Panel central (servidor Flask)
│   ├── app.py                  # Punto de entrada, factory pattern
│   ├── routes/                 # Blueprints por funcionalidad
│   │   ├── auth.py            # Login, registro, logout (rate-limited)
│   │   ├── dashboard.py       # Dashboard principal y estadísticas
│   │   ├── admin.py           # Gestión de usuarios y zonas
│   │   ├── api.py             # Endpoints JSON para frontend/externos
│   │   └── scanner.py         # Rutas auxiliares para el escáner
│   ├── models/                 # Capa de datos
│   │   ├── user.py            # CRUD usuarios, autenticación
│   │   ├── access_log.py      # Logging y consultas de accesos
│   │   ├── zone.py            # Gestión de zonas de acceso
│   │   └── payroll.py         # Turnos, nómina, horas trabajadas
│   ├── services/               # Lógica de negocio
│   │   ├── qr_service.py      # Generación de imágenes QR
│   │   ├── totp_service.py    # Servicio TOTP (30s rotation)
│   │   ├── email_service.py   # Envío de emails
│   │   ├── email_confirmation_service.py  # Tokens de confirmación
│   │   ├── export_service.py  # PDF/Excel export
│   │   ├── cache_service.py   # Redis wrapper
│   │   └── audit_service.py   # Auditoría de acciones admin
│   ├── utils/                  # Utilidades
│   │   ├── decorators.py      # @login_required, etc.
│   │   └── helpers.py         # Funciones auxiliares
│   ├── static/                 # CSS, JS, imágenes
│   │   └── qrcodes/           # Códigos QR generados (PNG)
│   └── templates/              # Templates Jinja2
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── admin_users.html
│       └── ... (otros templates)
│
├── scanner/                     # Módulo físico de escaneo
│   ├── physical.py            # Lógica principal (OpenCV + pyzbar)
│   ├── scanner_fisico.py      # Wrapper compatible (punto de entrada)
│   └── README.md              # Documentación del escáner
│
├── database/                    # Scripts SQL
│   ├── setup_database.sql     # Schema inicial (usuarios, accesos_log, etc.)
│   ├── schema_extensions.sql  # Extensiones (payroll, etc.)
│   ├── add_indexes.sql        # Índices para performance
│   └── fix_user_id_nullable.sql
│
├── config/                      # Configuración
│   └── settings.py            # Carga variables de entorno
│
├── deployment/                  # Despliegue
│   ├── nginx.conf             # Proxy reverso
│   ├── start.ps1              # Script de inicio (Windows)
│   └── stop.ps1               # Script de parada (Windows)
│
├── tests/                       # Suite de pruebas pytest
│   ├── conftest.py            # Fixtures compartidas
│   ├── test_auth.py           # Tests de autenticación
│   ├── test_models.py         # Tests de modelos
│   ├── test_routes.py         # Tests de endpoints
│   └── test_login.py          # Tests específicos de login
│
├── docs/                        # Documentación técnica
│   ├── QUICKSTART.md          # Guía de inicio rápido
│   ├── MANUAL_USUARIO.md      # Manual para operadores
│   └── README_OLD.md          # Documentación detallada
│
├── scripts/                     # Utilidades
│   ├── init_database.py       # Inicialización automática BD
│   └── restaurar_cuentas.py   # Restore de datos y credenciales test
│
├── .env.example               # Plantilla de variables de entorno
├── .env                       # Variables reales (git ignored)
├── .gitignore
├── Dockerfile                 # Imagen Docker
├── docker-compose.yml         # Orquestación (Flask + MySQL + Redis)
├── requirements.txt           # Dependencias Python
├── pytest.ini                 # Configuración de tests
├── CHANGELOG.md               # Historial de versiones
├── CONTRIBUTING.md            # Guía de contribución
└── README.md                  # Este archivo
```

---

## 🧱 Stack Tecnológico

| Componente | Tecnología | Versión | Rol |
|:---|:---|:---|:---|
| **Backend** | Flask | 3.1.0 | Framework web y lógica de negocio |
| **Base de Datos** | MySQL | 8.0+ | Almacenamiento persistente |
| **Caché** | Redis | 7.0+ | Performance y rate limiting |
| **Servidor** | Gunicorn | Latest | Servidor WSGI para producción |
| **Proxy Reverso** | Nginx | Latest | Balanceo y SSL/TLS |
| **Lenguaje** | Python | 3.11+ | Desarrollo |
| **Containerización** | Docker | Latest | Despliegue portátil |
| **Visión por Computadora** | OpenCV | 4.10.0 | Detección de QR |
| **Decodificación QR** | pyzbar | 0.1.9 | Lectura de QR física |
| **Seguridad** | Cryptography | 44.0.0 | Hashing Scrypt y cifrado |
| **Autenticación** | PyOTP | 2.9.0 | Generación TOTP |
| **Email** | Flask-Mail | 0.10.0 | Notificaciones por correo |
| **Testing** | pytest | 8.3.3 | Suite de pruebas |
| **Rate Limiting** | Flask-Limiter | 3.9.0 | Control de intentos fallidos |
| **Exportación** | openpyxl, python-docx, fpdf | Latest | Reportes PDF/Excel |
| **Logging** | structlog | 24.1.0 | Logs estructurados en JSON |

---

## 📋 Requisitos Previos

### Sistema Operativo
- **Linux** (Debian/Ubuntu recomendado) o **Windows** con WSL2
- **macOS** también soportado

### Software Requerido
- **Python 3.11 o superior**
- **MySQL 8.0+ o MariaDB 10.3+** (base de datos `qr_access_db`)
- **Git** para clonar el repositorio
- *(Opcional)* **Docker & Docker Compose** para despliegue containerizado
- *(Opcional)* **Redis 7.0+** para caché (funciona sin él en modo in-memory)

### Hardware (Escaneo Físico)
- **Cámara USB** (webcam estándar, 2MP mínimo)
- **Monitor** (para visualización de estado del escáner)
- Conexión de red hacia el panel web

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/anibalmonasterio85/Q1.git
cd Q1
```

### 2. Crear Entorno Virtual

#### En Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### En Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Si tienes problemas con `mysql-connector-python` en Windows, instálalo manualmente:
```bash
pip install mysql-connector-python --only-binary :all:
```

### 4. Configurar Variables de Entorno

Copia el archivo de plantilla y edítalo con tus valores:

```bash
cp .env.example .env
```

Edita `.env` con tu editor favorito:

```dotenv
# DATABASE
DB_HOST=localhost
DB_PORT=3306
DB_USER=qr_access
DB_PASSWORD=tu_contraseña_segura_aqui
DB_NAME=qr_access_db

# FLASK
FLASK_APP=web_panel/app.py
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=genera_una_clave_aleatoria_de_al_menos_32_caracteres

# EMAIL (Gmail con contraseña de aplicación)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=noreply@qraccess.pro

# REDIS (opcional)
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

**⚠️ Importante**: 
- Genera una `SECRET_KEY` fuerte: `python -c "import secrets; print(secrets.token_hex(32))"`
- Para Gmail, usa una contraseña de aplicación, NO tu contraseña de cuenta
- Cambia todas las contraseñas en producción

### 5. Crear Base de Datos

#### Opción A: Automático (recomendado)

```bash
python scripts/init_database.py
```

#### Opción B: Manual

Conecta a MySQL y ejecuta:

```bash
mysql -u root -p < database/setup_database.sql
mysql -u root -p < database/schema_extensions.sql
mysql -u root -p < database/add_indexes.sql
```

Verifica que la BD se creó:

```bash
mysql -u qr_access -p qr_access_db -e "SHOW TABLES;"
```

### 6. Inicializar Datos de Prueba (Opcional)

```bash
python scripts/restaurar_cuentas.py
```

Esto crea cuentas de prueba y usuarios administrativos.

---

## 🎮 Cómo Ejecutar el Proyecto

### Parte 1: Iniciar el Panel Web (Servidor Central)

```bash
python web_panel/app.py
```

Verás:
```
==================================================
  🔐 QR Access Control PRO
  🌐 Servidor: http://localhost:5001
  📊 Debug: False
  💾 Base de datos: localhost:3306/qr_access_db
  📁 Logs: logs/web_panel.log
==================================================
```

**Accede en el navegador**: `http://localhost:5001`

**Credenciales por defecto**:
- Correo: `admin@qraccess.com`
- Contraseña: `admin123`

⚠️ **Cambia la contraseña inmediatamente en producción**.

### Parte 2: Iniciar el Escáner Físico (Terminal en Puerta)

En otra terminal (con `venv` activado):

```bash
python scanner/scanner_fisico.py
```

Verás:
```
============================================================
  🔐 QR ACCESS CONTROL PRO - PHYSICAL SCANNER
============================================================
  📷 Cámara: 0
  💾 BD: localhost:3336/qr_access_db
  🔄 Cooldown: 3s
  ⌨️  Controles: 'q' = Salir | 's' = Captura
============================================================

[INFO] Cámara abierta. Esperando códigos QR...
```

**Controles**:
- **Q**: Salir del escáner
- **S**: Captura pantalla (guarda como PNG)

El escáner mostrará en tiempo real:
- ✅ ACCESO PERMITIDO (verde) - Usuario encontrado y activo
- ❌ ACCESO DENEGADO (rojo) - Usuario inactivo, QR expirado o no registrado
- 📋 Nombre del usuario y detalles del resultado

Todos los accesos se registran automáticamente en `accesos_log`.

### Parte 3: Ejecutar Tests (Opcional)

```bash
pytest tests/ -v
```

O con cobertura:

```bash
pytest tests/ --cov=web_panel --cov-report=html
```

Se genera reporte HTML en `htmlcov/index.html`.

---

## 🌐 Endpoints y Rutas Principales

### Autenticación

| Método | Ruta | Descripción | Auth Requerida |
|:---|:---|:---|:---|
| **GET/POST** | `/login` | Página de login con rate limit (10/min) | No |
| **GET/POST** | `/register` | Registro público de usuarios (5/min) | No |
| **GET** | `/logout` | Cierre de sesión | Sí |

### Dashboard

| Método | Ruta | Descripción | Auth Requerida |
|:---|:---|:---|:---|
| **GET** | `/dashboard` | Panel principal con estadísticas | Sí |
| **GET** | `/dashboard/perfil` | Perfil del usuario actual | Sí |
| **POST** | `/dashboard/perfil` | Actualizar perfil usuario | Sí |

### Administración

| Método | Ruta | Descripción | Auth Requerida |
|:---|:---|:---|:---|
| **GET** | `/admin/usuarios` | Listado de usuarios (tabla paginada) | Sí (Admin) |
| **GET/POST** | `/admin/usuarios/crear` | Crear nuevo usuario | Sí (Admin) |
| **GET/POST** | `/admin/usuarios/<id>/editar` | Editar usuario | Sí (Admin) |
| **POST** | `/admin/usuarios/<id>/eliminar` | Eliminar usuario | Sí (Admin) |
| **POST** | `/admin/usuarios/<id>/regenerar_qr` | Regenerar código QR | Sí (Admin) |
| **GET** | `/admin/zonas` | Listado de zonas | Sí (Admin) |
| **GET/POST** | `/admin/zonas/crear` | Crear zona de acceso | Sí (Admin) |
| **GET** | `/admin/reportes` | Exportar reportes (PDF/Excel) | Sí (Admin) |

### API (JSON para Frontend)

| Método | Ruta | Descripción | Auth Requerida |
|:---|:---|:---|:---|
| **GET** | `/api/stats` | Estadísticas dashboard (JSON) | Sí |
| **GET** | `/api/accesos` | Últimos 20 accesos (JSON) | Sí |
| **GET** | `/api/accesos/live` | Top 10 accesos tiempo real | Sí |
| **POST** | `/api/accesos/filter` | Filtrar accesos por fecha/resultado | Sí |
| **POST** | `/api/validate_qr` | Validar QR (para escáneres externos) | Opcional |

### Escáner

| Método | Ruta | Descripción | Auth Requerida |
|:---|:---|:---|:---|
| **GET** | `/scanner/status` | Estado del escáner físico | No |

---

## 💾 Estructura de la Base de Datos

### Tabla: `usuarios`
Almacena información de usuarios y sus credenciales.

| Columna | Tipo | Descripción |
|:---|:---|:---|
| **id** | INT PK | ID único del usuario |
| **nombre** | VARCHAR(100) | Nombre completo |
| **correo** | VARCHAR(150) UK | Email único |
| **password_hash** | VARCHAR(255) | Hash Scrypt de la contraseña |
| **rol** | ENUM('admin','usuario','visitante') | Rol de acceso |
| **activo** | BOOLEAN | Si está activo para acceso |
| **fecha_expiracion** | DATETIME NULL | Fecha de expiración de credencial |
| **qr_code** | VARCHAR(255) UK | Token TOTP base32 (secreto) |
| **foto** | VARCHAR(255) NULL | Ruta a foto de perfil |
| **departamento** | VARCHAR(100) NULL | Departamento del usuario |
| **telefono** | VARCHAR(20) NULL | Teléfono de contacto |
| **notas** | TEXT NULL | Notas administrativas |
| **created_at** | DATETIME | Timestamp de creación |
| **updated_at** | DATETIME | Timestamp última actualización |

**Índices**: `idx_correo`, `idx_qr_code`, `idx_rol`, `idx_activo`

### Tabla: `accesos_log`
Registro de cada intento de acceso (permitido/denegado).

| Columna | Tipo | Descripción |
|:---|:---|:---|
| **id** | INT PK | ID del log |
| **qr_texto** | VARCHAR(255) | Texto del QR escaneado |
| **resultado** | ENUM('permitido','denegado') | Resultado del acceso |
| **user_id** | INT FK NULL | Usuario asociado (NULL si desconocido) |
| **metodo** | VARCHAR(50) | Método: 'qr_scanner', 'api', etc. |
| **ip_address** | VARCHAR(45) NULL | IP del cliente |
| **scanner_id** | VARCHAR(50) | ID del escáner físico |
| **detalles** | TEXT NULL | Detalles adicionales (razón denegado) |
| **fecha_hora** | DATETIME | Timestamp del intento |

**Índices**: `idx_fecha_hora`, `idx_resultado`, `idx_user_id`

### Tabla: `configuracion`
Parámetros del sistema (clave-valor).

| Columna | Tipo | Descripción |
|:---|:---|:---|
| **id** | INT PK | ID |
| **clave** | VARCHAR(100) UK | Nombre de la configuración |
| **valor** | TEXT | Valor |
| **descripcion** | VARCHAR(255) NULL | Descripción |
| **updated_at** | DATETIME | Última actualización |

**Ejemplos**: `app_name`, `session_timeout`, `max_login_attempts`, `qr_expiration_days`, `timezone`

### Tablas adicionales (si activadas)
- **payroll**: Turnos, horas trabajadas, nómina
- **zones**: Zonas de acceso con RBAC
- **audit_logs**: Auditoría de acciones administrativas

---

## 🧪 Testing

### Ejecutar Todos los Tests

```bash
pytest tests/ -v
```

### Ejecutar Tests por Categoría

```bash
# Solo tests unitarios
pytest tests/ -m unit -v

# Solo tests de autenticación
pytest tests/ -m auth -v

# Tests que requieren BD
pytest tests/ -m requires_db -v
```

### Ver Cobertura

```bash
pytest tests/ --cov=web_panel --cov-report=term-missing --cov-report=html
open htmlcov/index.html
```

### Fixtures Disponibles (conftest.py)

- `client`: Cliente Flask para testing de rutas
- `app`: Instancia de aplicación Flask
- `db_connection`: Conexión a BD de prueba
- `admin_user`: Usuario admin para autenticación
- `test_user`: Usuario regular para testing

Cobertura mínima requerida: **80%** (ver `pytest.ini`)

---

## 📊 Estado Actual y Notas Conocidas

### ✅ Features Implementadas
- ✅ TOTP dinámico con rotación cada 30 segundos
- ✅ Hashing Scrypt para contraseñas
- ✅ Rate limiting en login y registro
- ✅ Escaneo QR físico con OpenCV + pyzbar
- ✅ Panel administrativo web completo
- ✅ API REST para integración externa
- ✅ Exportación PDF/Excel de reportes
- ✅ Logging estructurado con structlog
- ✅ Docker y docker-compose listos
- ✅ Tests automatizados con pytest
- ✅ Confirmación de email
- ✅ RBAC multi-zona

### 🔄 En Desarrollo
- 🔄 Módulo de nómina y turnos (refinamiento)
- 🔄 Biometría (face recognition)
- 🔄 App móvil (Flutter)
- 🔄 API v2 con Swagger completo

### ⚠️ Limitaciones Conocidas
- El escáner físico requiere **webcam USB conectada**
- Email requiere configuración SMTP válida (Gmail o similar)
- Redis es opcional pero recomendado para rate limiting distribuido
- No soporta aún multi-tenancy (en roadmap v3.0)

### 📝 TODOs Principales
- Implementar face recognition biométrica
- Agregar SMS como alternativa a email
- Dashboard de analytics avanzado
- Integración con sistemas de RR.HH. externos
- Migrar a SQLAlchemy ORM (actualmente raw SQL)

---

## 🐳 Despliegue con Docker

### Usando Docker Compose (Recomendado)

```bash
# Copiar y configurar .env
cp .env.example .env
# Editar .env con tus valores

# Construir imágenes
docker-compose build

# Levantar servicios (Flask + MySQL + Redis)
docker-compose up -d

# Ver logs
docker-compose logs -f web_panel

# Inicializar BD (primera vez)
docker-compose exec web_panel python scripts/init_database.py

# Detener
docker-compose down
```

### Dockerfile Personalizado

```bash
# Construir imagen
docker build -t qr-access-pro:latest .

# Ejecutar
docker run -d \
  --name qr-access \
  -p 5000:5000 \
  -e DB_HOST=host.docker.internal \
  -e DB_USER=qr_access \
  -e DB_PASSWORD=tu_password \
  -e SECRET_KEY=tu_secret_key \
  qr-access-pro:latest
```

Accede a `http://localhost:5000`

---

## 🔧 Configuración Avanzada

### Rate Limiting Personalizado

En `config/settings.py` o `.env`:

```dotenv
RATE_LIMIT_ENABLED=true
LOGIN_RATE_LIMIT=10/minute      # 10 intentos por minuto
API_RATE_LIMIT=30/minute        # 30 peticiones por minuto
GENERAL_RATE_LIMIT=100/minute   # Límite general
```

### Logging Estructurado

Los logs se guardan en `logs/web_panel.log` con rotación automática (5MB max, 5 backups).

Formato: `[YYYY-MM-DD HH:MM:SS] LEVEL in module: message`

```bash
# Ver logs en tiempo real
tail -f logs/web_panel.log

# Ver solo errores
grep ERROR logs/web_panel.log
```

### Variables de Entorno Principales

```dotenv
# APP
FLASK_ENV=production             # development | production
DEBUG=0                          # 0 = desactivado
SECRET_KEY=...                   # 32+ caracteres alfanuméricos

# DATABASE
DB_HOST=localhost
DB_PORT=3306
DB_NAME=qr_access_db
DB_POOL_SIZE=5                   # Conexiones simultáneas

# SECURITY
SESSION_TIMEOUT=28800            # 8 horas
SESSION_COOKIE_SECURE=true       # HTTPS obligatorio
SESSION_COOKIE_HTTPONLY=true

# CACHE/REDIS
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379

# QR CONFIG
TOTP_WINDOW=1                    # ±30 segundos tolerancia
QR_BOX_SIZE=10                   # Tamaño de celda QR
```

---

## 📚 Documentación Adicional

Dentro del repositorio encontrarás:

- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Pasos alternativos y troubleshooting
- **[docs/MANUAL_USUARIO.md](docs/MANUAL_USUARIO.md)** - Manual para operadores
- **[docs/README_OLD.md](docs/README_OLD.md)** - Especificaciones técnicas detalladas
- **[scanner/README.md](scanner/README.md)** - Guía del escáner físico
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Cómo contribuir al proyecto
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de versiones

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para saber cómo:

1. Hacer fork del repositorio
2. Crear una rama feature (`git checkout -b feature/mi-feature`)
3. Commitear cambios (`git commit -am 'feat: agregar mi feature'`)
4. Hacer push a la rama (`git push origin feature/mi-feature`)
5. Abrir un Pull Request

### Estándares de Código
- Código en **inglés**, commits en **inglés**
- Usar **pytest** para tests (mínimo 80% cobertura)
- Docstrings en funciones críticas
- Type hints recomendados (Python 3.11+)

---

## 📞 Soporte y Contacto

- **Issues**: Reporta bugs en [GitHub Issues](https://github.com/anibalmonasterio85/Q1/issues)
- **Discussions**: Preguntas en [GitHub Discussions](https://github.com/anibalmonasterio85/Q1/discussions)
- **Email**: Para soporte profesional, contacta al equipo

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE) - ver detalles en el archivo LICENSE.

---

## 👤 Autor

**Aníbal Monasterio**  
GitHub: [@anibalmonasterio85](https://github.com/anibalmonasterio85)

Hecho con ❤️ en 2026

---

## 🗺️ Roadmap

### v2.1 (Q2 2026)
- [ ] Face recognition biométrica
- [ ] Integración con Active Directory
- [ ] SMS notifications
- [ ] Mobile app (Flutter)

### v3.0 (Q3 2026)
- [ ] Multi-tenancy (SaaS)
- [ ] AI-powered anomaly detection
- [ ] Webhooks e integraciones
- [ ] GraphQL API

### v4.0 (Q4 2026)
- [ ] Global deployment ready
- [ ] Advanced enterprise features
- [ ] Marketplace de extensiones

---

**¡Gracias por usar QR Access PRO! 🚀**

*Seguridad moderna para acceso sin fricciones.*
