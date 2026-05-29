import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #ffffff !important; text-transform: uppercase; }
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #ffc107 !important; 
        color: #000000 !important; 
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 15px !important;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #5a189a !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Descargando y procesando..."):
            try:
                # 1. Definimos un nombre de archivo fijo y forzamos MP3
                filename = "audio_final.mp3"
                if os.path.exists(filename):
                    os.remove(filename)

                # 2. Configuración robusta de yt-dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'audio_final', # Esto genera audio_final.mp3
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # 3. Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, introduce una URL válida.")
