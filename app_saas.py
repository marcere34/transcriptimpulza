import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de página con diseño Impulza Digital
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #ffffff !important; text-transform: uppercase; }
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
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")

def procesar_audio(archivo):
    model = whisper.load_model("base")
    resultado = model.transcribe(archivo)
    return resultado["text"]

tab1, tab2 = st.tabs(["📥 Descargar desde URL", "📁 Subir archivo (Plan B)"])

with tab1:
    url_video = st.text_input("URL del video:")
    if st.button("Transcribir ahora"):
        if url_video:
            with st.spinner("Procesando video... Esto puede tardar según la duración."):
                try:
                    # Configuración funcional de yt-dlp
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
                    
                    if os.path.exists(filename):
                        texto = procesar_audio(filename)
                        st.success("¡Transcripción lista!")
                        st.text_area("Resultado:", texto, height=300)
                        os.remove(filename)
                    else:
                        st.error("Error al descargar el audio. Usa la pestaña 'Subir archivo'.")
                except Exception as e:
                    st.error(f"Error procesando el video: {e}")
                    st.write("YouTube/TikTok puede bloquear el acceso a servidores de la nube. Intenta usar la pestaña 'Subir archivo'.")

with tab2:
    archivo_subido = st.file_uploader("Sube el audio/video aquí si la URL falla:", type=['mp3', 'mp4', 'wav'])
    if archivo_subido:
        with open("temp_upload.mp3", "wb") as f:
            f.write(archivo_subido.getbuffer())
        texto = procesar_audio("temp_upload.mp3")
        st.text_area("Resultado:", texto, height=300)
        os.remove("temp_upload.mp3")
