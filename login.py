import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64

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

    # ---------- CSS personalizado ----------
    st.markdown("""
        <style>
        /* Quitar espacios externos y fondo del body */
        .main, .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            background-color: white !important;
        }
        header {visibility: hidden;}
        
        .login-container {
            background-color: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 2.5rem;
            max-width: 450px;
            margin: 2rem auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
        }
        @media (prefers-color-scheme: dark) {
            .login-container {
                background-color: #1e1e1e;
                color: white;
            }
            input {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #777 !important;
            }
        }
        .login-title {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            color: #20c997;
        }
        .stButton>button {
            background-color: #20c997;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #1aa179;
            color: white;
        }
        label {
            color: black !important;
            font-weight: bold;
        }
        .warning-text {
            color: black !important;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Contenedor principal ----------
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # ---------- Logo centrado ----------
    try:
        with open("logobiblioteca.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <img src="data:image/png;base64,{encoded}" 
                     style="width: 130px; height: 130px; border-radius: 50%; margin-bottom: 1rem; display: block; margin-left: auto; margin-right: auto;">
                """,
                unsafe_allow_html=True
            )
    except Exception:
        st.warning("⚠️ No se pudo cargar el logo. Verifica la ruta y el nombre del archivo.")

    # ---------- Título ----------
    st.markdown('<div class="login-title">Biblioteca Alejandría</div>', unsafe_allow_html=True)

    # ---------- Campos de entrada ----------
    correo = st.text_input("Correo electrónico", key="correo")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena")

    # ---------- Botones ----------
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Iniciar sesión"):
            if not correo or not contrasena:
                st.markdown('<p class="warning-text">⚠️ Campos incompletos</p>', unsafe_allow_html=True)
            else:
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

    # ---------- Cambiar contraseña ----------
    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return acceso, usuario
