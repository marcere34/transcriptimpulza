import base64
import glob
import os
from pathlib import Path

import streamlit as st
import whisper
import yt_dlp

from deep_translator import GoogleTranslator


# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="ProTranscribe AI",
    page_icon="logo_impulza.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CARGAR LOGO
# =========================================================

def cargar_logo_base64():
    carpeta_app = Path(__file__).resolve().parent

    rutas_posibles = [
        carpeta_app / "logo_impulza.png",
        Path.cwd() / "logo_impulza.png",
    ]

    for ruta_logo in rutas_posibles:
        if ruta_logo.is_file():
            return base64.b64encode(
                ruta_logo.read_bytes()
            ).decode("utf-8")

    return ""

logo_base64 = cargar_logo_base64()

# =========================================================
# APARIENCIA SAAS PRO — IMPULZA DIGITAL
# Solo apariencia. No modifica la lógica.
# =========================================================

st.markdown(
    """
    <style>

    :root {
        --purple: #84139B;
        --yellow: #FFCC00;
        --black: #000000;
        --white: #FFFFFF;
        --glass: rgba(8, 8, 10, 0.74);
        --border: rgba(255, 255, 255, 0.12);
    }

    html,
    body,
    [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    /* Fondo principal */
    .stApp {
        background:
            radial-gradient(
                circle at 12% 4%,
                rgba(132, 19, 155, 0.38),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 12%,
                rgba(255, 204, 0, 0.08),
                transparent 20%
            ),
            linear-gradient(
                180deg,
                #050506 0%,
                #080709 55%,
                #020203 100%
            );
        color: var(--white);
    }

    /* Ocultar interfaz visual de Streamlit */
    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Ancho y espacios */
    .block-container {
        max-width: 1120px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;
    }

    /* =========================
       HERO SAAS
       ========================= */

    .pt-hero {
        position: relative;
        overflow: hidden;
        margin-bottom: 26px;
        padding: 36px 38px 42px;
        border: 1px solid var(--border);
        border-radius: 28px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 15, 18, 0.92),
                rgba(3, 3, 4, 0.94)
            );
        box-shadow:
            0 32px 95px rgba(0, 0, 0, 0.58),
            0 0 95px rgba(132, 19, 155, 0.16);
        backdrop-filter: blur(24px);
        text-align: center;
    }

    .pt-hero::before {
        content: "";
        position: absolute;
        top: -220px;
        left: 50%;
        width: 390px;
        height: 390px;
        transform: translateX(-50%);
        border-radius: 50%;
        background: rgba(132, 19, 155, 0.52);
        filter: blur(95px);
        pointer-events: none;
    }

    .pt-hero::after {
        content: "";
        position: absolute;
        right: -80px;
        bottom: -110px;
        width: 230px;
        height: 230px;
        border-radius: 50%;
        background: rgba(255, 204, 0, 0.07);
        filter: blur(65px);
        pointer-events: none;
    }

    .pt-logo-wrap {
        position: relative;
        z-index: 2;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 26px;
    }

    .pt-logo {
        display: block;
        width: min(340px, 78%);
        max-height: 86px;
        object-fit: contain;
        filter:
            drop-shadow(
                0 14px 30px
                rgba(132, 19, 155, 0.34)
            );
    }

    .pt-kicker {
        position: relative;
        z-index: 2;
        display: inline-block;
        margin-bottom: 13px;
        color: var(--yellow);
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .pt-title {
        position: relative;
        z-index: 2;
        max-width: 840px;
        margin: 0 auto;
        color: var(--white);
        font-size:
            clamp(42px, 5.6vw, 66px);
        line-height: 1;
        letter-spacing: -3.2px;
        font-weight: 900;
    }

    .pt-title strong {
        color: var(--yellow);
        font-weight: 900;
    }

    .pt-description {
        position: relative;
        z-index: 2;
        max-width: 690px;
        margin: 19px auto 0;
        color: var(--white);
        font-size: 16px;
        line-height: 1.7;
        opacity: 0.82;
    }

    /* Ondas de audio */
    .pt-wave {
        position: relative;
        z-index: 2;
        height: 45px;
        margin: 28px auto 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
    }

    .pt-wave span {
        width: 4px;
        border-radius: 999px;
        background:
            linear-gradient(
                180deg,
                var(--yellow),
                var(--purple)
            );
        box-shadow:
            0 0 16px
            rgba(132, 19, 155, 0.44);
        animation:
            ptWave 1.35s ease-in-out infinite;
    }

    .pt-wave span:nth-child(1) {
        height: 12px;
        animation-delay: 0.05s;
    }

    .pt-wave span:nth-child(2) {
        height: 24px;
        animation-delay: 0.10s;
    }

    .pt-wave span:nth-child(3) {
        height: 38px;
        animation-delay: 0.15s;
    }

    .pt-wave span:nth-child(4) {
        height: 20px;
        animation-delay: 0.20s;
    }

    .pt-wave span:nth-child(5) {
        height: 44px;
        animation-delay: 0.25s;
    }

    .pt-wave span:nth-child(6) {
        height: 29px;
        animation-delay: 0.30s;
    }

    .pt-wave span:nth-child(7) {
        height: 15px;
        animation-delay: 0.35s;
    }

    .pt-wave span:nth-child(8) {
        height: 33px;
        animation-delay: 0.40s;
    }

    .pt-wave span:nth-child(9) {
        height: 18px;
        animation-delay: 0.45s;
    }

    .pt-wave span:nth-child(10) {
        height: 40px;
        animation-delay: 0.50s;
    }

    .pt-wave span:nth-child(11) {
        height: 22px;
        animation-delay: 0.55s;
    }

    @keyframes ptWave {
        0%,
        100% {
            transform: scaleY(0.55);
            opacity: 0.62;
        }

        50% {
            transform: scaleY(1);
            opacity: 1;
        }
    }

    /* =========================
       PESTAÑAS
       ========================= */

    div[data-baseweb="tab-list"] {
        display: grid !important;
        grid-template-columns:
            1fr 1fr !important;
        gap: 10px !important;
        padding: 7px !important;
        margin-bottom: 20px !important;
        border:
            1px solid var(--border) !important;
        border-radius: 18px !important;
        background:
            rgba(0, 0, 0, 0.56) !important;
        backdrop-filter: blur(18px) !important;
    }

    button[data-baseweb="tab"] {
        width: 100% !important;
        min-height: 52px !important;
        padding: 10px 18px !important;
        border:
            1px solid
            rgba(255, 255, 255, 0.11) !important;
        border-radius: 13px !important;
        background:
            rgba(255, 255, 255, 0.035) !important;
        color: var(--white) !important;
        font-size: 14px !important;
        font-weight: 800 !important;
    }

    button[data-baseweb="tab"] * {
    color: #FFFFFF !important;
    opacity: 1 !important;
    }

    button[data-baseweb="tab"]:hover {
        border-color:
            rgba(255, 204, 0, 0.52) !important;
        background:
            rgba(255, 204, 0, 0.06) !important;
    }

    button[data-baseweb="tab"]
    [aria-selected="true"] {
        color: #090900 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
    border-color: var(--yellow) !important;
    background: var(--yellow) !important;
    color: #090900 !important;
}

button[data-baseweb="tab"][aria-selected="true"] * {
    color: #090900 !important;
    fill: #090900 !important;
}

    /* =========================
       ETIQUETAS
       ========================= */

    .stTextInput label,
    .stFileUploader label,
    .stSelectbox label,
    .stTextArea label {
        color: var(--white) !important;
        font-size: 14px !important;
        font-weight: 800 !important;
    }

    /* =========================
       INPUTS
       ========================= */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        min-height: 56px !important;
        border:
            1px solid
            rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        background:
            rgba(0, 0, 0, 0.62) !important;
        color: var(--white) !important;
        box-shadow:
            inset 0 1px 0
            rgba(255, 255, 255, 0.03) !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color:
            var(--yellow) !important;
        box-shadow:
            0 0 0 3px
            rgba(255, 204, 0, 0.10),
            0 12px 32px
            rgba(0, 0, 0, 0.28) !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] span {
        color: var(--white) !important;
    }

    div[data-baseweb="input"]
    input::placeholder {
        color:
            rgba(255, 255, 255, 0.46) !important;
    }

    ul[role="listbox"] {
        background: #070708 !important;
        border:
            1px solid
            rgba(255, 255, 255, 0.13) !important;
    }

    li[role="option"] {
        color: var(--white) !important;
    }

    li[role="option"]:hover {
        background:
            rgba(132, 19, 155, 0.40) !important;
    }

    /* =========================
       BOTONES GLASS
       ========================= */

    .stButton > button {
        width: 100% !important;
        min-height: 56px !important;
        border:
            1px solid
            rgba(255, 255, 255, 0.22) !important;
        border-radius: 15px !important;
        background:
            linear-gradient(
                135deg,
                rgba(132, 19, 155, 0.96),
                rgba(132, 19, 155, 0.68)
            ) !important;
        color: var(--white) !important;
        font-size: 15px !important;
        font-weight: 900 !important;
        box-shadow:
            inset 0 1px 0
            rgba(255, 255, 255, 0.20),
            0 16px 38px
            rgba(132, 19, 155, 0.34) !important;
        backdrop-filter: blur(18px) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform:
            translateY(-2px) !important;
        border-color:
            var(--yellow) !important;
        background:
            var(--yellow) !important;
        color: #090900 !important;
        box-shadow:
            0 18px 42px
            rgba(255, 204, 0, 0.20) !important;
    }

    .stDownloadButton > button {
        width: 100% !important;
        min-height: 54px !important;
        border:
            1px solid
            var(--yellow) !important;
        border-radius: 15px !important;
        background:
            rgba(255, 204, 0, 0.97) !important;
        color: #090900 !important;
        font-weight: 900 !important;
        box-shadow:
            0 14px 34px
            rgba(255, 204, 0, 0.18) !important;
    }

    /* =========================
       SUBIR ARCHIVO
       ========================= */

    [data-testid="stFileUploaderDropzone"] {
        min-height: 180px !important;
        border:
            1.5px dashed
            rgba(255, 204, 0, 0.52) !important;
        border-radius: 20px !important;
        background:
            radial-gradient(
                circle at center,
                rgba(132, 19, 155, 0.18),
                transparent 66%
            ),
            rgba(0, 0, 0, 0.52) !important;
    }

    [data-testid="stFileUploaderDropzone"]
    small,
    [data-testid="stFileUploaderDropzone"]
    span {
        color: var(--white) !important;
    }

    [data-testid="stFileUploaderDropzone"]
    button {
        border:
            1px solid
            rgba(255, 204, 0, 0.68) !important;
        border-radius: 12px !important;
        background:
            rgba(255, 204, 0, 0.08) !important;
        color: var(--yellow) !important;
        font-weight: 800 !important;
    }

    /* =========================
       TEXTO Y RESULTADOS
       ========================= */

    textarea {
        border:
            1px solid
            rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        background:
            rgba(0, 0, 0, 0.62) !important;
        color: var(--white) !important;
        line-height: 1.7 !important;
        padding: 17px !important;
    }

    textarea:focus {
        border-color:
            var(--yellow) !important;
        box-shadow:
            0 0 0 3px
            rgba(255, 204, 0, 0.10) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 15px !important;
        border:
            1px solid
            rgba(255, 255, 255, 0.12) !important;
    }

    .stMarkdown p,
    [data-testid="stCaptionContainer"] {
        color: var(--white) !important;
    }

    hr {
        border-color:
            rgba(255, 255, 255, 0.10) !important;
    }

    /* =========================
       CELULAR
       ========================= */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 14px;
            padding-right: 14px;
            padding-top: 0.75rem;
        }

        .pt-hero {
            padding: 25px 20px 30px;
            border-radius: 22px;
        }

        .pt-logo {
            width: min(280px, 88%);
        }

        .pt-title {
            font-size: 39px;
            letter-spacing: -2px;
        }

        .pt-description {
            font-size: 15px;
        }

        div[data-baseweb="tab-list"] {
            grid-template-columns:
                1fr !important;
        }
/* Texto de las pestañas */
div[data-testid="stTab"] p {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Pestaña activa */
div[data-testid="stTab"][aria-selected="true"] p {
    color: #FFCC00 !important;
    opacity: 1 !important;
}

/* Pestaña inactiva */
div[data-testid="stTab"][aria-selected="false"] p {
    color: #FFFFFF !important;
    opacity: 1 !important;
}
        
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# ENCABEZADO VISUAL
# =========================================================

logo_html = (
    '<img class="pt-logo" '
    'src="data:image/webp;base64,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" '
    'alt="Impulza Digital">'
)


st.markdown(
    '<section class="pt-hero">'
    f'<div class="pt-logo-wrap">'
    f'{logo_html}'
    f'</div>'
    '<div class="pt-kicker">'
    'TRANSCRIPCIÓN CON INTELIGENCIA ARTIFICIAL'
    '</div>'
    '<div class="pt-title">'
    'ProTranscribe <strong>AI</strong>'
    '</div>'
    '<div class="pt-description">'
    'Convierte videos y audios en texto desde una URL '
    'o subiendo un archivo. Después traduce el resultado '
    'al idioma que necesites.'
    '</div>'
    '<div class="pt-wave">'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '<span></span>'
    '</div>'
    '</section>',
    unsafe_allow_html=True,
)


# =========================================================
# ESTADO ORIGINAL
# =========================================================

if "texto_transcrito" not in st.session_state:
    st.session_state.texto_transcrito = None

if "texto_traducido" not in st.session_state:
    st.session_state.texto_traducido = None


# =========================================================
# FUNCIÓN ORIGINAL DE TRADUCCIÓN
# =========================================================

def traducir_texto_largo(texto, destino):
    limite = 4000

    trozos = [
        texto[i:i + limite]
        for i in range(0, len(texto), limite)
    ]

    traductor = GoogleTranslator(
        source="auto",
        target=destino,
    )

    traducciones = [
        traductor.translate(trozo)
        for trozo in trozos
    ]

    return " ".join(traducciones)


# =========================================================
# PESTAÑAS
# =========================================================

tab1, tab2 = st.tabs(
    [
        "Pegar URL",
        "Subir video o audio",
    ]
)
# =========================================================
# PESTAÑA 1: URL
# =========================================================

with tab1:
    url = st.text_input(
        "URL del video:",
        placeholder="Pega aquí el enlace del video",
    )

    if st.button(
        "Transcribir desde URL",
        key="procesar_url",
    ):
        if not url.strip():
            st.warning(
                "Por favor, ingresa una URL."
            )

        else:
            with st.spinner(
                "Descargando y preparando el video..."
            ):
                try:
                    for archivo_temporal in glob.glob(
                        "/tmp/audio_final*"
                    ):
                        try:
                            os.remove(
                                archivo_temporal
                            )
                        except OSError:
                            pass

                    http_headers = {
                        "User-Agent": (
                            "Mozilla/5.0 "
                            "(Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 "
                            "(KHTML, like Gecko) "
                            "Chrome/126.0.0.0 "
                            "Safari/537.36"
                        ),
                        "Accept-Language": (
                            "es-ES,es;q=0.9,en;q=0.8"
                        ),
                    }

                    if (
                        "facebook.com" in url.lower()
                        or "fb.watch" in url.lower()
                    ):
                        http_headers["Referer"] = (
                            "https://www.facebook.com/"
                        )

                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": "/tmp/audio_final",
                        "quiet": True,
                        "noplaylist": True,
                        "http_headers": http_headers,
                    }

                    with yt_dlp.YoutubeDL(
                        ydl_opts
                    ) as ydl:
                        ydl.download(
                            [url]
                        )

                    archivos = glob.glob(
                        "/tmp/audio_final*"
                    )

                    if archivos:
                        model = whisper.load_model(
                            "base"
                        )

                        resultado = model.transcribe(
                            archivos[0]
                        )

                        st.session_state.texto_transcrito = (
                            resultado["text"]
                        )

                        st.session_state.texto_traducido = None

                        os.remove(
                            archivos[0]
                        )

                    else:
                        st.error(
                            "No se encontró el archivo descargado."
                        )

                except Exception as error:
                    st.error(
                        f"Error: {error}"
                    )
                    # =========================================================
# PESTAÑA 2: SUBIR ARCHIVO
# =========================================================

with tab2:
    archivo = st.file_uploader(
        "Sube tu archivo de video o audio:",
        type=[
            "mp4",
            "mp3",
            "wav",
            "webm",
            "m4a",
            "mov",
        ],
    )

    if archivo is not None:
        if st.button(
            "Transcribir archivo subido",
            key="transcribir_archivo",
        ):
            with st.spinner(
                "Procesando el archivo..."
            ):
                try:
                    path = (
                        f"/tmp/{archivo.name}"
                    )

                    with open(
                        path,
                        "wb",
                    ) as archivo_temporal:
                        archivo_temporal.write(
                            archivo.getbuffer()
                        )

                    model = whisper.load_model(
                        "base"
                    )

                    resultado = model.transcribe(
                        path
                    )

                    st.session_state.texto_transcrito = (
                        resultado["text"]
                    )

                    st.session_state.texto_traducido = None

                    os.remove(
                        path
                    )

                except Exception as error:
                    st.error(
                        f"Error: {error}"
                    )


# =========================================================
# RESULTADO Y TRADUCCIÓN
# =========================================================

if st.session_state.texto_transcrito:
    st.markdown(
        """
        <div style="
            margin-top: 32px;
            padding: 22px 0 10px;
            border-top:
                1px solid
                rgba(255,255,255,0.10);
            text-align: center;
        ">
            <div style="
                color: #FFCC00;
                font-size: 11px;
                font-weight: 900;
                letter-spacing: 1.8px;
                margin-bottom: 7px;
            ">
                RESULTADO
            </div>

            <div style="
                color: #FFFFFF;
                font-size: 28px;
                font-weight: 900;
                letter-spacing: -0.8px;
            ">
                Tu transcripción está lista
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success(
        "La transcripción se completó correctamente."
    )

    texto_actualizado = st.text_area(
        "Transcripción original:",
        value=st.session_state.texto_transcrito,
        height=280,
    )

    st.session_state.texto_transcrito = (
        texto_actualizado
    )

    st.download_button(
        label="Descargar transcripción TXT",
        data=texto_actualizado,
        file_name="transcripcion.txt",
        mime="text/plain",
        use_container_width=True,
    )

    idioma = st.selectbox(
        "¿Quieres traducirlo?",
        [
            "Ninguno",
            "Español",
            "Inglés",
            "Francés",
            "Italiano",
            "Portugués",
        ],
    )

    mapa_idiomas = {
        "Español": "es",
        "Inglés": "en",
        "Francés": "fr",
        "Italiano": "it",
        "Portugués": "pt",
    }

    if idioma != "Ninguno":
        if st.button(
            f"Traducir a {idioma}",
            key="boton_traducir",
        ):
            with st.spinner(
                "Traduciendo el contenido..."
            ):
                try:
                    st.session_state.texto_traducido = (
                        traducir_texto_largo(
                            st.session_state.texto_transcrito,
                            mapa_idiomas[idioma],
                        )
                    )

                except Exception as error:
                    st.error(
                        f"Error en la traducción: {error}"
                    )

    if st.session_state.texto_traducido:
        texto_traducido_editado = st.text_area(
            "Texto traducido:",
            value=(
                st.session_state.texto_traducido
            ),
            height=280,
        )

        st.session_state.texto_traducido = (
            texto_traducido_editado
        )

        st.download_button(
            label="Descargar traducción TXT",
            data=texto_traducido_editado,
            file_name="traduccion.txt",
            mime="text/plain",
            use_container_width=True,
        )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown(
    """
    <div style="
        text-align: center;
        margin-top: 46px;
        padding-top: 24px;
        border-top:
            1px solid
            rgba(255,255,255,0.10);
        color: #FFFFFF;
        font-size: 12px;
        opacity: 0.72;
    ">
        Powered by
        <strong style="
            color: #FFCC00;
            opacity: 1;
        ">
            Impulza Digital
        </strong>
    </div>
    """,
    unsafe_allow_html=True,
)
