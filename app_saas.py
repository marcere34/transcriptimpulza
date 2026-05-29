import streamlit as st
import yt_dlp
import whisper
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="centered")

# Estilos CSS premium ajustados al diseño de Impulza Digital
st.markdown("""
    <style>
    /* Fondo global */
    .stApp { background-color: #0A0A0A; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    
    /* Contenedor tipo Tarjeta de Login */
    .main-login-box {
        background-color: #121212;
        padding: 40px;
        border-radius: 25px;
        border: 1px solid #7B2CBF; /* Morado Impulza */
        box-shadow: 0 10px 30px rgba(123, 44, 191, 0.2);
        text-align: center;
        margin-top: 50px;
    }
    
    /* Títulos con estilo */
    .title-imp { font-size: 32px; font-weight: 900; color: #FFFFFF; margin-bottom: 10px; text-transform: uppercase; }
    .subtitle-imp { font-size: 18px; color: #FFD60A; font-weight: 600; margin-bottom: 25px; }
    
    /* Botón Amarillo Premium */
    .stButton>button { 
        background-color: #FFD60A !important; 
        color: #000000 !important; 
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        padding: 12px !important;
        font-size: 16px;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); background-color: #FFC300 !important; }
    
    /* Inputs estilizados */
    .stTextInput>div>div>input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #3C096C !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Lógica de Sesión
if 'acceso_concedido' not in st.session_state:
    st.session_state.acceso_concedido = False

# 1. LÓGICA DE GOOGLE SHEETS
def guardar_lead(nombre, email):
    try:
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Leads_ProTranscribe").sheet1
        sheet.append_row([nombre, email])
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# 2. PÁGINA DE INICIO (LOGIN)
if not st.session_state.acceso_concedido:
    st.markdown("<div class='main-login-box'>", unsafe_allow_html=True)
    st.markdown("<div class='title-imp'>IMPULZA DIGITAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-imp'>VERIFICACIÓN DE ACCESO</div>", unsafe_allow_html=True)
    st.write("Ingresa tus datos para acceder a tu plataforma de transcripción profesional.")
    
    nombre = st.text_input("", placeholder="Nombre Completo")
    email = st.text_input("", placeholder="Correo Electrónico")
    
    if st.button("ACCEDER AHORA"):
        if nombre and email:
            guardar_lead(nombre, email)
            st.session_state.acceso_concedido = True
            st.rerun()
        else:
            st.warning("Completa los campos para continuar.")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. INTERFAZ PRINCIPAL
else:
    st.title("ProTranscribe por Impulza Digital")
    
    tab1, tab2 = st.tabs(["🚀 Transcripción", "📩 Contacto"])
    
    with tab1:
        url_video = st.text_input("", placeholder="Pega aquí la URL del video...")
        if st.button("Transcribir ahora"):
            if url_video:
                with st.spinner("Procesando audio..."):
                    try:
                        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp_audio.%(ext)s', 'quiet': True}
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url_video, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        model = whisper.load_model("base")
                        resultado = model.transcribe(filename)
                        
                        st.success("¡Transcripción generada!")
                        st.text_area("Resultado final:", resultado["text"], height=300)
                        if os.path.exists(filename): os.remove(filename)
                    except Exception as e:
                        st.error(f"Error procesando: {e}")
            else:
                st.warning("Por favor, introduce una URL válida.")
