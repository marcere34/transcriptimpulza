import streamlit as st
import yt_dlp
import whisper
import os
import time

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #ffffff !important; text-transform: uppercase; }
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    .stButton>button { background-color: #ffc107 !important; color: #000000 !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Descargando y procesando..."):
            try:
                # 1. Definir ruta absoluta
                output_path = os.path.join(os.getcwd(), "audio_final.mp3")
                
                # 2. Configuración de descarga
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                    'outtmpl': 'audio_final', # Esto creará audio_final.mp3
                    'quiet': True
                }
                
                # 3. Descarga
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # 4. ESPERA ACTIVA: Verificar que el archivo existe realmente antes de avanzar
                max_retries = 10
                while not os.path.exists(output_path) and max_retries > 0:
                    time.sleep(1)
                    max_retries -= 1
                
                if not os.path.exists(output_path):
                    raise Exception("El archivo no se creó a tiempo.")
                
                # 5. Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(output_path)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # 6. Limpieza
                if os.path.exists(output_path):
                    os.remove(output_path)
                    
            except Exception as e:
                st.error(f"Error técnico crítico: {e}")
                st.write("Si el error persiste, el servidor no tiene permisos para guardar archivos.")
    else:
        st.warning("Introduce una URL.")
