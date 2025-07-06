import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

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

def login():
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    verde_agua = "#44bba4"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde = "#ffffff" if modo_oscuro else "#44bba4"

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-image: url('fondologin.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            overflow: hidden;
            height: 100vh;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
        }}

        .login-card {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 40px 30px;
            max-width: 400px;
            width: 100%;
            margin: auto;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
            text-align: center;
        }}

        .stTextInput input {{
            border: 1px solid {borde};
            border-radius: 8px;
            padding: 10px;
            color: {texto};
            background-color: white;
        }}

        .stButton > button {{
            background-color: {verde_agua};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }}

        .stButton > button:hover {{
            background-color: #379d8e;
        }}

        .theme-button {{
            position: absolute;
            top: 20px;
            right: 30px;
        }}

        .login-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Botón de tema (arriba derecha)
    st.markdown('<div class="theme-button">', unsafe_allow_html=True)
    icono = "💡" if not modo_oscuro else "🔦"
    if st.button(icono, key="tema_login"):
        st.session_state.modo_oscuro = not modo_oscuro
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-wrapper"><div class="login-card">', unsafe_allow_html=True)

    try:
        st.image("logobiblioteca.png", width=80)
    except:
        st.warning("No se pudo cargar el logo")

    st.markdown("<h3 style='color:#000000;'>Biblioteca Alejandría</h3>", unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

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

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

    with col_b:
        if st.button("Registrarse"):
            st.session_state.vista = "registro"
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)
    return acceso, usuario
