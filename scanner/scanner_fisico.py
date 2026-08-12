"""Wrapper CLI para el escáner físico.

Mejoras:
- Opciones CLI: --camera, --list, --headless, --width, --height, --cooldown
- Mantiene compatibilidad con la llamada histórica `python scanner/scanner_fisico.py [camera_index]`
"""

import argparse
from scanner.physical import main, list_cameras


def build_parser():
    p = argparse.ArgumentParser(prog='scanner_fisico', description='QR Access PRO - Scanner wrapper')
    p.add_argument('camera_index', nargs='?', type=int, help='Índice de la cámara (legacy pos arg)')
    p.add_argument('--camera', '-c', type=int, help='Índice de la cámara a usar')
    p.add_argument('--list', '-l', action='store_true', help='Listar cámaras disponibles y salir')
    p.add_argument('--headless', action='store_true', help='Ejecutar sin ventana (solo validación)')
    p.add_argument('--width', type=int, help='Ancho del frame')
    p.add_argument('--height', type=int, help='Alto del frame')
    p.add_argument('--cooldown', type=int, help='Cooldown entre lecturas (seg)')
    return p


def cli_main():
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        cams = list_cameras()
        if cams:
            print('Cámaras detectadas:', ', '.join(map(str, cams)))
        else:
            print('No se detectaron cámaras')
        return

    camera_index = args.camera if args.camera is not None else args.camera_index

    kwargs = {}
    if args.width:
        kwargs['width'] = args.width
    if args.height:
        kwargs['height'] = args.height
    if args.cooldown:
        kwargs['cooldown'] = args.cooldown
    kwargs['headless'] = args.headless

    main(camera_index, **kwargs)


if __name__ == '__main__':
    cli_main()
