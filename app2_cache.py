import streamlit as st
import cv2
from PIL import Image
import tempfile
import os
import numpy as np  # Asegúrate de importar numpy

##variables globales
texto_info = "Procesando video..."

# Función para procesar el video y generar la imagen de salida
@st.cache_data
def recuperar_datos(video_path):
    # Abre el video
    cap = cv2.VideoCapture(video_path)

    # Lista para almacenar los frames
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convierte el frame a escala de grises
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Añade el frame a la lista
        frames.append(img_gray)

    # Libera el video
    cap.release()

    # Convierte la lista de frames a un array de NumPy y reorganiza las dimensiones
    frames_array = np.stack(frames, axis=-1)

    # Selecciona un slice específico
    frame_gray = frames_array[900, 0:1000, 300:1100]
    output_image = frame_gray    

    return output_image

# Configuración de la interfaz
st.title("Prototipo funcional de la técnica de rebanado de video")
st.write("Sube un video para procesarlo y generar una imagen de salida.")

# Subir archivo de video
uploaded_video = st.file_uploader("Sube tu video aquí", type=["mp4", "avi", "mov", "mkv"])

if uploaded_video is not None:
    # Guardar el video en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_video.read())
        temp_video_path = temp_video.name

    # Procesar el video
    status_placeholder = st.empty()
    status_placeholder.info("Procesando el video...")
    output_image = recuperar_datos(temp_video_path)

    # Mostrar la imagen generada
    if output_image is not None:
        status_placeholder.success("Proceso finalizado!")
        st.title("Resultado")
        st.image(output_image, caption="Imagen generada a partir del video.", use_container_width=True)

    # Eliminar el archivo temporal
    os.remove(temp_video_path)
