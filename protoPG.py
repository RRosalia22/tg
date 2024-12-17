import streamlit as st
import cv2
from PIL import Image
import tempfile
import os
import numpy as np
import gc

##variables globales
texto_info="Procesando video..."

# Función para procesar el video y generar la imagen de salida
def process_video(video_path):
    # Ejemplo: Captura el primer cuadro del video
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    video.release()
    if success:
        # Convertir el cuadro a una imagen
        output_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return output_image
    else:
        st.error("Error al procesar el video.")
        return None

#funcion
def recuperar_datos(video_path):


    # Abre el video

    cap = cv2.VideoCapture(video_path)

    # Lista para almacenar los frames
    frames = []

    # Proceso para capturar frames
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir frame a escala RGB (uint8, para ahorrar memoria)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(img)  # Almacena el frame
        
        frame_count += 1

        # Limpiar cada ciertos frames para evitar uso excesivo de memoria
        if frame_count % 100 == 0:
            gc.collect()  # Limpia objetos no usados
            print(f"{frame_count} frames procesados...")

    # Libera recursos
    cap.release()

    # Convierte la lista de frames a un array de NumPy
    frames_array = np.array(frames, dtype=np.uint8)  # Especifica dtype para optimización
    del frames  # Libera la lista original
    gc.collect()  # Asegúrate de liberar memoria

    #print("Forma de frames_array:", frames_array.shape)

    #print("Forma de frames_array:", frames_array.shape)  # Debería ser (altura, ancho, número de frames)
    #frame_gray = frames_array[900, 0:1000, 300:1100]
    #--------------------------------------------
    slice_colors = frames_array[1100:299:-1, #n-frames
                            880, # altura / corte
                            0:1000, # ancho 
                            :] # canales RGB
    #------------------------------TEXTOS
    img_text = np.array(slice_colors)

    # Definir el texto, la fuente, el tamaño, el color y el grosor
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'Flecha recta'
    org = (300, 120) ##(ancho,numero_frame)
    fontScale = 0.8
    color = (255, 255, 255)
    thickness = 2

    # Agregar el texto a la imagen
    cv2.putText(img_text, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(img_text, text, (600, 120), font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(img_text, "Flecha cruce derecha", (600, 210), font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(img_text, "Flecha cruce derecha", (600, 310), font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(img_text, text, (300, 210), font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(img_text, text, (300, 300), font, fontScale, color, thickness, cv2.LINE_AA)
    #------------------------------VERTICALES------------------------
    cv2.putText(img_text, "S-ID",(890, 1100-900), font, fontScale, (0, 0, 255),thickness, cv2.LINE_AA)
    cv2.putText(img_text, "SP-20",(890, 1100-684-50), font, fontScale, (255, 255, 0),thickness, cv2.LINE_AA)

    #-----
    gc.collect()
    output_image = img_text    

    #-------------------------------------------
    return output_image

# Configuración de la interfaz
st.title("Prototipo funcional de la técnica de rebanado de video")
st.write("Sube un video para procesarlo y generar una imagen de salida.")

#Subir archivo de video
uploaded_video = st.file_uploader("Sube tu video aquí", type=["mp4", "avi", "mov", "mkv"])

if uploaded_video is not None:
    # Guardar el video en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_video.read())
        temp_video_path = temp_video.name
        #os.remove(temp_video.name)


    # Procesar el video
    status_placeholder = st.empty() 
    status_placeholder.info("Procesando el video...")
    output_image = recuperar_datos(temp_video_path)


    # Mostrar la imagen generada
    if output_image is not None:
        status_placeholder.success("Proceso finalizado!")
        st.image(output_image, caption="Imagen generada a partir del video.", use_container_width=True)
        

    # Eliminar el archivo temporal
    os.remove(temp_video_path)
