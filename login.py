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
        st.error(f"\u274c Error al conectar con Firebase: {e}")
        st.stop()

db = firestore.client()

# ---------- DISEÑO Y TEMA ----------
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

modo_oscuro = st.session_state.modo_oscuro

fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
texto = "#ffffff" if modo_oscuro else "#000000"
borde_input = "#ffffff" if modo_oscuro else "#44bba4"

st.markdown(f"""
    <style>
    html, body, .stApp {{
        background-color: {fondo};
        color: {texto};
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow: hidden;
    }}
    .login-container {{
        display: flex;
        height: 100vh;
    }}
    .login-left {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .logo-title {{
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }}
    .logo-title img {{
        width: 60px;
        margin-right: 1rem;
    }}
    .titulo {{
        font-size: 2rem;
        font-weight: bold;
        color: {texto};
    }}
    .boton-verde {{
        background-color: #44bba4 !important;
        color: white !important;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        margin-top: 0.5rem;
    }}
    .tema-btn {{
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 10;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- BOTÓN TEMA ----------
st.markdown("<div class='tema-btn'>", unsafe_allow_html=True)
icono = "💡" if not st.session_state.modo_oscuro else "🔦"
if st.button(f"Tema {icono}"):
    st.session_state.modo_oscuro = not st.session_state.modo_oscuro
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ---------- LOGIN ----------
st.markdown("<div class='login-container'>", unsafe_allow_html=True)
st.markdown("<div class='login-left'>", unsafe_allow_html=True)

# Logo y Título
st.markdown("<div class='logo-title'>", unsafe_allow_html=True)
try:
    logo = Image.open("logobiblioteca.png")
    st.image(logo, width=60, use_container_width=False)
except:
    st.markdown("<p style='color:red;'>Logo no encontrado</p>", unsafe_allow_html=True)

st.markdown("<div class='titulo'>Biblioteca Alejandría</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Título login
st.markdown(f"<h3 style='color:{texto};'>\ud83d\udd10 Iniciar sesión</h3>", unsafe_allow_html=True)

correo = st.text_input("Correo electrónico")
contrasena = st.text_input("Contraseña", type="password")

acceso = False
usuario = None

if st.button("Iniciar sesión", use_container_width=True, type="primary"):
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

cols = st.columns(2)
if cols[0].button("Registrarse", use_container_width=True):
    st.session_state.vista = "registro"
    st.rerun()

if cols[1].button("\u00bfOlvidaste tu contraseña?", use_container_width=True):
    st.session_state.codigo_enviado = False
    st.session_state.codigo_verificacion = ""
    st.session_state.correo_recuperar = ""
    st.session_state.vista = "recuperar"
    st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

return acceso, usuario
