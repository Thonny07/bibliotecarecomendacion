import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Inicializar Firebase
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

def login():
    # Configuración
    verde_agua = "#44bba4"
    fondo = "#ffffff"
    texto = "#000000"

    st.set_page_config(layout="wide")  # Pantalla completa

    st.markdown(f"""
    <style>
    html, body, .stApp {{
        height: 100vh;
        overflow: hidden;
        margin: 0;
        padding: 0;
        background-color: {fondo};
        color: {texto};
        font-family: 'Segoe UI', sans-serif;
    }}

    .centered {{
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}

    .form-box {{
        width: 100%;
        max-width: 350px;
        text-align: center;
        padding: 30px;
    }}

    .form-box h3 {{
        margin-top: 10px;
        margin-bottom: 25px;
        color: {texto};
    }}

    .stTextInput input {{
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 30px;
        padding: 12px 15px;
        width: 100%;
    }}

    .stButton > button {{
        background-color: {verde_agua};
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 30px;
        padding: 10px;
        width: 100%;
        margin-top: 10px;
    }}

    .stButton > button:hover {{
        background-color: #379d8e;
    }}

    .extra-buttons {{
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }}

    .theme-button {{
        position: absolute;
        top: 15px;
        right: 25px;
        z-index: 9999;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Botón de tema
    st.markdown('<div class="theme-button">', unsafe_allow_html=True)
    icono = "💡" if not st.session_state.get("modo_oscuro", False) else "🔦"
    if st.button(icono, key="tema_btn"):
        st.session_state.modo_oscuro = not st.session_state.get("modo_oscuro", False)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Centro absoluto
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-box">', unsafe_allow_html=True)

        try:
            st.image("logobiblioteca.png", width=100)
        except:
            st.warning("⚠️ No se pudo cargar el logo")

        st.markdown("<h3>USER LOGIN</h3>", unsafe_allow_html=True)

        correo = st.text_input("", placeholder="Correo electrónico")
        contrasena = st.text_input("", placeholder="Contraseña", type="password")

        acceso = False
        usuario = None

        if st.button("Iniciar sesión"):
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

        col1, col2 = st.columns(2)
        with col1:
            if st.button("¿Olvidaste tu contraseña?"):
                st.session_state.codigo_enviado = False
                st.session_state.codigo_verificacion = ""
                st.session_state.correo_recuperar = ""
                st.session_state.vista = "recuperar"
                st.rerun()

        with col2:
            if st.button("Registrarse"):
                st.session_state.vista = "registro"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # cierra form-box

    st.markdown('</div>', unsafe_allow_html=True)  # cierra centered

    return acceso, usuario
