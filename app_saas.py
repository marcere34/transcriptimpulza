import streamlit as st
import yt_dlp
import whisper
import os
import glob
import random

# Configuración de página
st.set_page_config(
    page_title="ProTranscribe AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

/* Fondo general */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(205, 65, 198, 0.16), transparent 30%),
        linear-gradient(180deg, #ffffff 0%, #f8f3fa 100%);
    color: #111111;
}

/* Ocultar elementos de Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

/* Contenedor principal */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Títulos */
h1 {
    color: #111111 !important;
    font-size: 48px !important;
    font-weight: 800 !important;
    letter-spacing: -2px !important;
    text-transform: none !important;
}

/* Etiquetas */
.stTextInput label,
.stFileUploader label {
    color: #111111 !important;
    font-weight: 700 !important;
}

/* Inputs */
div[data-baseweb="input"] > div {
    min-height: 54px;
    border-radius: 14px;
    border: 1px solid rgba(132, 19, 155, 0.20);
    background: #ffffff;
}

div[data-baseweb="input"] > div:focus-within {
    border-color: #84139B;
    box-shadow: 0 0 0 4px rgba(132, 19, 155, 0.08);
}

/* Botones */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border: none !important;
    border-radius: 15px !important;
    background: linear-gradient(135deg, #84139B, #CD41C6) !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    box-shadow: 0 14px 30px rgba(132, 19, 155, 0.25);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 35px rgba(132, 19, 155, 0.35);
}

/* Pestañas */
button[data-baseweb="tab"] {
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 700;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #84139B !important;
    background: rgba(132, 19, 155, 0.08);
}

/* Subir archivo */
[data-testid="stFileUploaderDropzone"] {
    min-height: 160px;
    border: 2px dashed rgba(132, 19, 155, 0.30);
    border-radius: 18px;
    background: rgba(132, 19, 155, 0.05);
}

/* Caja de texto */
textarea {
    border-radius: 16px !important;
    border: 1px solid rgba(132, 19, 155, 0.20) !important;
    background: #ffffff !important;
    color: #111111 !important;
}

/* Alertas */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Móvil */
@media (max-width: 700px) {
    .block-container {
        padding-left: 16px;
        padding-right: 16px;
    }

    h1 {
        font-size: 36px !important;
    }
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #84139B 0%, #CD41C6 100%);
    padding: 34px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 20px 50px rgba(132, 19, 155, 0.25);
">
    <div style="
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.6px;
        color: #FFCC00;
        margin-bottom: 10px;
    ">
        IMPULZA DIGITAL
    </div>

    <div style="
        font-size: 44px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 12px;
    ">
        ProTranscribe AI
    </div>

    <div style="
        font-size: 17px;
        line-height: 1.6;
        max-width: 760px;
        color: rgba(255,255,255,0.92);
    ">
        Transcribe videos y audios desde una URL o subiendo un archivo.
        Detecta el idioma y traduce el resultado al español.
    </div>
</div>
""", unsafe_allow_html=True)
# Limpieza inicial
for f in glob.glob("/tmp/audio_*"):
    try: os.remove(f)
    except: pass

if 'file_path' not in st.session_state:
    st.session_state.file_path = None

tab1, tab2 = st.tabs(["🔗 Pegar URL", "📁 Subir Video/Audio"])

with tab1:
    url_video = st.text_input("URL del video:")
    if st.button("Transcribir URL"):
        if url_video:
            with st.spinner("Conectando..."):
                try:
                    output_template = "/tmp/audio_final"
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': output_template,
                        'quiet': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url_video])
                    
                    possible_files = glob.glob(f"{output_template}*")
                    if possible_files: st.session_state.file_path = possible_files[0]
                except Exception as e: st.error(f"Error de descarga: {e}")
        else:
            st.warning("Por favor, ingresa una URL.")

with tab2:
    # El file_uploader ahora es persistente y está siempre visible en la pestaña
    uploaded_file = st.file_uploader("Sube tu archivo (mp4, mp3, wav, webm):", type=['mp4', 'mp3', 'wav', 'webm'])
    
    if uploaded_file is not None:
        if st.button("Procesar Archivo Subido"):
            path = f"/tmp/{uploaded_file.name}"
            with open(path, "wb") as f: f.write(uploaded_file.getbuffer())
            st.session_state.file_path = path

# Proceso de transcripción unificado
if st.session_state.file_path:
    try:
        with st.spinner("La IA está transcribiendo..."):
            model = whisper.load_model("base")
            resultado = model.transcribe(st.session_state.file_path)
            st.success("¡Transcripción lista!")
            st.text_area("Resultado:", resultado["text"], height=300)
        
        # Limpieza después de procesar
        if os.path.exists(st.session_state.file_path): 
            os.remove(st.session_state.file_path)
        st.session_state.file_path = None
    except Exception as e:
        st.error(f"Error en IA: {e}")
        st.session_state.file_path = None
