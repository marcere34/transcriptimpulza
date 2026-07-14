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
        border-color:
            var(--yellow) !important;
        background:
            var(--yellow) !important;
        color: #090900 !important;
        box-shadow:
            0 12px 30px
            rgba(255, 204, 0, 0.18) !important;
    }

    div[data-baseweb="tab-highlight"] {
        display: none !important;
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
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# ENCABEZADO VISUAL
# =========================================================

logo_html = (
    f'<img class="pt-logo" '
    f'src="data:image/png;base64,{logo_base64}" '
    f'alt="Impulza Digital">'
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

logo_base64 = cargar_logo_base64()

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
