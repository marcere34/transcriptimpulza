import streamlit as st
import yt_dlp
import whisper
import os

# Configuración de la página
st.set_page_config(page_title="TikTok Transcript Pro", page_icon="🎙️")

st.title("🎙️ TikTok Transcript Pro")
st.write("Pega el enlace de tu TikTok y obtén la transcripción al instante.")

url_video = st.text_input("URL del video de TikTok:")

if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video... Esto puede tardar un poco dependiendo de la duración."):
            try:
                # Opciones configuradas para máxima compatibilidad y evitar bloqueos
                ydl_opts = {
                    'format': 'best', 
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }
                
                # Descarga del video/audio
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_video, download=True)
                    filename = ydl.prepare_filename(info)
                
                # Carga del modelo de IA Whisper
                # Usamos 'base' para un equilibrio entre velocidad y precisión
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza de archivos temporales
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error técnico al procesar el video: {e}")
                st.write("Tip: Asegúrate de que el video sea público y que el enlace sea correcto.")
    else:
        st.warning("Por favor, introduce una URL válida de TikTok.")
