import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from PIL import Image

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

# Aplicar estilos según tema
modo_oscuro = st.session_state.get("modo_oscuro", False)
fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
texto = "#ffffff" if modo_oscuro else "#000000"
borde_input = "#ffffff" if modo_oscuro else "#44bba4"

st.markdown(f"""
    <style>
    html, body, .stApp {{
        background-color: {fondo};
        color: {texto};
    }}
    .login-container {{
        display: flex;
        height: 100vh;
    }}
    .left-img {{
        flex: 7;
        background-image: url('portadalogin.png');
        background-size: cover;
        background-position: center;
    }}
    .right-panel {{
        flex: 3;
        padding: 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: {fondo};
        color: {texto};
    }}
    .theme-button {{
        position: absolute;
        top: 20px;
        right: 30px;
    }}
    input[type="text"], input[type="password"] {{
        width: 100%;
        padding: 10px;
        margin-bottom: 12px;
        border-radius: 8px;
        border: 1px solid {borde_input};
        background-color: {fondo};
        color: {texto};
    }}
    .btn {{
        background-color: #44bba4;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        width: 100%;
        margin-top: 8px;
    }}
    .btn:hover {{
        background-color: #379d8e;
    }}
    .small-buttons {{
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        width: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# Botón de tema en esquina superior derecha
icono = "🔆" if not modo_oscuro else "🌙"
if st.button(f"{icono} Cambiar tema", key="toggle_tema", help="Cambiar entre modo claro y oscuro"):
    st.session_state.modo_oscuro = not modo_oscuro
    st.rerun()

# Contenido en dos columnas: imagen izquierda, login derecha
st.markdown("<div class='login-container'>", unsafe_allow_html=True)

# Imagen a la izquierda
st.markdown("<div class='left-img'></div>", unsafe_allow_html=True)

# Panel derecho (formulario)
st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

# Logo y título
try:
    logo = Image.open("logobiblioteca.png")
    st.image(logo, width=80)
except:
    st.warning("⚠️ No se pudo cargar el logo")
st.markdown("<h2 style='text-align: center;'>Biblioteca Alejandría</h2>", unsafe_allow_html=True)

# Formulario
correo = st.text_input("Correo electrónico")
contrasena = st.text_input("Contraseña", type="password")

acceso = False
usuario = None

if st.button("Iniciar sesión", key="iniciar", help="Iniciar sesión con tus credenciales", type="primary"):
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

# Botones pequeños debajo
col1, col2 = st.columns(2)
with col1:
    if st.button("Registrarse", key="registro"):
        st.session_state.vista = "registro"
        st.rerun()
with col2:
    if st.button("¿Olvidaste tu contraseña?", key="recuperar"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # Cierre panel derecho
st.markdown("</div>", unsafe_allow_html=True)  # Cierre contenedor principal

return acceso, usuario
