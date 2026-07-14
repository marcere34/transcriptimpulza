import glob
import os
import textwrap
import streamlit as st
import whisper
import yt_dlp

from deep_translator import GoogleTranslator


# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="ProTranscribe AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# APARIENCIA SAAS OSCURA — IMPULZA DIGITAL
# =========================================================

st.markdown(
    """
    <style>

    :root {
        --purple: #84139B;
        --yellow: #FFCC00;
        --fuchsia: #CD41C6;
        --black: #070708;
        --dark-card: #121116;
        --dark-card-soft: #19171E;
        --white: #FFFFFF;
        --muted: #A9A3AE;
        --border: rgba(255, 255, 255, 0.10);
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

    /* Fondo general */
    .stApp {
        background:
            radial-gradient(
                circle at 12% 8%,
                rgba(132, 19, 155, 0.28),
                transparent 29%
            ),
            radial-gradient(
                circle at 92% 25%,
                rgba(205, 65, 198, 0.16),
                transparent 26%
            ),
            linear-gradient(
                180deg,
                #08070A 0%,
                #0D0B10 50%,
                #070708 100%
            );
        color: var(--white);
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

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Contenedor principal */
    .block-container {
        max-width: 1080px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Texto general */
    p,
    span,
    label,
    div {
        color: inherit;
    }

    .stMarkdown,
    .stCaption,
    .stText {
        color: var(--white);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    /* Tarjeta general */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(25, 23, 30, 0.95),
                rgba(14, 13, 17, 0.96)
            );
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow:
            0 25px 80px rgba(0, 0, 0, 0.42);
        backdrop-filter: blur(20px);
    }

    /* Etiquetas */
    .stTextInput label,
    .stFileUploader label,
    .stSelectbox label,
    .stTextArea label {
        color: var(--white) !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* Campo URL */
    div[data-baseweb="input"] > div {
        min-height: 56px;
        border-radius: 15px;
        border:
            1px solid rgba(255, 255, 255, 0.12);
        background: #141217;
        transition: all 0.2s ease;
    }

    div[data-baseweb="input"] > div:hover {
        border-color:
            rgba(205, 65, 198, 0.48);
    }

    div[data-baseweb="input"] > div:focus-within {
        border-color: var(--fuchsia);
        box-shadow:
            0 0 0 4px rgba(205, 65, 198, 0.12);
    }

    div[data-baseweb="input"] input {
        color: var(--white) !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #77717E !important;
    }

    /* Selectores */
    div[data-baseweb="select"] > div {
        min-height: 54px;
        border-radius: 15px;
        border:
            1px solid rgba(255, 255, 255, 0.12);
        background: #141217;
        color: var(--white);
    }

    div[data-baseweb="select"] span {
        color: var(--white) !important;
    }

    div[data-baseweb="popover"] {
        color: var(--white);
    }

    ul[role="listbox"] {
        background: #17141B !important;
        border:
            1px solid rgba(255, 255, 255, 0.10);
    }

    li[role="option"] {
        color: var(--white) !important;
    }

    li[role="option"]:hover {
        background:
            rgba(132, 19, 155, 0.28) !important;
    }

    /* Botones principales */
    .stButton > button {
        width: 100%;
        min-height: 56px;
        border:
            1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 15px !important;
        background:
            linear-gradient(
                135deg,
                var(--purple),
                var(--fuchsia)
            ) !important;
        color: var(--white) !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        box-shadow:
            0 16px 38px rgba(132, 19, 155, 0.34);
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            filter 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 20px 45px rgba(132, 19, 155, 0.48);
        filter: brightness(1.08);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Botón descargar */
    .stDownloadButton > button {
        width: 100%;
        min-height: 52px;
        border:
            1px solid var(--yellow) !important;
        border-radius: 14px !important;
        background: var(--yellow) !important;
        color: #151100 !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        box-shadow:
            0 12px 28px rgba(255, 204, 0, 0.20);
        transition: all 0.2s ease;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.04);
        box-shadow:
            0 16px 34px rgba(255, 204, 0, 0.28);
    }

    /* Pestañas */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        padding: 7px;
        border-radius: 17px;
        background:
            rgba(255, 255, 255, 0.045);
        border:
            1px solid rgba(255, 255, 255, 0.07);
    }

    button[data-baseweb="tab"] {
        min-height: 50px;
        border-radius: 12px;
        padding: 11px 22px;
        font-weight: 750;
        color: #AAA4AF;
        background: transparent;
    }

    button[data-baseweb="tab"]:hover {
        color: var(--white);
        background:
            rgba(255, 255, 255, 0.04);
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--yellow) !important;
        background:
            linear-gradient(
                135deg,
                rgba(132, 19, 155, 0.38),
                rgba(205, 65, 198, 0.20)
            );
        box-shadow:
            inset 0 0 0 1px
            rgba(205, 65, 198, 0.22);
    }

    div[data-baseweb="tab-highlight"] {
        display: none;
    }

    /* Subir archivo */
    [data-testid="stFileUploaderDropzone"] {
        min-height: 176px;
        border:
            1.5px dashed
            rgba(205, 65, 198, 0.45);
        border-radius: 19px;
        background:
            linear-gradient(
                145deg,
                rgba(132, 19, 155, 0.10),
                rgba(255, 255, 255, 0.025)
            );
        transition: all 0.2s ease;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--fuchsia);
        background:
            rgba(132, 19, 155, 0.16);
    }

    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] span {
        color: var(--muted) !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        border:
            1px solid rgba(255, 204, 0, 0.60) !important;
        border-radius: 12px !important;
        background:
            rgba(255, 204, 0, 0.08) !important;
        color: var(--yellow) !important;
        font-weight: 750 !important;
    }

    /* Archivo subido */
    [data-testid="stFileUploaderFile"] {
        background: #17151B;
        border:
            1px solid rgba(255, 255, 255, 0.08);
        border-radius: 13px;
        color: var(--white);
    }

    /* Áreas de texto */
    textarea {
        border-radius: 17px !important;
        border:
            1px solid
            rgba(255, 255, 255, 0.12) !important;
        background: #111014 !important;
        color: var(--white) !important;
        line-height: 1.65 !important;
        padding: 16px !important;
    }

    textarea:focus {
        border-color: var(--fuchsia) !important;
        box-shadow:
            0 0 0 4px
            rgba(205, 65, 198, 0.12) !important;
    }

    /* Mensajes y alertas */
    [data-testid="stAlert"] {
        border-radius: 15px;
        border:
            1px solid rgba(255, 255, 255, 0.08);
    }

    /* Spinner */
    [data-testid="stSpinner"] {
        color: var(--yellow);
    }

    /* Separadores */
    hr {
        border-color:
            rgba(255, 255, 255, 0.09) !important;
    }

    /* Texto markdown */
    .stMarkdown p {
        color: var(--muted);
    }

    .stMarkdown strong {
        color: var(--white);
    }

    /* Adaptación móvil */
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
            letter-spacing: -1.3px !important;
        }

        .saas-hero {
            padding: 25px !important;
            border-radius: 21px !important;
        }

        .hero-description {
            font-size: 15px !important;
        }
    }

/* ===== ENCABEZADO SAAS PREMIUM ===== */

.app-shell {
    margin-bottom: 24px;
    padding: 26px 30px 34px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(132,19,155,0.22),
            transparent 26%
        ),
        linear-gradient(
            145deg,
            #151219 0%,
            #0d0b10 100%
        );
    box-shadow:
        0 28px 70px rgba(0,0,0,0.38);
}

.app-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 48px;
}

.brand-box {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-logo {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background:
        linear-gradient(
            135deg,
            #84139B,
            #CD41C6
        );
    color: #ffffff;
    font-size: 20px;
    font-weight: 900;
    box-shadow:
        0 12px 28px rgba(132,19,155,0.32);
}

.brand-name {
    color: #ffffff;
    font-size: 15px;
    font-weight: 800;
}

.brand-by {
    margin-top: 2px;
    color: #8f8995;
    font-size: 11px;
}

.status-box {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    background: rgba(255,255,255,0.035);
    color: #aaa3af;
    font-size: 11px;
    font-weight: 700;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #28c879;
    box-shadow:
        0 0 12px rgba(40,200,121,0.65);
}

.hero-content {
    max-width: 760px;
}

.hero-tag {
    margin-bottom: 15px;
    color: #FFCC00;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1.8px;
}

.hero-content h1 {
    margin: 0;
    max-width: 800px;
    color: #ffffff !important;
    font-size: clamp(38px, 6vw, 64px) !important;
    line-height: 1.02 !important;
    letter-spacing: -3px !important;
    font-weight: 850 !important;
}

.hero-content h1 span {
    color: #FFCC00;
}

.hero-content p {
    max-width: 650px;
    margin: 18px 0 0;
    color: #aaa3af;
    font-size: 16px;
    line-height: 1.65;
}

/* ===== PESTAÑAS MÁS LEGIBLES ===== */

div[data-baseweb="tab-list"] {
    margin-top: 8px;
    padding: 5px;
    border-radius: 14px;
    background: #111015;
    border: 1px solid rgba(255,255,255,0.08);
}

button[data-baseweb="tab"] {
    min-height: 46px;
    padding: 10px 20px;
    color: #a9a3ae !important;
    font-size: 13px;
    font-weight: 750;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    background:
        linear-gradient(
            135deg,
            #84139B,
            #a92ab1
        ) !important;
    box-shadow:
        0 8px 22px rgba(132,19,155,0.30);
}

/* ===== CAMPO URL OSCURO ===== */

div[data-baseweb="input"] > div {
    background: #111015 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
}

div[data-baseweb="input"] input {
    color: #ffffff !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #6e6873 !important;
}

/* ===== BOTÓN MÁS PROFESIONAL ===== */

.stButton > button {
    width: auto !important;
    min-width: 210px;
    padding-left: 24px !important;
    padding-right: 24px !important;
    background:
        linear-gradient(
            135deg,
            #84139B,
            #CD41C6
        ) !important;
    border-radius: 13px !important;
}

/* MÓVIL */

@media (max-width: 700px) {
    .app-shell {
        padding: 20px;
    }

    .app-topbar {
        margin-bottom: 34px;
    }

    .status-box {
        display: none;
    }

    .hero-content h1 {
        font-size: 40px !important;
        letter-spacing: -2px !important;
    }

    .stButton > button {
        width: 100% !important;
    }
}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# ENCABEZADO SAAS OSCURO
# =========================================================

st.markdown(
    """
    <div class="app-shell">
        <div class="app-topbar">
            <div class="brand-box">
                <div class="brand-logo">P</div>

                <div>
                    <div class="brand-name">ProTranscribe AI</div>
                    <div class="brand-by">Impulza Digital</div>
                </div>
            </div>

            <div class="status-box">
                <span class="status-dot"></span>
                Sistema listo
            </div>
        </div>

        <div class="hero-content">
            <div class="hero-tag">TRANSCRIPCIÓN CON IA</div>

            <h1>
                Convierte videos y audios
                <span>en texto</span>
            </h1>

            <p>
                Pega una URL o sube un archivo para transcribirlo
                y traducirlo automáticamente.
            </p>
        </div>
    </div>
    """,
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
        "🔗 Pegar URL",
        "📁 Subir video o audio",
    ]
)


# =========================================================
# PESTAÑA 1: URL
# =========================================================

with tab1:
    url = st.text_input(
        "URL del video:",
        placeholder=(
            "Pega aquí el enlace del video"
        ),
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

                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": "/tmp/audio_final",
                        "quiet": True,
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
                            "No se encontró el archivo "
                            "descargado."
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
            margin-top: 30px;
            padding: 20px 0 8px;
            border-top:
                1px solid
                rgba(255,255,255,0.08);
        ">
            <div style="
                color: #FFCC00;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 1.6px;
                margin-bottom: 6px;
            ">
                RESULTADO
            </div>

            <div style="
                color: #FFFFFF;
                font-size: 27px;
                font-weight: 800;
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
        margin-top: 44px;
        padding-top: 24px;
        border-top:
            1px solid rgba(255,255,255,0.08);
        color: #77717E;
        font-size: 12px;
    ">
        Powered by
        <strong style="
            color: #FFCC00;
        ">
            Impulza Digital
        </strong>
    </div>
    """,
    unsafe_allow_html=True,
)
