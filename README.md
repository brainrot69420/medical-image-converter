# medical-imaging-converter
Converts a DICOM file or directory of files to JPG, PNG, or TIFF files

*Script name:* dicom_converter.py

Script that converts DICOM files (.dcm) to images (JPG, PNG, TIFF) from the command line.

## Includes:
- Batch processing of a directory or individual file
- Choice of output format from among three available formats
- Insertion of the image acquisition date into the output file name
- Logging of conversion and error logs in conversion.log

## 100% Python code. Requires the following libraries:

- [Pydicom](https://pydicom.github.io/) - to open DICOM/DCM files
- [Pillow](https://pillow.readthedocs.io/en/stable/) - to create and save JPG, PNG, or TIFF images
- [NumPy](https://numpy.org/) - to manipulate pixel arrays

## Execution

It's recommended to create and activate a virtual environment (optional but highly recommended):
~~~
python3 -m venv venv
source venv/bin/activate
~~~
Installation of dependencies:
~~~
pip install pydicom pillow numpy
~~~
Usage:
~~~
dicom_converter.py [-h] [-f {jpg,png,tiff}] [-c CENTER] [-w WIDTH] input_path output_path
~~~
positional arguments:
  input_path                                        .dcm file or directory with .dcm files
  output_path                                       Output file or destination directory

options:
  -h, --help                                        Show this help message and exit
  -f {jpg,png,tiff}, --format {jpg,png,tiff}        Output format (default: jpg)
  -c CENTER, --center CENTER                        Window Center for image contrast
  -w WIDTH, --width WIDTH                           Window Width for image contrast


### A single DCM file with PNG output
~~~
(venv) alejandro@dockerlab:~$ python3 dicom_converter.py -f png /home/alejandro/series-000001/image-000002.dcm /home/alejandro/salida/
[✔] Guardado: /home/alejandro/salida/image-000002_20061012.png
~~~
### A directory of DCM files, with the default output being JPG
~~~
(venv) alejandro@dockerlab:~$ python3 dicom_converter.py -f jpg /home/alejandro/series-000001/ /home/alejandro/salida/
[✔] Guardado: /home/alejandro/salida/image-000355_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000311_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000361_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000218_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000317_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000302_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000282_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000091_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000039_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000026_20061012.jpg
[✔] Guardado: /home/alejandro/salida/image-000314_20061012.jpg
~~~
### A directory of DCM files. Using windowing to enhance the contrast of medical images (parameters depend on the type of study and the body part in the image).
~~~
(venv) alejandro@dockerlab:~$ python3 dicom_converter.py -f png --center 40 --width 400 /home/alejandro/series-000001/ /home/alejandro/salida-high-contrast/
[✔] Guardado: /home/alejandro/salida/image-000355_20061012.png
[✔] Guardado: /home/alejandro/salida/image-000311_20061012.png
[✔] Guardado: /home/alejandro/salida/image-000361_20061012.png
~~~




