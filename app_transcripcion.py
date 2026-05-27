# --- APLICACIÓN DE TRANSCRIPCIÓN TIKTOK (VERSIÓN APP) ---
import streamlit as st
import yt_dlp
import whisper
import os

st.title("TikTok Transcript Pro")
st.write("Pega el enlace de tu TikTok y obtén la transcripción al instante.")

url_video = st.text_input("URL del video de TikTok:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video... esto puede tardar un poco."):
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'temp_audio.mp3',
                    'extractor_args': {'tiktok': {'impersonate': 'chrome'}},
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                model = whisper.load_model("base")
                resultado = model.transcribe("temp_audio.mp3")
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists("temp_audio.mp3"):
                    os.remove("temp_audio.mp3")
                    
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Por favor, introduce una URL válida.")