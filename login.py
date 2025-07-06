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

    # ---------- CSS PERSONALIZADO ----------
    st.markdown("""
        <style>
        /* Eliminar headers y toolbars */
        header, footer, .block-container {
            visibility: hidden !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Contenedor principal con margen superior eliminado */
        .main {
            padding-top: 0rem !important;
        }

        /* Caja del formulario */
        .login-container {
            background-color: white;
            border-radius: 20px;
            padding: 2rem 2.5rem;
            max-width: 420px;
            margin: 3rem auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
        }

        @media (prefers-color-scheme: dark) {
            .login-container {
                background-color: #1e1e1e;
                color: white;
            }
            input, textarea {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #777 !important;
            }
        }

        .logo-img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            display: block;
            margin: 0 auto 1rem auto;
        }

        .login-title {
            font-size: 1.7rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            color: #20c997;
        }

        label {
            color: black !important;
            font-weight: 500;
        }

        @media (prefers-color-scheme: dark) {
            label {
                color: white !important;
            }
        }

        .stButton>button {
            background-color: #20c997;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
            width: 100%;
        }

        .stButton>button:hover {
            background-color: #17a88b;
        }

        .stTextInput>div>div>input {
            border-radius: 8px !important;
        }

        .warning-text {
            color: black !important;
            font-weight: bold;
        }

        @media (prefers-color-scheme: dark) {
            .warning-text {
                color: white !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- CONTENEDOR PRINCIPAL ----------
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # ---------- LOGO ----------
    try:
        with open("logobiblioteca.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f'<img src="data:image/png;base64,{encoded}" class="logo-img">',
                unsafe_allow_html=True
            )
    except:
        st.warning("⚠️ No se pudo cargar el logo.")

    # ---------- TÍTULO ----------
    st.markdown('<div class="login-title">Biblioteca Alejandría</div>', unsafe_allow_html=True)

    # ---------- CAMPOS ----------
    correo = st.text_input("Correo electrónico", key="correo")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena")

    # ---------- BOTONES ----------
    col1, col2 = st.columns(2)
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

    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return acceso, usuario
