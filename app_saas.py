import streamlit as st
import yt_dlp
import whisper
import os
import glob

# Configuración
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; }
    .stButton>button { background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

url = st.text_input("URL del video:")
archivo_subido = st.file_uploader("O sube tu archivo aquí:", type=['mp4', 'mp3', 'wav'])

if st.button("Transcribir ahora"):
    archivo_a_procesar = None
    
    # 1. Prioridad: Subida manual
    if archivo_subido:
        archivo_a_procesar = "/tmp/temp_upload.mp3"
        with open(archivo_a_procesar, "wb") as f:
            f.write(archivo_subido.getbuffer())
    
    # 2. Si no hay subida, intentar URL
    elif url:
        with st.spinner("Descargando desde URL..."):
            try:
                # Forzamos la descarga en /tmp con un nombre genérico
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '/tmp/video_download',
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # BUSCADOR FLEXIBLE: Busca cualquier archivo que haya dejado yt-dlp en /tmp
                lista_archivos = glob.glob("/tmp/video_download*")
                if lista_archivos:
                    archivo_a_procesar = lista_archivos[0]
                else:
                    st.error("No se encontró el archivo descargado. Intenta subirlo manualmente.")
            except Exception as e:
                st.error(f"Error en la descarga: {e}")

    # 3. Transcripción
    if archivo_a_procesar:
        with st.spinner("Transcribiendo..."):
            try:
                model = whisper.load_model("base")
                resultado = model.transcribe(archivo_a_procesar)
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza
                if os.path.exists(archivo_a_procesar):
                    os.remove(archivo_a_procesar)
            except Exception as e:
                st.error(f"Error en transcripción: {e}")
