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

# PASO 2: Reescritura Estratégica
if st.session_state.transcripcion:
    st.divider()
    st.subheader("Paso 2: Generar Guion Estratégico")
    estilo = st.selectbox("Elige el objetivo:", ["Autoridad (LinkedIn)", "Crecimiento (Instagram)", "Viral (Alto Impacto)"])
    
    if st.button("Generar Guion"):
        txt = st.session_state.transcripcion
        
        if estilo == "Viral (Alto Impacto)":
            guion = f"El mercado te ha estado mintiendo sobre {txt[:30]}.\n\nOlvídate de lo que siempre escuchas. La realidad es que:\n{txt[30:200]}...\n\nSi quieres resultados distintos, deja de hacer lo mismo de siempre.\n\nEl sistema es este:\n1. {txt[200:300]}\n2. {txt[300:400]}\n\nImpulza tu marca. Comenta 'GUION' si quieres que te explique cómo escalar esto a otro nivel."
            hashtags = "#ImpulzaDigital #Estrategia #AltoImpacto #IA"
            
        elif estilo == "Autoridad (LinkedIn)":
            guion = f"El error más común al intentar {txt[:30]} es ignorar la estrategia base.\n\nHe analizado el proceso y detectado puntos clave:\n{txt[30:300]}...\n\nLa conclusión es clara: necesitas profesionalizar tu proceso.\n\n¿Qué opinas sobre este enfoque?"
            hashtags = "#Estrategia #ImpulzaDigital #Negocios #Autoridad"
            
        else: # Crecimiento (Instagram)
            guion = f"La estrategia exacta para dominar {txt[:30]} 🚀\n\nNo busques atajos, busca sistemas. Esto es lo que realmente marca la diferencia:\n{txt[:300]}...\n\nGuarda este post si quieres aplicarlo hoy mismo."
            hashtags = "#ImpulzaDigital #Branding #CrecimientoDigital #IA"
        
        st.text_area("Tu nuevo guion profesional:", guion, height=300)
        st.markdown(f"**Hashtags:** {hashtags}")
```

### Por qué esta estructura "Viral" funciona:
*   **"El mercado te ha estado mintiendo":** Esto es un *Pattern Interrupt*. La gente se detiene porque siente curiosidad o indignación positiva.
*   **"Olvídate de lo que siempre escuchas":** Esto te posiciona instantáneamente como la persona que tiene la verdad, no alguien que repite lo mismo que todos.
*   **Sistema Paso a Paso:** Los videos virales de alto impacto siempre enumeran los pasos. El cerebro humano ama las listas porque parecen "fáciles de seguir".

¿Qué tal se siente este cambio de tono? Ya no es Clickbait, es **Contenido de Autoridad**. Haz el *Commit* y el *Reboot* y cuéntame qué te parece.
