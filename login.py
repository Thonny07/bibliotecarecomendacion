import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from PIL import Image

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
    st.markdown("""
        <style>
        .login-container {
            display: flex;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }
        .left-panel {
            width: 65%;
            background-color: #a2ded0;
        }
        .right-panel {
            width: 35%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .logo {
            width: 80px;
            margin-bottom: 1rem;
        }
        .titulo {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .login-form {
            width: 100%;
            max-width: 350px;
        }
        .verde-agua {
            background-color: #44bba4 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-container">
        <div class="left-panel"></div>
        <div class="right-panel">
            <img src="https://raw.githubusercontent.com/tuusuario/tu-repo/main/logobiblioteca.png" class="logo" />
            <div class="titulo">Biblioteca Alejandría</div>
            <div class="login-form">
    """, unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    cols = st.columns([1, 1])
    acceso = False
    usuario = None

    with cols[0]:
        if st.button("Iniciar sesión", type="primary"):
            doc = db.collection("usuarios").document(correo).get()
            if doc.exists:
                datos = doc.to_dict()
                if datos["contrasena"] == contrasena:
                    st.success(f"Bienvenido, {datos['nombre']}")
                    acceso = True
                    usuario = datos
                else:
                    st.error("❌ Contraseña incorrecta")
            else:
                st.error("❌ Usuario no encontrado")

    with cols[1]:
        if st.button("Registrarse"):
            st.session_state.vista = "registro"
            st.rerun()

    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return acceso, usuario
