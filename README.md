# mouse_virtual

Este proyecto permite controlar el mouse de tu computadora usando gestos de la mano capturados por una cámara web, utilizando OpenCV, MediaPipe y Autopy.

## Características

- Control del puntero del mouse con el dedo índice.
- Clic izquierdo simulando el gesto de juntar el índice y el medio.
- Detección de mano en tiempo real usando MediaPipe.
- Interfaz visual con OpenCV.

## Requisitos

- Python 3.8 o superior (Preferiblemete Python 3.10, versiones posteriores crea conflicto entre las librerías)
- Webcam
- Windows (probado en este sistema)

## Instalación

1. Instala las dependencias:
    ```bash
    pip install opencv-python mediapipe numpy autopy
    ```

## Uso

1. Ejecuta el script principal:
    ```bash
    python virtualmouse.py
    ```

2. Apunta tu mano a la cámara:
    - Mueve el dedo índice para controlar el mouse.
    - Junta el dedo índice y el medio para hacer clic izquierdo.

3. Pulsa `ESC` para salir.

## Archivos principales

- `virtualmouse.py`: Script principal para el control del mouse.
- `followhands.py`: Módulo para la detección y seguimiento de la mano.

**Autor:** [Nicolás Arévalo Fajardo]  
**Fecha:** 26/05/2025

