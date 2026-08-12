"""QR Access Control PRO - Physical Scanner Module

Este archivo contiene la lógica del escáner físico:
- captura de cámara
- detección y decodificación de QR
- validación contra la base de datos
- visualización de resultados
"""
import os
import sys
import time
import logging
from datetime import datetime

import cv2
import numpy as np

# Add project root to path when executed from scanner/ directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config.settings import config
from web_panel.models import user as user_model, access_log

logger = logging.getLogger(__name__)

CAMERA_INDEX = int(os.getenv('SCANNER_CAMERA_INDEX', '0'))
SCAN_COOLDOWN = int(os.getenv('SCANNER_COOLDOWN', '3'))
FRAME_WIDTH = int(os.getenv('SCANNER_FRAME_WIDTH', '640'))
FRAME_HEIGHT = int(os.getenv('SCANNER_FRAME_HEIGHT', '480'))
WINDOW_NAME = 'QR Access Control PRO - Scanner'

COLOR_SUCCESS = (128, 222, 74)
COLOR_DENIED = (113, 113, 248)
COLOR_INFO = (250, 165, 96)
COLOR_WHITE = (255, 255, 255)
COLOR_BG = (26, 26, 42)

PYZBAR_AVAILABLE = True
try:
    from pyzbar import pyzbar
except Exception as err:
    PYZBAR_AVAILABLE = False
    pyzbar = None
    logger.warning(f"pyzbar no disponible: {err}")
    logger.warning("Se usará OpenCV QRCodeDetector como respaldo para decodificar QR.")


class QRResult:
    """Resultado unificado de decodificación QR."""

    def __init__(self, data, polygon=None):
        self.data = data
        self.polygon = []
        self._build_polygon(polygon)

    def _build_polygon(self, polygon):
        if polygon is None:
            return
        pts = np.asarray(polygon, dtype=np.int32)

        if pts.ndim == 3 and pts.shape[1] == 1:
            pts = pts[:, 0, :]

        if pts.ndim == 2 and pts.shape[1] == 2:
            for x, y in pts:
                point = type('Point', (), {'x': int(x), 'y': int(y)})
                self.polygon.append(point)


