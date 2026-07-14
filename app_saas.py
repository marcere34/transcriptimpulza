import streamlit as st
import yt_dlp
import whisper
import os
import glob
from deep_translator import GoogleTranslator


# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="ProTranscribe AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# APARIENCIA SAAS — IMPULZA DIGITAL
# =========================================================

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background:
        radial-gradient(
            circle at top left,
            rgba(205, 65, 198, 0.16),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f8f3fa 100%
        );
    color: #111111;
}

/* Ocultar elementos visuales de Streamlit */
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

/* Tarjeta principal */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.94);
    border: 1px solid rgba(132, 19, 155, 0.14);
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(54, 17, 65, 0.10);
}

/* Etiquetas */
.stTextInput label,
.stFileUploader label,
.stSelectbox label,
.stTextArea label {
    color: #171219 !important;
    font-weight: 700 !important;
}

/* Campo para pegar URL */
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

/* Selector de idiomas */
div[data-baseweb="select"] > div {
    min-height: 52px;
    border-radius: 14px;
    border: 1px solid rgba(132, 19, 155, 0.20);
    background: #ffffff;
}

/* Botones principales */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border: none !important;
    border-radius: 15px !important;
    background:
        linear-gradient(
            135deg,
            #84139B,
            #CD41C6
        ) !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    box-shadow: 0 14px 30px rgba(132, 19, 155, 0.24);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 36px rgba(132, 19, 155, 0.34);
}

/* Pestañas */
div[data-baseweb="tab-list"] {
    gap: 8px;
    padding: 6px;
    border-radius: 16px;
    background: rgba(132, 19, 155, 0.06);
}

button[data-baseweb="tab"] {
    min-height: 48px;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 700;
    color: #6d6470;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #84139B !important;
    background: #ffffff;
    box-shadow: 0 7px 20px rgba(52, 16, 64, 0.09);
}

/* Ocultar línea inferior de pestañas */
div[data-baseweb="tab-highlight"] {
    display: none;
}

/* Área para subir archivos */
[data-testid="stFileUploaderDropzone"] {
    min-height: 165px;
    border: 2px dashed rgba(132, 19, 155, 0.30);
    border-radius: 18px;
    background: rgba(132, 19, 155, 0.05);
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #84139B;
    background: rgba(132, 19, 155, 0.08);
}

/* Botón del cargador de archivos */
[data-testid="stFileUploaderDropzone"] button {
    border: 1px solid rgba(132, 19, 155, 0.24) !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    color: #84139B !important;
    font-weight: 700 !important;
}

/* Áreas de texto */
textarea {
    border-radius: 16px !important;
    border: 1px solid rgba(132, 19, 155, 0.20) !important;
    background: #ffffff !important;
    color: #111111 !important;
    line-height: 1.65 !important;
}

textarea:focus {
    border-color: #84139B !important;
    box-shadow: 0 0 0 4px rgba(132, 19, 155, 0.08) !important;
}

/* Mensajes y alertas */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: #84139B;
}

/* Separación entre elementos */
[data-testid="stVerticalBlock"] {
    gap: 1rem;
}

