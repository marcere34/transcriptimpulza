import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

# Estilos CSS estilo Impulza Digital (Fondo oscuro, botones amarillos, bordes morados)
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    
    /* Títulos */
    h1 { color: #ffffff !important; text-transform: uppercase; }
    
    /* Botón Amarillo Estilo Impulza */
    .stButton>button { 
        background-color: #ffc107 !important; 
        color: #000000 !important; 
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 15px !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #5a189a !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")
st.write("Pega el enlace de un video y obtén la transcripción.")

# INTERFAZ
url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video... Esto puede tardar según la duración."):
            try:
                # Tu configuración robusta que ya probaste
                ydl_opts = {
                    'format': 'bestaudio/best', 
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'nocheckcertificate': True,
                    'ignoreerrors': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    filename = ydl.prepare_filename(info)
                
                # Carga del modelo Whisper
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error procesando el video: {e}")
                st.write("YouTube/TikTok puede bloquear el acceso a servidores. Si el error persiste, intenta con otro enlace.")
    else:
        st.warning("Por favor, introduce una URL válida.")
