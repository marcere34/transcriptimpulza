import streamlit as st
import yt_dlp
import whisper
import os

# Configuración visual Impulza Digital
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; font-weight: 800; text-transform: uppercase; }
    .stButton>button { background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

if 'transcripcion' not in st.session_state:
    st.session_state.transcripcion = None

url_video = st.text_input("URL del video:")

# PASO 1: Transcripción Literal
if st.button("Paso 1: Obtener Transcripción Literal"):
    if url_video:
        with st.spinner("Procesando..."):
            try:
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '/tmp/temp_audio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                resultado = whisper.load_model("base").transcribe("/tmp/temp_audio.mp3")
                st.session_state.transcripcion = resultado["text"]
                st.success("¡Transcripción literal obtenida!")
            except Exception as e:
                st.error(f"Error: {e}")

# PASO 2: Visualización y Reescritura Estratégica
if st.session_state.transcripcion:
    st.divider()
    st.subheader("Paso 2: Material Bruto")
    st.text_area("Transcripción literal:", st.session_state.transcripcion, height=200)
    
    st.divider()
    st.subheader("Paso 3: Reescritura Estratégica SEO")
    plataforma = st.selectbox("¿En qué red social lo vas a publicar?", ["TikTok", "Instagram", "LinkedIn"])
    
    if st.button("Generar Nuevo Guion SEO"):
        with st.spinner("Creando guion estratégico..."):
            texto = st.session_state.transcripcion
            
            # Lógica SEO por plataforma (Palabras Clave + Estructura)
            if plataforma == "TikTok":
                guion = f"GANCHO (3s): ¿Sabías que {texto[:50]}...? ¡Hoy te enseño a solucionarlo!\n\nCONTENIDO: {texto[:300]}...\n\nCTA: Comenta 'IA' para más info.\n\nPALABRAS CLAVE: viral, trucos, automatización, {plataforma.lower()}, tips."
                hashtags = "#ImpulzaDigital #TikTokViral #IA #ContenidoInteligente #Tips"
            elif plataforma == "Instagram":
                guion = f"TÍTULO: La verdad sobre {plataforma.lower()}.\n\nCUERPO: Analizando la idea de: {texto[:300]}...\n\nCONCLUSIÓN: Guarda este post para después.\n\nPALABRAS CLAVE: estrategia, marca personal, branding, crecimiento, {plataforma.lower()}."
                hashtags = "#ImpulzaDigital #InstagramSEO #MarcaPersonal #Growth #DigitalMarketing"
            else:
                guion = f"TITULO PROFESIONAL: El futuro de {texto[:50]}.\n\nDESARROLLO: Basado en el concepto: {texto[:300]}...\n\nPALABRAS CLAVE: negocios, eficiencia, {plataforma.lower()}, tecnología."
                hashtags = "#ImpulzaDigital #Business #InteligenciaArtificial #Tech #Productor"

            st.markdown(f"### Nuevo Guion para {plataforma}")
            st.text_area("Guion reescrito:", guion, height=300)
            st.markdown(f"**Hashtags recomendados:** {hashtags}")
