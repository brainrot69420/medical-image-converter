#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
#
# dicom_to_jpg.py
# 
# Script que convierte un archivo DICOM (DCM) a JPG.
#
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import argparse
import os

import numpy as np
import pydicom
from PIL import Image

def dicom_to_jpg(input_path: str, output_path: str, window_center=None, window_width=None):
    """
    Convierte un archivo DICOM a JPG.

    :param input_path: Ruta al archivo .dcm
    :param output_path: Ruta donde se guardará el .jpg
    :param window_center: (opcional) nivel de ventana para contraste
    :param window_width: (opcional) ancho de ventana para contraste
    """
    # Leer DICOM
    ds = pydicom.dcmread(input_path)
    pixel_array = ds.pixel_array.astype(np.float32)

    # Aplicar windowing si se proveen parámetros
    if window_center is not None and window_width is not None:
        # Fórmula de windowing lineal
        wc, ww = float(window_center), float(window_width)
        min_val = wc - ww/2
        max_val = wc + ww/2
        pixel_array = np.clip(pixel_array, min_val, max_val)
    else:
        # Si no, escalamos automáticamente al rango de datos
        min_val = np.min(pixel_array)
        max_val = np.max(pixel_array)

    # Normalizar a 0–255
    pixel_array = (pixel_array - min_val) / (max_val - min_val) * 255.0
    pixel_array = pixel_array.astype(np.uint8)

    # Convertir a imagen PIL
    img = Image.fromarray(pixel_array)
    # Para imágenes en escala de grises garantizar el modo 'L'
    if img.mode != 'L':
        img = img.convert('L')

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Guardar JPG
    img.save(output_path, format='JPEG', quality=95)
    print(f"[✔] Guardado: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Convierte un archivo DICOM (.dcm) a imagen JPG."
    )
    parser.add_argument("input", help="Ruta al archivo DICOM de entrada")
    parser.add_argument("output", help="Ruta de salida para el JPG (ej: salida.jpg)")
    parser.add_argument("--center", "-c", help="Window Center (nivel de ventana)", type=float)
    parser.add_argument("--width", "-w", help="Window Width (ancho de ventana)", type=float)
    args = parser.parse_args()

    dicom_to_jpg(
        input_path=args.input,
        output_path=args.output,
        window_center=args.center,
        window_width=args.width
    )

if __name__ == "__main__":
    main()