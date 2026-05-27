import streamlit as st
import yt_dlp
import whisper
import os
import streamlit_authenticator as stauth

# Configuración de la página
st.set_page_config(page_title="ProTranscribe AI", layout="wide")

# Estilos CSS con tus colores de marca
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stSidebar { background-color: #4D184A; }
    .stButton>button { background-color: #84139B; color: #FFFFFF; border-radius: 10px; font-weight: bold; }
    .stTextInput>div>div>input { border: 2px solid #CD41C6; background-color: #1A1A1A; color: white; }
    h1, h2, h3 { color: #FFCC00; }
    </style>
""", unsafe_allow_html=True)

# Simulación de base de datos de usuarios (en un SaaS real, esto iría a Firestore)
names = ['Usuario Ejemplo']
usernames = ['usuario1']
passwords = ['123456'] # En producción, usa contraseñas hasheadas
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'protranscribe_key', 'cookie_key', cookie_expiry_days=30)

# Interfaz de Login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Usuario o contraseña incorrectos.')
elif authentication_status == None:
    st.warning('Por favor, introduce tus credenciales.')
else:
    # --- Interfaz una vez logueado ---
    st.sidebar.title(f"Bienvenido {name}")
    authenticator.logout('Cerrar sesión', 'sidebar')
    
    menu = st.sidebar.radio("Navegación", ["Dashboard", "Nueva Transcripción", "Mi Cuenta"])

    if menu == "Dashboard":
        st.title("Hola de nuevo 👋")
        st.write("Bienvenido a tu panel de control profesional.")
        st.info("Aquí aparecerá tu historial de transcripciones próximamente.")

    elif menu == "Nueva Transcripción":
        st.title("🎙️ Nueva Transcripción")
        url = st.text_input("Pega aquí la URL del video (TikTok, YouTube, FB, IG):")
        
        if st.button("Transcribir ahora"):
            if url:
                with st.spinner("Procesando con IA..."):
                    try:
                        ydl_opts = {
                            'format': 'bestaudio/best', 
                            'outtmpl': 'temp_audio.%(ext)s', 
                            'quiet': True,
                            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                            'nocheckcertificate': True
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            filename = ydl.prepare_filename(info)
                        
                        model = whisper.load_model("base")
                        res = model.transcribe(filename)
                        
                        st.success("¡Transcripción completa!")
                        st.text_area("Resultado:", res["text"], height=300)
                        
                        if os.path.exists(filename): os.remove(filename)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Ingresa una URL válida.")

    elif menu == "Mi Cuenta":
        st.title("Configuración")
        st.write(f"Usuario: **{username}**")
        st.write("Tu plan actual: **Gratuito**")
