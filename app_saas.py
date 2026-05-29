import streamlit as st
import yt_dlp
import whisper
import os

# Configuración visual Impulza Digital
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")
st.markdown("<style>.stApp { background-color: #0d0d0d; color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🌐 Universal Transcript AI")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando..."):
            try:
                # Usamos /tmp por ser la única ruta con permisos totales en Streamlit Cloud
                ydl_opts = {
                    'format': 'bestaudio/best', 
                    'outtmpl': '/tmp/temp_audio', # Sin extensión, dejamos que ffmpeg lo gestione
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'http_headers': {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                    }
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # El archivo resultante siempre será /tmp/temp_audio.mp3
                filename = "/tmp/temp_audio.mp3"
                
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Por favor, introduce una URL válida.")
