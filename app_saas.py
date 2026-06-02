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

# Sesión para guardar
if 'transcripcion' not in st.session_state:
    st.session_state.transcripcion = None

url_video = st.text_input("URL del video:")

# PASO 1: Transcripción
if st.button("Paso 1: Transcribir Video"):
    if url_video:
        with st.spinner("Descargando audio..."):
            try:
                # Quitamos postprocessors para evitar error de ffprobe
                ydl_opts = {
                    'format': 'bestaudio/best', 
                    'outtmpl': '/tmp/temp_audio',
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                # Buscamos cualquier archivo en /tmp que sea el audio descargado
                # (yt-dlp a veces añade extensiones como .webm o .m4a)
                temp_file = None
                for f in os.listdir('/tmp/'):
                    if f.startswith('temp_audio'):
                        temp_file = os.path.join('/tmp/', f)
                
                if temp_file:
                    res = whisper.load_model("base").transcribe(temp_file)
                    st.session_state.transcripcion = res["text"]
                    st.success("¡Transcripción completa!")
                    os.remove(temp_file)
                else:
                    st.error("No se encontró el archivo descargado.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Introduce una URL.")

# PASO 2: Reescritura Estratégica
if st.session_state.transcripcion:
    st.divider()
    st.subheader("Paso 2: Generar Guion Estratégico")
    estilo = st.selectbox("Elige el objetivo:", ["Viral (Alto Impacto)", "Autoridad (LinkedIn)", "Crecimiento (Instagram)"])
    
    if st.button("Generar Guion"):
        txt = st.session_state.transcripcion
        if estilo == "Viral (Alto Impacto)":
            guion = f"El mercado te ha estado mintiendo sobre {txt[:50]}.\n\nOlvídate de lo que siempre escuchas. La realidad es que:\n{txt[50:200]}...\n\nSi quieres resultados distintos, deja de hacer lo mismo de siempre.\n\nEl sistema es este:\n1. {txt[200:300]}\n2. {txt[300:400]}\n\nImpulza tu marca. Comenta 'GUION' si quieres escalar."
            hashtags = "#ImpulzaDigital #Estrategia #AltoImpacto #IA"
        elif estilo == "Autoridad (LinkedIn)":
            guion = f"El error más común al intentar {txt[:30]} es ignorar la estrategia base.\n\nHe detectado puntos clave:\n{txt[30:300]}...\n\nLa conclusión es clara: necesitas profesionalizar tu proceso.\n\n¿Qué opinas sobre este enfoque?"
            hashtags = "#Estrategia #ImpulzaDigital #Negocios #Autoridad"
        else:
            guion = f"La estrategia exacta para dominar {txt[:30]} 🚀\n\nEsto es lo que realmente marca la diferencia:\n{txt[:300]}...\n\nGuarda este post si quieres aplicarlo hoy."
            hashtags = "#ImpulzaDigital #Branding #CrecimientoDigital #IA"
        
        st.text_area("Tu nuevo guion profesional:", guion, height=300)
        st.markdown(f"**Hashtags:** {hashtags}")
