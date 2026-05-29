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
st.write("Pega el enlace de un video y obtén la transcripción.")

url_video = st.text_input("URL del video:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Descargando y procesando... Esto puede tardar."):
            try:
                # 1. Configuración de descarga
                filename = "audio_final.mp3"
                if os.path.exists(filename):
                    os.remove(filename)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'audio_final',
                    'quiet': True,
                    'no_warnings': True,
                }
                
                # 2. Descarga
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # 3. Transcripción con Whisper
                # Usamos el modelo 'base' que es el estándar recomendado
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                # 4. Mostrar resultado
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # 5. Limpieza
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Asegúrate de que el video es público y no tiene restricciones.")
    else:
        st.warning("Por favor, introduce una URL válida.")
