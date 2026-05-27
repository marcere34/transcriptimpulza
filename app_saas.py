import streamlit as st
import streamlit_authenticator as stauth
import yt_dlp
import whisper
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="ProTranscribe SaaS", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stButton>button { background-color: #84139B; color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# 1. AUTENTICACIÓN
config = {
    'credentials': {
        'usernames': {
            'usuario1': {
                'name': 'Tu Nombre',
                'password': '123456'
            }
        }
    },
    'cookie': {'name': 'pro_transcribe', 'key': 'secret_key', 'expiry_days': 30}
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Corrección: Usamos el método .login() directamente, 
# si falla, es que la versión requiere el nombre del formulario explícito.
try:
    # Intento de login estándar
    name, authentication_status, username = authenticator.login()
except:
    # Fallback para versiones anteriores
    name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.sidebar.write(f"Bienvenido, **{name}**")
    
    # 2. LÓGICA DE GOOGLE SHEETS
    def guardar_lead(email):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("Leads_ProTranscribe").sheet1
        sheet.append_row([email])

    # 3. INTERFAZ
    tab1, tab2 = st.tabs(["Nueva Transcripción", "Captar Leads"])
    
    with tab1:
        url = st.text_input("URL del video:")
        if st.button("Transcribir"):
            st.write("Procesando video...")
            
    with tab2:
        email = st.text_input("Correo del cliente:")
        if st.button("Guardar en Sheets"):
            try:
                guardar_lead(email)
                st.success("Correo guardado con éxito en la hoja de cálculo.")
            except Exception as e:
                st.error(f"Error al conectar con Google Sheets: {e}")

elif authentication_status is False:
    st.error("Usuario o contraseña incorrectos")
