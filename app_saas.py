import streamlit as st
import yt_dlp
import whisper
import os
import glob

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
                # 1. Limpieza absoluta
                for f in glob.glob("/tmp/audio_*"):
                    os.remove(f)

                # 2. Descarga SIN post-procesamiento (Cero FFmpeg aquí)
                ydl_opts = {
                    'format': 'bestaudio',
                    'outtmpl': '/tmp/audio_%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'postprocessors': [], # ESTO DESACTIVA TOTALMENTE FFPROBE
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # 3. Encontrar el archivo descargado (sea .webm, .m4a, .mp3, etc.)
                files = glob.glob("/tmp/audio_*")
                if not files:
                    raise Exception("No se encontró ningún archivo descargado.")
                
                filename = files[0]
                
                # 4. Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # 5. Limpieza
                os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Tip: Si el sitio bloquea la descarga, descarga el archivo en tu PC y súbelo manualmente.")
    else:
        st.warning("Introduce una URL.")
