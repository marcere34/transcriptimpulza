import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Debug ProTranscribe", layout="wide")

st.title("Debug: ProTranscribe")
url_video = st.text_input("URL del video:")

if st.button("Probar Descarga"):
    if url_video:
        with st.spinner("Diagnosticando..."):
            try:
                # Limpiamos /tmp antes de probar
                for f in os.listdir('/tmp/'):
                    if f.startswith('audio_final'):
                        os.remove(os.path.join('/tmp/', f))
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '/tmp/audio_final',
                    'quiet': False, # CAMBIADO A FALSE para ver errores en los logs
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    st.write("Info extraída. Revisando archivos en /tmp/...")
                
                archivos_en_tmp = os.listdir('/tmp/')
                st.write(f"Archivos encontrados en /tmp/: {archivos_en_tmp}")
                
            except Exception as e:
                st.error(f"Error detallado: {e}")
