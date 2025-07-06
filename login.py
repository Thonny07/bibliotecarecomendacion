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
    st.set_page_config(layout="wide")  # Pantalla completa

    st.markdown("""
    <style>
    html, body, .stApp {
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow: hidden;
        font-family: 'Segoe UI', sans-serif;
    }

    .container {
        display: flex;
        width: 100vw;
        height: 100vh;
    }

    .left {
        flex: 6;
        background: linear-gradient(to right, #7b2ff7, #f107a3);
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 40px;
        text-align: center;
    }

    .left h1 {
        font-size: 36px;
        margin-bottom: 10px;
    }

    .left p {
        font-size: 16px;
        max-width: 400px;
    }

    .right {
        flex: 4;
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .form-box {
        width: 100%;
        max-width: 350px;
        text-align: center;
    }

    .form-box h3 {
        margin-bottom: 25px;
        font-weight: 600;
        color: #333;
    }

    .stTextInput input {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 25px;
        padding: 12px 20px;
        width: 100%;
    }

    .stButton > button {
        background: linear-gradient(to right, #7b2ff7, #f107a3);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 10px;
        width: 100%;
        margin-top: 15px;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #651ee0, #c9068e);
    }

    .extra-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }

    .extra-buttons button {
        font-size: 13px;
    }

    .theme-btn {
        position: absolute;
        top: 10px;
        right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Botón de cambio de tema arriba a la derecha
    st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
    icono = "💡" if not st.session_state.get("modo_oscuro", False) else "🔦"
    if st.button(icono, key="tema_btn"):
        st.session_state.modo_oscuro = not st.session_state.get("modo_oscuro", False)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Contenedor principal
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Lado izquierdo con mensaje de bienvenida
    st.markdown("""
        <div class="left">
            <h1>Welcome to website</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.</p>
        </div>
    """, unsafe_allow_html=True)

    # Lado derecho: formulario de login
    st.markdown('<div class="right"><div class="form-box">', unsafe_allow_html=True)

    st.markdown("<h3>USER LOGIN</h3>", unsafe_allow_html=True)

    correo = st.text_input("", placeholder="Correo electrónico")
    contrasena = st.text_input("", placeholder="Contraseña", type="password")

    acceso = False
    usuario = None

    if st.button("Login"):
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

    st.markdown('</div></div>', unsafe_allow_html=True)  # Cierra form-box y right
    st.markdown('</div>', unsafe_allow_html=True)  # Cierra container

    return acceso, usuario
