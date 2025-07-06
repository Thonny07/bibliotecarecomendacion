import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ---------- CONFIGURACIÓN DE PÁGINA Y ESTILO ----------
st.set_page_config(page_title="Login", layout="centered")

# Fondo celeste claro y ocultar barra de scroll
st.markdown("""
    <style>
        body {
            background-color: #E0F7FA;
            overflow: hidden;
        }
        .login-box {
            background-color: white;
            padding: 3rem 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 360px;
            margin: auto;
            margin-top: 50px;
            text-align: center;
        }
        .login-logo {
            width: 80px;
            margin-bottom: 1rem;
        }
        .stButton>button {
            width: 100%;
            margin-top: 0.5rem;
            background-color: #0288D1;
            color: white;
        }
        .stTextInput>div>input {
            text-align: center;
        }
        .small-button > button {
            background-color: #B3E5FC !important;
            color: #000 !important;
        }
    </style>
""", unsafe_allow_html=True)

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

# ---------- LOGIN ----------
def login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    # Logo (puedes cambiar por tu imagen con st.image)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Generic_Login_Icon.svg/1200px-Generic_Login_Icon.svg.png", width=80)

    # Nombre o título
    st.markdown("### Bienvenido")

    # Inputs
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    acceso = False
    usuario = None

    # Botones
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
