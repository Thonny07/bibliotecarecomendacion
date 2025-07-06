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

    # Cargar logo como base64
    def load_logo_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    logo_base64 = load_logo_base64("logobiblioteca.png")

    # Estilos personalizados
    st.markdown(f"""
        <style>
        .main {{ padding-top: 2rem; }}
        .logo-img {{
            display: block;
            margin: 0 auto 1rem auto;
            width: 160px;
            height: 160px;
            border-radius: 50%;
            object-fit: cover;
        }}
        .app-name {{
            text-align: center;
            font-size: 1.8rem;
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
            margin-top: 0.4rem;
        }}
        .btn-verdeagua > button:hover {{
            background-color: #1eb386 !important;
        }}
        .column-btns {{
            gap: 10px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Logo y nombre
    st.markdown(f'<img class="logo-img" src="data:image/png;base64,{logo_base64}">', unsafe_allow_html=True)
    st.markdown('<div class="app-name">Biblioteca Alejandría</div>', unsafe_allow_html=True)

    # Campos
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    # Botones en columnas
    col1, col2 = st.columns([1, 1], gap="small")
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

    # Botón de recuperar contraseña
    st.markdown('<div class="btn-verdeagua" style="margin-top: 0.8rem;">', unsafe_allow_html=True)
    if st.button("¿Olvidaste tu contraseña?", key="btn_forgot"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
