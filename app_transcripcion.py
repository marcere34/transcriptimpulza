import streamlit as st
import yt_dlp
import whisper
import os
import streamlit_authenticator as stauth
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="ProTranscribe AI", layout="wide")

# --- CSS MARCA ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stButton>button { background-color: #84139B; color: #FFFFFF; border-radius: 10px; font-weight: bold; }
    .stTextInput>div>div>input { border: 2px solid #CD41C6; background-color: #1A1A1A; color: white; }
    h1 { color: #FFCC00 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN GOOGLE SHEETS ---
def guardar_lead(email):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads_ProTranscribe").sheet1
    sheet.append_row([email])

# --- AUTENTICACIÓN ---
# Nota: Para evitar errores de Hasher, definimos usuarios manualmente.
# En producción, usa un archivo .yaml para gestionar usuarios.
usernames = ['usuario1']
passwords = ['123456']
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate({'usuario1': {'name': 'Usuario Ejemplo', 'password': hashed_passwords[0]}}, 'cookie_name', 'cookie_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.sidebar.title(f"Hola, {name}")
    authenticator.logout('Cerrar sesión', 'sidebar')
    
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Nueva Transcripción", "Captar Leads"])

    if menu == "Captar Leads":
        st.title("📬 Registro de Leads")
        email = st.text_input("Ingresa tu correo para recibir acceso premium:")
        if st.button("Guardar Correo"):
            try:
                guardar_lead(email)
                st.success(f"¡Gracias! {email} guardado en nuestra lista.")
            except Exception as e:
                st.error("Error al conectar con Google Sheets. Asegúrate de tener el archivo credenciales.json.")
    
    elif menu == "Nueva Transcripción":
        st.title("🎙️ Nueva Transcripción")
        url = st.text_input("URL del video:")
        if st.button("Transcribir"):
            with st.spinner("Procesando..."):
                try:
                    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp_audio.%(ext)s', 'quiet': True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                    model = whisper.load_model("base")
                    res = model.transcribe(filename)
                    st.text_area("Resultado:", res["text"], height=300)
                    if os.path.exists(filename): os.remove(filename)
                except Exception as e:
                    st.error(f"Error: {e}")

elif authentication_status == False:
    st.error('Usuario o contraseña incorrectos.')
