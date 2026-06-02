import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página con tus colores de marca
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
                # SOLUCIÓN DEFINITIVA: postprocessors: [] desactiva ffmpeg por completo
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '/tmp/audio_final',
                    'quiet': True,
                    'no_warnings': True,
                    'postprocessors': [], 
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    # Detectamos el archivo real descargado aunque la extensión varíe
                    filename = "/tmp/audio_final." + info.get('ext')
                
                # Carga del modelo Whisper
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Si el error persiste, usa la opción de subir archivo manualmente.")
    else:
        st.warning("Introduce una URL.")
