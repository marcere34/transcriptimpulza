import streamlit as st
import whisper
import os

# Configuración y Estilo
st.set_page_config(page_title="ProTranscribe por Impulza Digital", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    h1 { color: #FFCC00 !important; text-transform: uppercase; font-weight: 800; }
    .stButton>button { 
        background-color: #FFCC00 !important; color: #000000 !important; font-weight: 800 !important; 
        border-radius: 10px !important; border: 2px solid #84139B !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("ProTranscribe - Impulza Digital")
st.write("Sube tu video o audio para obtener la transcripción exacta.")

# Único método de entrada para evitar bloqueos
archivo_subido = st.file_uploader("Arrastra tu archivo aquí (MP4, MP3, WAV):", type=['mp4', 'mp3', 'wav'])

if st.button("Transcribir ahora"):
    if archivo_subido:
        with st.spinner("Procesando audio..."):
            try:
                # Guardar temporalmente
                temp_path = "/tmp/archivo_temporal"
                with open(temp_path, "wb") as f:
                    f.write(archivo_subido.getbuffer())
                
                # Transcripción
                model = whisper.load_model("base")
                resultado = model.transcribe(temp_path)
                
                st.success("¡Transcripción lista!")
                st.text_area("Resultado:", resultado["text"], height=300)
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, sube un archivo primero.")
