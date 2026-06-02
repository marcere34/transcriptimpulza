import streamlit as st
import yt_dlp
import whisper
import os
import glob

# Configuración visual
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
        background-color: #1a1a1a !important; color: #ffffff !important; 
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
                # Limpieza previa de cualquier residuo en /tmp
                for f in glob.glob("/tmp/audio_impulza*"):
                    os.remove(f)

                # Descarga sin forzar extensiones
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': '/tmp/audio_impulza',
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # BUSCADOR INTELIGENTE: Busca cualquier archivo que haya creado yt-dlp
                lista_archivos = glob.glob("/tmp/audio_impulza*")
                
                if not lista_archivos:
                    raise Exception("No se encontró ningún archivo descargado.")
                
                filename = lista_archivos[0]
                
                # Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza final
                os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Si el error persiste, el sitio está bloqueando la IP.")
    else:
        st.warning("Por favor, introduce una URL válida.")
