import streamlit as st
import yt_dlp
import whisper
import os

# Configuración visual Impulza Digital
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; 
        border-radius: 10px !important; border: 2px solid #84139B !important; 
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important; color: #ffffff !important; 
        border: 2px solid #84139B !important; border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")

# Sesión para guardar la transcripción
if 'transcripcion' not in st.session_state:
    st.session_state.transcripcion = ""

# PASO 1: Transcripción
url_video = st.text_input("URL del video:")
if st.button("Paso 1: Transcribir Video"):
    with st.spinner("Procesando audio..."):
        try:
            ydl_opts = {
                'format': 'bestaudio/best', 
                'outtmpl': '/tmp/temp_audio',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_video])
            
            res = whisper.load_model("base").transcribe("/tmp/temp_audio.mp3")
            st.session_state.transcripcion = res["text"]
            st.success("¡Transcripción completa!")
        except Exception as e:
            st.error(f"Error: {e}")

# PASO 2: Reescritura Inteligente
if st.session_state.transcripcion:
    st.divider()
    st.subheader("Paso 2: Generar Guion Estratégico")
    estilo = st.selectbox("Elige el objetivo del guion:", ["Autoridad (LinkedIn)", "Crecimiento (Instagram)", "Directo (TikTok)"])
    
    if st.button("Generar Guion"):
        txt = st.session_state.transcripcion
        
        if estilo == "Autoridad (LinkedIn)":
            guion = f"El error más común al intentar {txt[:30]} es ignorar la estrategia base.\n\nTras analizar este contenido, he detectado tres puntos clave:\n1. {txt[30:150]}\n2. {txt[150:250]}\n3. {txt[250:350]}\n\nLa conclusión es clara: si quieres resultados, necesitas profesionalizar tu proceso.\n\n¿Qué opinas sobre este enfoque?"
            hashtags = "#Estrategia #ImpulzaDigital #Negocios #Autoridad"
            
        elif estilo == "Crecimiento (Instagram)":
            guion = f"La estrategia exacta para dominar {txt[:30]} 🚀\n\nNo busques atajos, busca sistemas. Esto es lo que realmente marca la diferencia:\n{txt[:300]}...\n\nSi te ha aportado valor, guárdate este post para aplicarlo hoy mismo.\n\n#ImpulzaDigital #Crecimiento"
            hashtags = "#ImpulzaDigital #Branding #CrecimientoDigital #IA"
            
        else: # Estilo Directo (TikTok)
            guion = f"3 pasos para mejorar en {txt[:30]}.\n\nOlvídate de la teoría, vamos a la práctica:\n1. Optimiza: {txt[:100]}\n2. Ejecuta: {txt[100:200]}\n3. Escala: {txt[200:300]}\n\nGuarda este video y ponlo en práctica. Impulza tu marca ya."
            hashtags = "#ImpulzaDigital #TipsIA #Productividad #ContenidoViral"
        
        st.text_area("Tu nuevo guion profesional:", guion, height=300)
        st.markdown(f"**Hashtags recomendados:** {hashtags}")
