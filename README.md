# QR Access PRO 🔐

Sistema profesional de control de acceso mediante códigos QR dinámicos, diseñado para entornos empresariales. Reemplaza las tarjetas magnéticas tradicionales con tecnología de autenticación moderna y registros en tiempo real.

---

## 🌟 Características Principales

*   **Identificación Sin Contacto**: Generación y lectura de QRs dinámicos con renovación cada 30 segundos (TOTP).
*   **Seguridad Enterprise**: Hashing Scrypt para contraseñas, comunicación SSL/TLS y protección contra fuerza bruta.
*   **Control Laboral**: Cálculo automático de turnos, reporte de horas trabajadas y detección de atrasos.
*   **Gestión Centralizada**: Panel administrativo para crear, editar y suspender credenciales instantáneamente.
*   **Arquitectura Robusta**: Preparado para escalar con Redis, Nginx y Docker.

---

## 🧱 Estructura del Proyecto

* `web_panel/` — Panel central con Flask, rutas, modelos y servicios.
  * `web_panel/app.py` — Punto de entrada del servidor web.
  * `web_panel/routes/` — Blueprints de `auth`, `dashboard`, `admin`, `api`, `scanner`.
  * `web_panel/models/` — Acceso a datos para usuarios, logs y zonas.
  * `web_panel/services/` — Lógica de QR, email, TOTP y exportación.
  * `web_panel/static/`, `web_panel/templates/` — UI y assets para el panel.
* `scanner/` — Módulo físico de escaneo QR.
  * `scanner/physical.py` — Lógica de cámara, detección y validación QR.
  * `scanner/scanner_fisico.py` — Wrapper compatible con el comando histórico.
  * `scanner/README.md` — Documentación del escáner físico.
* `database/` — Scripts SQL para esquema, índices y migraciones.
* `deployment/` — Archivos de despliegue y configuración de infraestructura.
  * `deployment/nginx.conf` — Configuración de proxy reverso.
  * `deployment/start.ps1` — Script de inicio en Windows.
  * `deployment/stop.ps1` — Script de detención en Windows.
* `config/` — Configuración de entorno, base de datos y logging.
* `docs/` — Documentación técnica y manual de usuario.
* `scripts/` — Utilidades de instalación y mantenimiento.
  * `scripts/restaurar_cuentas.py` — Restaurar cuentas y generar credenciales de prueba.
  * `scripts/init_database.py` — Inicialización de la base de datos.
* `tests/` — Todos los tests del proyecto.
  * `tests/test_auth.py` — Pruebas de autenticación.
  * `tests/test_login.py` — Pruebas de login.

---

## 🛠 Instalación y Configuración

### 1. Requisitos Previos
*   **Python 3.11+**
*   **MySQL / MariaDB** configurado con base de datos `qr_access_db`.
*   *(Opcional)* **Docker & Compose** para despliegue rápido.

### 2. Configurar Entorno
1.  **Clonar el repositorio**:
    ```bash
    git clone <repo_url>
    cd QR_Access_PROPC
    ```

2.  **Crear entorno virtual**:
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables (.env)**:
    Copia el archivo `.env.example` a `.env` y ajusta las credenciales de tu base de datos y llaves de seguridad.

---

## 🚀 Uso del Sistema

La arquitectura consta de dos partes independientes que se comunican entre sí para una validación segura.

### Parte 1: Iniciar el Panel Web (Servidor Central)
El panel web es el cerebro del sistema que controla la base de datos y los registros.

*   **Ejecutar en desarrollo**:
    ```bash
    python web_panel/app.py
    ```
    Accede a: `http://localhost:5000`

### Parte 2: Iniciar el Escáner (Terminal en Puerta)
El escáner es el programa que activa la cámara y espera que una credencial sea presentada.

*   **Ejecutar escáner**:
    ```bash
    python scanner/scanner_fisico.py
    ```

*   **Nota**: el módulo de escáner ahora está organizado en `scanner/physical.py` y mantiene el wrapper histórico `scanner/scanner_fisico.py`.

---

## 📋 Arquitectura y Seguridad

Este proyecto utiliza un stack moderno para garantizar redundancia y velocidad.

| Componente | Tecnología | Rol |
| :--- | :--- | :--- |
| **Backend** | Python / Flask 3.1 | Lógica y API |
| **Base de Datos** | MySQL 8.0+ | Almacenamiento persistente |
| **Caché** | Redis 7.0 | Performance y Rate limiting |
| **Proxy/Servidor** | Nginx / Gunicorn | Despliegue en producción |
| **Seguridad** | TOTP / Scrypt | Cifrado y validación |

---

## 📚 Documentación Adicional

He conservado la documentación técnica detallada (esquemas de DB, despliegue AWS, auditoría) en los siguientes archivos:

*   📖 **[Guía Técnica Detallada](docs/README_OLD.md)** - Esquemas completos de tablas y performance.
*   📘 **[Manual de Usuario](docs/MANUAL_USUARIO.md)** - Para operadores del sistema.
*   📙 **[Guía de Inicio Rápido](docs/QUICKSTART.md)** - Pasos alternativos de despliegue.

---

*"Seguridad moderna para acceso sin fricciones"*
**Hecho con ❤️ en 2026**