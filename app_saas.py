import streamlit as st
import yt_dlp
import whisper
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #ffffff !important; text-transform: uppercase; }
    .stButton>button { 
        background-color: #ffc107 !important; 
        color: #000000 !important; 
        font-weight: 800 !important; 
        border-radius: 10px !important; 
        border: none !important;
        padding: 15px !important;
    }
    .stTextInput>div>div>input { 
        background-color: #1a1a1a !important; 
        color: #ffffff !important; 
        border: 1px solid #5a189a !important; 
        border-radius: 10px !important; 
    }
    .stTextInput label { color: #FFCC00 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe por Impulza Digital")

# Lógica Google Sheets
def guardar_lead(nombre, email):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads_ProTranscribe").sheet1
    sheet.append_row([nombre, email])

tab1, tab2, tab3 = st.tabs(["🚀 Transcripción", "📩 Registro VIP", "📁 Subir archivo"])

with tab1:
    url_video = st.text_input("URL del video:")
    if st.button("Transcribir ahora"):
        if url_video:
            with st.spinner("Procesando..."):
                try:
                    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp_audio.%(ext)s', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_video, download=True)
                        filename = ydl.prepare_filename(info)
                    model = whisper.load_model("base")
                    res = model.transcribe(filename)
                    st.text_area("Resultado:", res["text"], height=300)
                    if os.path.exists(filename): os.remove(filename)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Introduce una URL.")

with tab2:
    nombre = st.text_input("Tu Nombre:")
    email = st.text_input("Tu Correo:")
    if st.button("Guardar en Lista VIP"):
        guardar_lead(nombre, email)
        st.success("¡Registrado!")

with tab3:
    archivo = st.file_uploader("Si la URL falla, sube el archivo:", type=['mp3', 'mp4', 'wav'])
    if archivo:
        with open("upload.mp3", "wb") as f: f.write(archivo.getbuffer())
        model = whisper.load_model("base")
        st.text_area("Resultado:", model.transcribe("upload.mp3")["text"], height=300)
        os.remove("upload.mp3")
```
