import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json  # Necesario para convertir el string del secret

# ---------- CONFIGURACIÓN BÁSICA ----------
st.set_page_config(page_title="Login", layout="centered")

# ---------- DETECCIÓN DE MODO OSCURO ----------
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

modo_oscuro = st.session_state.modo_oscuro

# ---------- ESTILOS DINÁMICOS ----------
def aplicar_estilos(modo_oscuro):
    if modo_oscuro:
        bg = "#121212"
        text = "#E0E0E0"
        card = "#1E1E1E"
        input_bg = "#2C2C2C"
        input_border = "#444444"
        accent = "#4FC3F7"
        hover = "#66B2FF"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg = "#F5F7FA"
        text = "#222222"
        card = "#FFFFFF"
        input_bg = "#FFFFFF"
        input_border = "#CCCCCC"
        accent = "#0288D1"
        hover = "#0277BD"
        shadow = "rgba(0, 0, 0, 0.15)"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg};
        color: {text};
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.3s ease-in-out;
    }}
    .stTextInput>div>div>input {{
        background-color: {input_bg};
        color: {text};
        border: 1px solid {input_border};
        border-radius: 10px;
        padding: 10px;
    }}
    .stTextInput>div>div>input::placeholder {{
        color: {text}AA;
    }}
    .stButton>button {{
        background-color: {accent};
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.2s ease;
        box-shadow: 0 4px 10px {shadow};
    }}
    .stButton>button:hover {{
        background-color: {hover};
    }}
    .login-card {{
        background-color: {card};
        padding: 3rem 2rem;
        border-radius: 16px;
        box-shadow: 0 6px 24px {shadow};
        max-width: 420px;
        margin: 6vh auto;
    }}
    .login-title {{
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        color: {text};
    }}
    .forgot-btn > button {{
        background: none !important;
        color: {accent} !important;
        font-size: 0.9rem !important;
        text-decoration: underline;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

aplicar_estilos(modo_oscuro)

# ---------- INICIALIZAR FIREBASE ----------
if not firebase_admin._apps:
    try:
        firebase_config_str = st.secrets["FIREBASE_CONFIG"]
        firebase_config = json.loads(firebase_config_str)

        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"❌ Error al conectar con Firebase: {e}")
        st.stop()

db = firestore.client()

# ---------- FUNCIÓN LOGIN ----------
def login():
    acceso = False
    usuario = None

    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">🔐 Iniciar sesión</div>', unsafe_allow_html=True)

        correo = st.text_input("Correo electrónico", placeholder="ejemplo@correo.com", key="correo_input")
        contrasena = st.text_input("Contraseña", type="password", placeholder="********", key="contrasena_input")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Iniciar sesión"):
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    datos = doc.to_dict()
                    if datos["contrasena"] == contrasena:
                        st.success(f"Bienvenido, {datos['nombre']} 👋")
                        acceso = True
                        usuario = datos
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

        with col2:
            if st.button("Registrarse"):
                st.session_state.vista = "registro"
                st.rerun()

        st.markdown('<div class="forgot-btn">', unsafe_allow_html=True)
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
