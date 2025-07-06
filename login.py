import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

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

# ---------- TEMA ----------
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

# Aplicar estilo según el tema
if st.session_state.modo_oscuro:
    bg_color = "#1e1e1e"
    text_color = "white"
    input_bg = "#2c2c2c"
    border_color = "#5adcec"
else:
    bg_color = "white"
    text_color = "black"
    input_bg = "#ffffff"
    border_color = "#5adcec"

st.markdown(f"""
    <style>
        html, body, .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stTextInput input, .stTextArea textarea {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px;
            font-size: 14px !important;
        }}
        .stButton button {{
            background-color: {border_color} !important;
            color: black !important;
            border-radius: 8px;
            padding: 0.3em 1em;
            font-size: 14px;
        }}
        .titulo-login {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 0.5em;
        }}
        .login-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
        }}
    </style>
""", unsafe_allow_html=True)

# ---------- UI ----------
col_logo, col_tema = st.columns([8, 1])

with col_tema:
    if st.button("Tema 💡", key="toggle_tema"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

st.markdown('<div class="login-container">', unsafe_allow_html=True)

# Mostrar logo
st.image("af2c7156-efd9-4fa6-99d2-e76df7a651aa.png", width=80)

st.markdown('<div class="titulo-login">Biblioteca Alejandría</div>', unsafe_allow_html=True)
st.markdown("### 🔐 Iniciar sesión")

# ---------- LOGIN ----------
def login():
    correo = st.text_input("Correo electrónico", key="correo_login")
    contrasena = st.text_input("Contraseña", type="password", key="clave_login")

    col1, col2 = st.columns([1, 1])
    acceso = False
    usuario = None

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

    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    return acceso, usuario