def draw_overlay(frame, title, status, color, user_name=None, detail=None):
    """Dibuja la interfaz sobre la imagen de la cámara."""
    h, w = frame.shape[:2]
    overlay = frame.copy()

    cv2.rectangle(overlay, (0, h - 120), (w, h), COLOR_BG, -1)
    frame = cv2.addWeighted(overlay, 0.88, frame, 0.12, 0)

    cv2.putText(frame, title, (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, COLOR_INFO, 2)
    cv2.putText(frame, status, (20, h - 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

    if user_name:
        cv2.putText(frame, f"Usuario: {user_name}", (20, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 1)

    if detail:
        cv2.putText(frame, detail, (w - 520, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_INFO, 1)

    cv2.rectangle(frame, (0, 0), (w, 42), COLOR_BG, -1)
    cv2.putText(frame, "QR Access Control PRO", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, COLOR_INFO, 2)

    return frame


def decode_with_pyzbar(frame):
    """Decodifica QR usando pyzbar."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded = pyzbar.decode(gray)
    results = []
    for item in decoded:
        data = item.data.decode('utf-8', errors='ignore') if isinstance(item.data, (bytes, bytearray)) else str(item.data)
        results.append(QRResult(data, item.polygon))
    return results


def decode_with_opencv(frame):
    """Decodifica QR usando OpenCV como respaldo."""
    detector = cv2.QRCodeDetector()
    # detectAndDecodeMulti has different return signatures across OpenCV versions.
    decoded_info = []
    points = None
    try:
        res = detector.detectAndDecodeMulti(frame)
        if res:
            # res may be (decoded_info, points, straight_qrcode) or
            # (retval, decoded_info, points, straight_qrcode)
            if isinstance(res, (list, tuple)):
                if len(res) == 3:
                    decoded_info, points = res[0], res[1]
                elif len(res) >= 4:
                    # retval present
                    decoded_info, points = res[1], res[2]
                else:
                    # fallback: try to infer
                    for elem in res:
                        if isinstance(elem, (list, tuple)) and all(isinstance(x, str) for x in elem):
                            decoded_info = list(elem)
                        elif hasattr(elem, 'shape') or (isinstance(elem, (list, tuple)) and elem and isinstance(elem[0], (list, tuple, np.ndarray))):
                            points = elem
    except Exception:
        decoded_info = []
        points = None

    # Fallback to single-detection API if nothing found
    if not decoded_info:
        try:
            single = detector.detectAndDecode(frame)
            if single:
                # detectAndDecode may return (data, points, straight_qrcode)
                data = single[0] if len(single) > 0 else None
                pts = single[1] if len(single) > 1 else None
                decoded_info = [data] if data else []
                points = [pts] if pts is not None else None
        except Exception:
            decoded_info = []
            points = None

    results = []
    if isinstance(decoded_info, (list, tuple)) and points is not None:
        for data, polygon in zip(decoded_info, points):
            if data:
                results.append(QRResult(data, polygon))
    elif decoded_info:
        # Single decoded string
        results.append(QRResult(decoded_info if isinstance(decoded_info, str) else decoded_info[0], points))

    return results


def decode_qr_codes(frame):
    """Devuelve todos los códigos QR detectados en un frame."""
    if PYZBAR_AVAILABLE:
        results = decode_with_pyzbar(frame)
        if results:
            return results

    # Fallback to OpenCV detector; ensure we always return a list
    results = decode_with_opencv(frame)
    return results or []


def validate_qr(qr_data):
    """Valida un código QR contra la base de datos y registra el intento."""
    qr_text = str(qr_data).strip()
    if not qr_text:
        access_log.create_log(qr_text, 'denegado')
        return 'error', 'Desconocido', 'QR inválido'

    user = user_model.get_by_qr(qr_text)
    if user:
        if not user.get('activo'):
            access_log.create_log(qr_text, 'denegado', user['id'])
            return 'denegado', user.get('nombre', 'Desconocido'), 'Usuario inactivo'

        expiration = user.get('fecha_expiracion')
        if expiration and expiration < datetime.now():
            access_log.create_log(qr_text, 'denegado', user['id'])
            return 'denegado', user.get('nombre', 'Desconocido'), 'QR expirado'

        access_log.create_log(qr_text, 'permitido', user['id'])
        return 'permitido', user.get('nombre', 'Desconocido'), 'Acceso permitido'

    access_log.create_log(qr_text, 'denegado')
    return 'denegado', 'Desconocido', 'No registrado'


def _try_open_with_backend(index, backend):
    try:
        cap = cv2.VideoCapture(index, backend)
        if cap is not None and cap.isOpened():
            return cap
    except Exception:
        pass
    return None


def list_cameras(max_index=6, timeout=0.5):
    """Detecta cámaras disponibles probando índices 0..max_index-1.

    Nota: es una detección heurística (abre brevemente cada índice).
    """
    available = []
    for i in range(max_index):
        try:
            cap = cv2.VideoCapture(i)
            time.sleep(timeout)
            if cap is not None and cap.isOpened():
                available.append(i)
                cap.release()
        except Exception:
            pass
    return available


def open_camera(camera_index):
    """Inicializa y valida la cámara probando backends si es necesario.

    Retorna un objeto `cv2.VideoCapture` abierto o `None`.
    """
    # Try platform-specific backends first (Windows often benefits from DSHOW/MSMF)
    backends = []
    if hasattr(cv2, 'CAP_DSHOW'):
        backends.append(cv2.CAP_DSHOW)
    if hasattr(cv2, 'CAP_MSMF'):
        backends.append(cv2.CAP_MSMF)
    # Default backend (0) as last resort
    backends.append(0)

    for backend in backends:
        cap = _try_open_with_backend(camera_index, backend)
        if cap:
            # Try to set properties, ignore failures
            try:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
                # Try enabling autofocus if supported
                if hasattr(cv2, 'CAP_PROP_AUTOFOCUS'):
                    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            except Exception:
                pass
            return cap

    # If none of the backends worked, return None
    return None


def main(camera_index=None, width=None, height=None, fps=None, headless=False, cooldown=None):
    """Loop principal del escáner físico.

    Parámetros opcionales permiten configurar resolución, cooldown y modo headless.
    """
    # Allow updating module-level defaults during this run
    global FRAME_WIDTH, FRAME_HEIGHT, SCAN_COOLDOWN

    selected_camera = CAMERA_INDEX if camera_index is None else camera_index
    frame_w = FRAME_WIDTH if width is None else int(width)
    frame_h = FRAME_HEIGHT if height is None else int(height)
    scan_cooldown = SCAN_COOLDOWN if cooldown is None else int(cooldown)

    print("\n" + "=" * 60)
    print("  🔐 QR ACCESS CONTROL PRO - PHYSICAL SCANNER")
    print("=" * 60)
    print(f"  📷 Cámara: {selected_camera}")
    print(f"  💾 BD: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
    print(f"  🔄 Cooldown: {scan_cooldown}s")
    print("  ⌨️  Controles: 'q' = Salir | 's' = Captura")
    print("=" * 60 + "\n")

    # Update global frame size for this session
    FRAME_WIDTH = frame_w
    FRAME_HEIGHT = frame_h
    SCAN_COOLDOWN = scan_cooldown

    cap = open_camera(selected_camera)
    if cap is None:
        print(f"[ERROR] No se pudo abrir la cámara {selected_camera}")
        print("  Prueba con otro índice: python scanner/scanner_fisico.py [0|1|2] o usa --list para enumerar cámaras")
        return

    print("[INFO] Cámara abierta. Esperando códigos QR...\n")

    last_scanned = {}
    last_status = ('Esperando QR...', COLOR_INFO, '', '')
    last_action_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] No se pudo leer frame de la cámara")
                break

            decoded_qrs = decode_qr_codes(frame)
            processed_data = set()

            for qr in decoded_qrs:
                qr_text = qr.data.strip() if isinstance(qr.data, str) else str(qr.data).strip()
                if not qr_text or qr_text in processed_data:
                    continue

                processed_data.add(qr_text)
                now = time.time()
                last_seen = last_scanned.get(qr_text, 0)
                if now - last_seen < SCAN_COOLDOWN:
                    continue

                last_scanned[qr_text] = now
                result, user_name, detail = validate_qr(qr_text)
                timestamp = datetime.now().strftime('%H:%M:%S')

                if result == 'permitido':
                    status_text = 'ACCESO PERMITIDO'
                    status_color = COLOR_SUCCESS
                    print(f"  ✅ [{timestamp}] PERMITIDO - {user_name}")
                else:
                    status_text = 'ACCESO DENEGADO'
                    status_color = COLOR_DENIED
                    print(f"  ❌ [{timestamp}] DENEGADO - {user_name} ({detail})")

                last_status = (status_text, status_color, user_name, detail)
                last_action_time = now

                if qr.polygon:
                    try:
                        pts = np.array([[p.x, p.y] for p in qr.polygon], np.int32)
                        cv2.polylines(frame, [pts], True, COLOR_INFO, 2)
                    except Exception:
                        pass

            if time.time() - last_action_time > SCAN_COOLDOWN:
                last_status = ('Esperando QR...', COLOR_INFO, '', '')

            status_text, status_color, user_name, detail = last_status
            detail_text = detail if detail else 'Acérca tu QR al lector.'
            display_frame = draw_overlay(frame, 'Escaneando...', status_text, status_color, user_name, detail_text)

            if not headless:
                cv2.imshow(WINDOW_NAME, display_frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print('\n[INFO] Scanner detenido por el usuario.')
                    break
                elif key == ord('s'):
                    filename = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    cv2.imwrite(filename, display_frame)
                    print(f"  📸 Captura guardada: {filename}")
            else:
                # Headless: small sleep to avoid busy-looping; rely on KeyboardInterrupt to exit
                time.sleep(0.01)

    except KeyboardInterrupt:
        print('\n[INFO] Scanner detenido (Ctrl+C).')
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print('[INFO] Recursos liberados. Hasta luego!')
