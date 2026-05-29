import streamlit as st
import yt_dlp
import whisper
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración inicial de la página
st.set_page_config(page_title="ProTranscribe SaaS", layout="centered")

# Estilos CSS mejorados para un look tipo SaaS premium
st.markdown("""
    <style>
    /* Fondo limpio y tipografía base */
    .stApp { background-color: #ffffff; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    
    /* Contenedor principal */
    .main .block-container { padding-top: 2rem; }
    
    /* Títulos */
    h1 { color: #1a1a1a !important; font-weight: 800 !important; letter-spacing: -1px; }
    
    /* Input personalizado */
    .stTextInput>div>div>input { 
        background-color: #f8f9fa; 
        border: 1px solid #e0e0e0; 
        border-radius: 8px; 
        padding: 12px;
        color: #1a1a1a;
    }
    
    /* Botón estilo SaaS moderno */
    .stButton>button { 
        background-color: #1a1a1a !important; 
        color: #ffffff !important; 
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover { background-color: #444444 !important; }
    
    /* Área de resultados */
    .stTextArea textarea { 
        border-radius: 12px; 
        border: 1px solid #e0e0e0;
        background-color: #fcfcfc;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe AI")
st.subheader("Transforma video a texto con IA de alta precisión.")

# 1. LÓGICA DE GOOGLE SHEETS
def guardar_lead(email):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    sheet = client.open("Leads_ProTranscribe").sheet1
    sheet.append_row([email])

# 2. INTERFAZ
tab1, tab2 = st.tabs(["🚀 Transcripción", "📩 Captar Leads"])

with tab1:
    url_video = st.text_input("", placeholder="Pega aquí la URL del video...")
    if st.button("Transcribir ahora"):
        if url_video:
            with st.spinner("Procesando contenido..."):
                try:
                    ydl_opts = {
                        'format': 'bestaudio/best', 
                        'outtmpl': 'temp_audio.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'nocheckcertificate': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_video, download=True)
                        filename = ydl.prepare_filename(info)
                    
                    model = whisper.load_model("base")
                    resultado = model.transcribe(filename)
                    
                    st.success("¡Transcripción generada!")
                    st.text_area("Resultado final:", resultado["text"], height=300)
                    
                    if os.path.exists(filename):
                        os.remove(filename)
                        
                except Exception as e:
                    st.error(f"Error procesando: {e}")
        else:
            st.warning("Por favor, introduce una URL válida.")
        
with tab2:
    email = st.text_input("Introduce el correo del cliente:")
    if st.button("Guardar contacto"):
        try:
            guardar_lead(email)
            st.success("Contacto guardado correctamente.")
        except Exception as e:
            st.error(f"Error: {e}")
