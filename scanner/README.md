# Scanner Físico

Este módulo contiene el escáner físico que utiliza la cámara para leer códigos QR.

## Archivos

* `physical.py` — Lógica principal de captura, decodificación y validación de QR.
* `scanner_fisico.py` — Entrada del script, mantiene compatibilidad con el comando histórico.

## Uso

Ejecuta el escáner desde la raíz del proyecto:

```bash
python scanner/scanner_fisico.py
```

## Comportamiento

* Detecta múltiples códigos QR en un mismo frame.
* Usa `pyzbar` si está instalado y cae en respaldo a OpenCV si no está disponible.
* Dibuja bordes y mensajes de estado en la ventana de la cámara.
* Registra accesos permitidos y denegados en la base de datos.
