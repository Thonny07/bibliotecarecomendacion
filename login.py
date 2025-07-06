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

    # Cargar imagen como base64
    def load_logo_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    logo_base64 = load_logo_base64("logobiblioteca.png")

    # Estilos personalizados
    st.markdown(f"""
        <style>
        .main {{ padding-top: 2rem; }}
        .login-box {{
            max-width: 460px;
            margin: 5vh auto;
            background-color: #ffffff;
            border-radius: 20px;
            padding: 3rem 2rem;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: black;
        }}
        .login-title {{
            background-color: orange;
            padding: 1rem;
            font-size: 1.8rem;
            font-weight: bold;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            color: black;
        }}
        .logo-img {{
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 1rem;
        }}
        .app-name {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #3bb3d4;
            margin-bottom: 2rem;
        }}
        .stTextInput > div > div > input {{
            background-color: #ffffff;
            color: black;
        }}
        .btn-verdeagua > button {{
            background-color: #20c997 !important;
            color: white !important;
            border-radius: 10px;
            font-weight: bold;
            width: 100% !important;
            font-size: 0.95rem;
            padding: 0.6rem 1rem;
            border: none;
        }}
        .btn-verdeagua > button:hover {{
            background-color: #1eb386 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        # ✅ Rectángulo encima del logo (Iniciar sesión) en naranja
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)

        # ✅ Logo centrado, grande y circular
        st.markdown(f'''
            <img class="logo-img" src="data:image/png;base64,{logo_base64}">
        ''', unsafe_allow_html=True)

        # ✅ Nombre de la biblioteca debajo del logo
        st.markdown('<div class="app-name">Biblioteca Alejandría</div>', unsafe_allow_html=True)

        # Campos de ingreso
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        # Botones
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="btn-verdeagua">', unsafe_allow_html=True)
            if st.button("Iniciar sesión", key="btn_login"):
                if not correo or not contrasena:
                    st.warning("⚠️ Campos incompletos")
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
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="btn-verdeagua">', unsafe_allow_html=True)
            if st.button("Registrarse", key="btn_register"):
                st.session_state.vista = "registro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        st.markdown('<div class="btn-verdeagua">', unsafe_allow_html=True)
        if st.button("¿Olvidaste tu contraseña?", key="btn_forgot"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
