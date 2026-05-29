import streamlit as st
import yt_dlp
import whisper
import os

st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stButton>button { background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

url_video = st.text_input("URL del video:")
plataforma = st.selectbox("¿Para qué plataforma es este contenido?", ["TikTok", "Instagram", "YouTube Shorts", "LinkedIn"])

if st.button("Transcribir y Optimizar SEO"):
    if url_video:
        with st.spinner("Procesando..."):
            try:
                # 1. Descarga y Transcripción
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '/tmp/temp_audio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                resultado = whisper.load_model("base").transcribe("/tmp/temp_audio.mp3")
                texto = resultado["text"]
                
                # 2. Generación de SEO según plataforma
                st.subheader(f"Estrategia SEO para {plataforma}")
                
                # Definición de lógica por plataforma
                if plataforma == "TikTok":
                    titulo = "¡Tienes que probar esto!"
                    keywords = "IA, automatización, viral, trucos, productividad"
                    hashtags = "#ImpulzaDigital #IA #ContenidoViral #TikTokTips #Productividad"
                elif plataforma == "Instagram":
                    titulo = "Transforma tu marca personal 🚀"
                    keywords = "branding, estrategia, IA, crecimiento, digital"
                    hashtags = "#ImpulzaDigital #MarketingDigital #GrowthHacking #BrandingIA #InstagramSEO"
                else:
                    titulo = "Optimiza tu flujo de trabajo"
                    keywords = "eficiencia, tecnología, IA, negocios"
                    hashtags = "#ImpulzaDigital #IA #WorkSmart #BusinessTips #Tech"

                # Mostrar Resultados
                st.markdown(f"**Título sugerido:** {titulo}")
                st.text_area("Descripción optimizada:", f"Gancho: {texto[:100]}...\n\nCuerpo: {texto[100:400]}...", height=150)
                st.markdown(f"**Palabras clave:** `{keywords}`")
                st.markdown(f"**Hashtags:** {hashtags}")
                
                if os.path.exists("/tmp/temp_audio.mp3"):
                    os.remove("/tmp/temp_audio.mp3")
                    
            except Exception as e:
                st.error(f"Error: {e}")
