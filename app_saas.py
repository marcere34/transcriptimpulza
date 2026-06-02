import streamlit as st
import yt_dlp
import whisper
import os
import glob
import random

# Configuración de página
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; 
        border-radius: 10px !important; border: 2px solid #84139B !important; 
    }
    .stTextInput>div>div>input {
        background-color: #2a2a2a !important; color: #ffffff !important; 
        border: 2px solid #84139B !important; border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Descargando y procesando..."):
            try:
                # 1. Limpieza absoluta
                for f in glob.glob("/tmp/audio_*"):
                    os.remove(f)

                # 2. Descarga con formato 'best' para evitar errores de disponibilidad
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': '/tmp/audio_%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'postprocessors': [], 
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # 3. Encontrar el archivo descargado
                files = glob.glob("/tmp/audio_*")
                if not files:
                    raise Exception("No se pudo descargar el audio. La plataforma bloqueó la IP o el video no está disponible.")
                
                filename = files[0]
                
                # 4. Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                # 5. Variación de texto para "engañar" al algoritmo
                texto = resultado["text"]
                if random.random() > 0.5:
                    texto = texto.replace("!", ".").replace("?", ".")
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", texto, height=300)
                
                os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Tip: Si el error persiste, intenta con otro video o verifica que el enlace sea público.")
    else:
        st.warning("Introduce una URL.")
