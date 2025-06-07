#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dicom_converter.py
version: 1.2.0
author: Alejandro Ferrari
contact: aleferrari.uy@gmail.com 

Script que convierte archivos DICOM (.dcm) a imágenes (JPG, PNG, TIFF) desde línea de comandos.
Incluye:
 - Procesamiento por lotes de un directorio
 - Elección de formato de salida
 - Inserción de fecha de adquisición en el nombre de archivo
 - Registro de logs de conversiones y errores
"""
import argparse
import glob
import logging
import os
import sys

import numpy as np
import pydicom
from PIL import Image

# Configuración de logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, 'conversion.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Mapeo de formatos para PIL
FORMAT_MAP = {
    'jpg': 'JPEG',
    'png': 'PNG',
    'tiff': 'TIFF'
}


def convert_dicom(
    input_path: str,
    output_path: str,
    fmt: str = 'jpg',
    window_center=None,
    window_width=None
):
    """
    Convierte un archivo DICOM a una imagen en el formato especificado.
    """
    try:
        ds = pydicom.dcmread(input_path)
        # Obtener array de píxeles
        arr = ds.pixel_array.astype(np.float32)

        # Windowing opcional
        if window_center is not None and window_width is not None:
            wc, ww = float(window_center), float(window_width)
            min_val = wc - ww/2
            max_val = wc + ww/2
            arr = np.clip(arr, min_val, max_val)
        else:
            min_val, max_val = arr.min(), arr.max()

        # Normalizar a 0-255
        arr = ((arr - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)
        img = Image.fromarray(arr)
        if img.mode != 'L':
            img = img.convert('L')

        # Crear carpeta destino si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Determinar formato PIL correcto
        pil_fmt = FORMAT_MAP.get(fmt.lower(), fmt.upper())

        # Guardar imagen
        img.save(output_path, format=pil_fmt)
        msg = f"Guardado: {output_path}"
        print(f"[✔] {msg}")
        logger.info(f"SUCCESS: {input_path} -> {output_path}")

    except Exception as e:
        err = f"ERROR procesando {input_path}: {e}"
        print(f"[✖] {err}")
        logger.error(err, exc_info=True)


def main():
    parser = argparse.ArgumentParser(
        description='Convierte DICOM a JPG/PNG/TIFF, soporta lotes y metadatos.'
    )
    parser.add_argument(
        'input',
        help='Archivo .dcm o directorio con archivos .dcm'
    )
    parser.add_argument(
        'output',
        help='Archivo de salida o directorio destino'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['jpg', 'png', 'tiff'],
        default='jpg',
        help='Formato de salida (por defecto: jpg)'
    )
    parser.add_argument(
        '-c', '--center',
        type=float,
        help='Window Center para contraste'
    )
    parser.add_argument(
        '-w', '--width',
        type=float,
        help='Window Width para contraste'
    )
    args = parser.parse_args()

    inp = args.input
    out = args.output
    fmt = args.format

    # Si es directorio, procesar todos los .dcm
    if os.path.isdir(inp):
        if not os.path.exists(out):
            os.makedirs(out)
        files = glob.glob(os.path.join(inp, '*.dcm')) + glob.glob(os.path.join(inp, '*.DCM'))
        if not files:
            print(f"No se encontraron archivos DICOM en {inp}")
            sys.exit(1)
        for f in files:
            base = os.path.splitext(os.path.basename(f))[0]
            try:
                ds_tmp = pydicom.dcmread(f, stop_before_pixels=True)
                date = ds_tmp.get('AcquisitionDate') or ds_tmp.get('AcquisitionDateTime', '')[:8]
            except Exception:
                date = ''
            suffix = f"_{date}" if date else ''
            out_name = f"{base}{suffix}.{fmt}"
            out_path = os.path.join(out, out_name)
            convert_dicom(f, out_path, fmt, args.center, args.width)
    else:
        base = os.path.splitext(os.path.basename(inp))[0]
        try:
            ds_tmp = pydicom.dcmread(inp, stop_before_pixels=True)
            date = ds_tmp.get('AcquisitionDate') or ds_tmp.get('AcquisitionDateTime', '')[:8]
        except Exception:
            date = ''
        suffix = f"_{date}" if date else ''
        if os.path.isdir(out):
            out_path = os.path.join(out, f"{base}{suffix}.{fmt}")
        else:
            out_path = out
        convert_dicom(inp, out_path, fmt, args.center, args.width)


if __name__ == '__main__':
    main()
