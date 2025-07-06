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
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde_input = "#ffffff" if modo_oscuro else "#44bba4"
    
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo};
            color: {texto};
            overflow: hidden;
        }}
        .login-container {{
            display: flex;
            height: 100vh;
        }}
        .imagen {{
            flex: 7;
            background-image: url('portadalogin.png');
            background-size: cover;
            background-position: center;
        }}
        .formulario {{
            flex: 3;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            color: {texto};
        }}
        .formulario input {{
            border: 1px solid {borde_input};
            border-radius: 8px;
            padding: 0.5rem;
            width: 100%;
            margin-bottom: 1rem;
            color: {texto};
            background-color: {fondo};
        }}
        .boton {{
            background-color: #44bba4;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
        }}
        .boton:hover {{
            background-color: #379d8e;
        }}
        .tema {{
            position: absolute;
            top: 1rem;
            right: 1rem;
        }}
        </style>
        <div class="login-container">
            <div class="imagen"></div>
            <div class="formulario">
                <div class="tema">
                    <form action="" method="post">
                        <button name="cambiar_tema" class="boton">{'🌞' if not modo_oscuro else '🌙'} Cambiar tema</button>
                    </form>
                </div>
    """, unsafe_allow_html=True)

    # --- Centro visual ---
    try:
        logo = Image.open("logobiblioteca.png")
        st.image(logo, width=80)
    except:
        st.warning("⚠️ No se pudo cargar el logo")
    st.markdown("<h2 style='text-align:center;'>Biblioteca Alejandría</h2>", unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    acceso = False
    usuario = None

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registrarse"):
            st.session_state.vista = "registro"
            st.rerun()
    with col2:
        if st.button("Olvidé mi contraseña"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

    st.markdown("""</div></div>""", unsafe_allow_html=True)
    if st.form_submit_button("cambiar_tema"):
        st.session_state.modo_oscuro = not modo_oscuro
        st.rerun()

    return acceso, usuario
