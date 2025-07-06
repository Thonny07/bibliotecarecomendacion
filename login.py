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
        st.error(f"Error al conectar con Firebase: {e}")
        st.stop()

db = firestore.client()

# ---------- TEMA ----------
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

# ---------- APLICAR ESTILOS ----------
def aplicar_estilos():
    modo = st.session_state.modo_oscuro
    fondo = "#1e1e1e" if modo else "#ffffff"
    texto = "#ffffff" if modo else "#000000"
    input_bg = "#2c2c2c" if modo else "#ffffff"
    celeste = "#a2ded0"

    st.markdown(f"""
        <style>
            html, body, .stApp {{
                background-color: {fondo};
                color: {texto};
            }}
            .login-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 90vh;
            }}
            .stTextInput > div > div > input {{
                background-color: {input_bg};
                color: {texto};
                border: 1px solid {celeste};
                border-radius: 10px;
                padding: 0.4em;
                font-size: 14px;
            }}
            .stButton > button {{
                background-color: {celeste};
                color: black;
                border-radius: 10px;
                padding: 0.4em 1.2em;
                margin: 0.3em;
                font-size: 14px;
                border: none;
            }}
            .titulo {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 1em;
                text-align: center;
            }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilos()

# ---------- BOTÓN DE TEMA EN LA ESQUINA SUPERIOR DERECHA ----------
col_espacio, col_boton = st.columns([9, 1])
with col_boton:
    if st.button("🌗", key="toggle_tema"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

# ---------- UI: LOGIN ----------
def login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    try:
        st.image("af2c7156-efd9-4fa6-99d2-e76df7a651aa.png", width=80)
    except:
        st.warning("⚠️ No se pudo cargar el logo.")

    st.markdown('<div class="titulo">Biblioteca Alejandría</div>', unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns(2)
    acceso = False
    usuario = None

    with col1:
        if st.button("Iniciar sesión"):
            doc = db.collection("usuarios").document(correo).get()
            if doc.exists:
                datos = doc.to_dict()
                if datos["contrasena"] == contrasena:
                    st.success(f"Bienvenido, {datos['nombre']}")
                    acceso = True
                    usuario = datos
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.error("Usuario no encontrado")

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

    st.markdown('</div>', unsafe_allow_html=True)
    return acceso, usuario