/* Adaptación para celular */
@media (max-width: 700px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
        padding-top: 1rem;
    }

    div[data-baseweb="tab-list"] {
        flex-direction: column;
    }

    button[data-baseweb="tab"] {
        width: 100%;
    }

    .saas-title {
        font-size: 36px !important;
    }

    .saas-hero {
        padding: 25px !important;
        border-radius: 20px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO SAAS
# =========================================================

st.markdown("""
<div class="saas-hero" style="
    background:
        linear-gradient(
            135deg,
            #84139B 0%,
            #CD41C6 100%
        );
    padding: 36px;
    border-radius: 26px;
    color: white;
    margin-bottom: 28px;
    box-shadow:
        0 22px 55px rgba(132, 19, 155, 0.25);
">

    <div style="
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255, 204, 0, 0.16);
        color: #FFCC00;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
    ">
        IMPULZA DIGITAL
    </div>

    <div class="saas-title" style="
        font-size: 48px;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -2px;
        margin-bottom: 14px;
    ">
        ProTranscribe AI
    </div>

    <div style="
        font-size: 17px;
        line-height: 1.65;
        max-width: 760px;
        color: rgba(255, 255, 255, 0.92);
    ">
        Transcribe videos y audios desde una URL o subiendo un archivo.
        Después puedes traducir el resultado al idioma que necesites.
    </div>

    <div style="
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 22px;
    ">
        <span style="
            padding: 7px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,0.13);
            font-size: 12px;
            font-weight: 600;
        ">
            URL de video
        </span>

        <span style="
            padding: 7px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,0.13);
            font-size: 12px;
            font-weight: 600;
        ">
            Subir archivo
        </span>

        <span style="
            padding: 7px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,0.13);
            font-size: 12px;
            font-weight: 600;
        ">
            Traducción automática
        </span>
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# CÓDIGO ORIGINAL DE TU APLICACIÓN
# NO SE CAMBIÓ LA LÓGICA
# =========================================================

# Inicialización de estado
if 'texto_transcrito' not in st.session_state:
    st.session_state.texto_transcrito = None


# Función para dividir texto largo y traducir por partes
def traducir_texto_largo(texto, destino):
    # Dividimos en trozos de 4000 caracteres
    # para estar seguros bajo el límite de 5000
    limite = 4000
    trozos = [
        texto[i:i + limite]
        for i in range(0, len(texto), limite)
    ]

    traductor = GoogleTranslator(
        source='auto',
        target=destino
    )

    traducciones = [
        traductor.translate(t)
        for t in trozos
    ]

    return " ".join(traducciones)


tab1, tab2 = st.tabs([
    "🔗 URL",
    "📁 Subir archivo"
])


# =========================================================
# PESTAÑA 1: URL
# =========================================================

with tab1:
    url = st.text_input(
        "URL del video:",
        placeholder="Pega aquí el enlace del video"
    )

    if st.button(
        "Procesar URL",
        key="procesar_url"
    ):
        with st.spinner("Descargando..."):
            try:
                # Limpieza previa
                for f in glob.glob("/tmp/audio_final*"):
                    os.remove(f)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '/tmp/audio_final',
                    'quiet': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Buscar archivo descargado
                files = glob.glob("/tmp/audio_final*")

                if files:
                    model = whisper.load_model("base")
                    res = model.transcribe(files[0])

                    st.session_state.texto_transcrito = res["text"]

                    os.remove(files[0])

            except Exception as e:
                st.error(f"Error: {e}")


# =========================================================
# PESTAÑA 2: SUBIR ARCHIVO
# =========================================================

with tab2:
    archivo = st.file_uploader(
        "Sube tu archivo (mp4, mp3, wav):",
        type=[
            'mp4',
            'mp3',
            'wav'
        ]
    )

    if archivo is not None:
        if st.button(
            "Transcribir archivo subido",
            key="transcribir_archivo"
        ):
            with st.spinner("Procesando..."):
                path = f"/tmp/{archivo.name}"

                with open(path, "wb") as f:
                    f.write(archivo.getbuffer())

                model = whisper.load_model("base")
                res = model.transcribe(path)

                st.session_state.texto_transcrito = res["text"]

                os.remove(path)


# =========================================================
# VISUALIZACIÓN Y TRADUCCIÓN
# =========================================================

if st.session_state.texto_transcrito:
    st.markdown("""
    <div style="
        margin-top: 28px;
        margin-bottom: 5px;
        color: #84139B;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.4px;
    ">
        RESULTADO
    </div>
    """, unsafe_allow_html=True)

    st.success("¡Transcripción lista!")

    st.text_area(
        "Transcripción original:",
        st.session_state.texto_transcrito,
        height=240
    )

    idioma = st.selectbox(
        "¿Quieres traducirlo?",
        [
            "Ninguno",
            "Español",
            "Inglés",
            "Francés",
            "Italiano",
            "Portugués"
        ]
    )

    if idioma != "Ninguno":
        mapa = {
            "Español": "es",
            "Inglés": "en",
            "Francés": "fr",
            "Italiano": "it",
            "Portugués": "pt"
        }

        with st.spinner(
            "Traduciendo, esto puede tomar un momento..."
        ):
            try:
                traducido = traducir_texto_largo(
                    st.session_state.texto_transcrito,
                    mapa[idioma]
                )

                st.text_area(
                    f"Traducción a {idioma}:",
                    traducido,
                    height=240
                )

            except Exception as e:
                st.error(
                    f"Error en la traducción: {e}"
                )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown("""
<div style="
    text-align: center;
    margin-top: 40px;
    padding-top: 22px;
    border-top: 1px solid rgba(132, 19, 155, 0.12);
    color: #766e79;
    font-size: 12px;
">
    Powered by
    <strong style="color:#84139B;">
        Impulza Digital
    </strong>
</div>
""", unsafe_allow_html=True)
