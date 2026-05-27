import streamlit as st
import yt_dlp
import whisper
import os

st.title("TikTok Transcript Pro")
st.write("Pega el enlace de tu TikTok y obtén la transcripción al instante.")

url_video = st.text_input("URL del video de TikTok:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video..."):
            try:
                # Quitamos los 'postprocessors' que causan el error de ffprobe
                ydl_opts = {
                    'format': 'bestaudio',
                    'outtmpl': 'temp_audio.%(ext)s',
                    'extractor_args': {'tiktok': {'impersonate': 'chrome'}},
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    filename = ydl.prepare_filename(info)
                
                # Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.write("Intenta con otro video o verifica que el link sea correcto.")
    else:
        st.warning("Por favor, introduce una URL válida.")
