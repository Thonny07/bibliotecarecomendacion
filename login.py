import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json  # Necesario para convertir el string del secret

# ---------- CONFIGURACIÓN GENERAL ----------
st.set_page_config(page_title="Iniciar sesión", layout="centered")

# ---------- ESTILO PERSONALIZADO DINÁMICO ----------
st.markdown("""
    <style>
        html, body, [class*="stApp"] {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Segoe UI', sans-serif;
            transition: all 0.3s ease-in-out;
        }
        .login-card {
            background-color: white;
            color: black;
            max-width: 400px;
            width: 100%;
            margin: 5vh auto;
            padding: 3rem 2rem;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
        }
        @media (prefers-color-scheme: dark) {
            .login-card {
                background-color: #1e1e1e;
                color: white;
            }
        }
        .login-title {
            font-size: 1.6rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .login-button button {
            background-color: #4FC3F7;
            color: white;
            border: none;
            padding: 0.6rem;
            border-radius: 8px;
            width: 100%;
            margin-top: 0.5rem;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        .login-button button:hover {
            background-color: #03A9F4;
        }
        .stTextInput>div>input {
            border-radius: 10px;
            padding: 0.5rem;
            text-align: center;
        }
        .forgot-button button {
            background: none !important;
            color: #0288D1;
            font-size: 0.9rem;
            text-decoration: underline;
            border: none;
            margin-top: 1rem;
        }
        hr {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
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
    acceso = False
    usuario = None

    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-title">🔐 Iniciar sesión</div>', unsafe_allow_html=True)

        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                if st.button("Iniciar sesión", key="btn_login"):
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
            with st.container():
                if st.button("Registrarse", key="btn_register"):
                    st.session_state.vista = "registro"
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        if st.button("¿Olvidaste tu contraseña?", key="btn_forgot", type="primary"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
