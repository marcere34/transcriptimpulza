import yt_dlp
import whisper
import os
import openai # IMPORTANTE: Necesitas esta librería para que la IA escriba el guion

# Configuración
st.set_page_config(page_title="ProTranscribe - Impulza Digital", layout="wide")
# Configuración de página con tus colores de marca
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

st.title("ProTranscribe - Impulza Digital")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stTextInput label { color: #CD41C6 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #FFCC00 !important; 
        color: #000000 !important; 
        font-weight: 800 !important; 
        border-radius: 10px !important;
        border: 2px solid #84139B !important;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important; 
        color: #ffffff !important; 
        border: 2px solid #84139B !important; 
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Aquí configurarías tu API KEY en los Secrets de Streamlit
# st.secrets["OPENAI_API_KEY"]
st.title("ProTranscribe - Impulza Digital")
st.write("Pega el enlace de un video y obtén la transcripción.")

def generar_guion_ia(texto, plataforma):
    # Esto es lo que "reescribe" de verdad el texto
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = f"Eres un experto en redes sociales. Reescribe este guion para {plataforma} enfocándote en SEO y viralidad, creando un gancho, cuerpo y llamado a la acción: {texto}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
url_video = st.text_input("URL del video:")

# ... (El resto de tu lógica de transcripción igual) ...
if st.button("Transcribir ahora"):
    if url_video:
        with st.spinner("Procesando video... Esto puede tardar según la duración."):
            try:
                # Configuramos yt-dlp con las cabeceras que ya sabemos que funcionan
                ydl_opts = {
                    'format': 'bestaudio/best', 
                    'outtmpl': '/tmp/temp_audio', # Ruta segura en /tmp
                    'quiet': True,
                    'no_warnings': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'http_headers': {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                    }
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_video])
                
                filename = "/tmp/temp_audio.mp3"
                
                # Carga del modelo Whisper
                model = whisper.load_model("base")
                resultado = model.transcribe(filename)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                # Limpieza
                if os.path.exists(filename):
                    os.remove(filename)
                    
            except Exception as e:
                st.error(f"Error procesando el video: {e}")
    else:
        st.warning("Por favor, introduce una URL válida.")
