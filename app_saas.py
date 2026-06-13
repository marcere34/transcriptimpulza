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
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; 
        border-radius: 10px !important; border: 2px solid #84139B !important; 
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

# Limpieza inicial de archivos huérfanos al cargar la app
for f in glob.glob("/tmp/audio_*"):
    try: os.remove(f)
    except: pass

tab1, tab2 = st.tabs(["🔗 Pegar URL", "📁 Subir Video/Audio"])

file_path = None

with tab1:
    url_video = st.text_input("URL del video:")
    if url_video and st.button("Transcribir URL"):
        with st.spinner("Conectando..."):
            try:
                # Usamos una ruta única para evitar colisiones
                output_template = "/tmp/audio_final"
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': output_template,
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # Buscar cualquier archivo que empiece con el nombre de salida
                possible_files = glob.glob(f"{output_template}*")
                if possible_files: file_path = possible_files[0]
            except Exception as e: st.error(f"Error de descarga: {e}")

with tab2:
    uploaded_file = st.file_uploader("Sube tu archivo:", type=['mp4', 'mp3', 'wav', 'webm'])
    if uploaded_file and st.button("Transcribir Archivo"):
        file_path = f"/tmp/{uploaded_file.name}"
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())

if file_path:
    try:
        with st.spinner("La IA está transcribiendo..."):
            model = whisper.load_model("base")
            resultado = model.transcribe(file_path)
            st.success("¡Transcripción lista!")
            st.text_area("Resultado:", resultado["text"], height=300)
        
        if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        st.error(f"Error en IA: {e}")
