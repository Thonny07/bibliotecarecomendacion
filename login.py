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
    texto = "#000000"
    degradado = "linear-gradient(to right, #6a11cb, #2575fc)"  # Azul degradado
    borde = "#44bba4"

    st.markdown(f"""
    <style>
    html, body, .stApp {{
        background-image: url('fondologin.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        overflow: hidden;
        height: 100vh;
    }}

    .login-card {{
        width: 400px;
        margin: auto;
        margin-top: 50px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0,0,0,0.3);
        font-family: 'Segoe UI', sans-serif;
    }}

    .top-section {{
        background: linear-gradient(to bottom, #6a11cb, #2575fc);
        padding: 30px;
        color: white;
        text-align: center;
    }}

    .top-section h2 {{
        margin: 0;
        font-size: 26px;
    }}

    .top-section p {{
        font-size: 14px;
        margin-top: 10px;
    }}

    .bottom-section {{
        background: white;
        padding: 30px;
        text-align: center;
    }}

    .bottom-section h3 {{
        color: #333;
        margin-bottom: 20px;
    }}

    .stTextInput input {{
        padding: 10px;
        border-radius: 30px;
        border: 1px solid #ccc;
        background-color: #f1f1f1;
        width: 100%;
        color: black;
    }}

    .stButton > button {{
        width: 100%;
        padding: 10px 20px;
        border-radius: 30px;
        background-image: {degradado};
        color: white;
        font-weight: bold;
        border: none;
    }}

    .stButton > button:hover {{
        background-image: linear-gradient(to right, #5b0eb3, #1f63e0);
    }}

    .extras {{
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        font-size: 13px;
        color: #555;
    }}

    .theme-button {{
        position: absolute;
        top: 20px;
        right: 30px;
        z-index: 9999;
    }}

    </style>
    """, unsafe_allow_html=True)

    # Botón tema arriba a la derecha
    st.markdown('<div class="theme-button">', unsafe_allow_html=True)
    icono = "💡" if not modo_oscuro else "🔦"
    if st.button(icono, key="tema_login"):
        st.session_state.modo_oscuro = not modo_oscuro
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Tarjeta de login
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="top-section">
        <h2>HELLO & WELCOME</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.</p>
    </div>
    <div class="bottom-section">
    """, unsafe_allow_html=True)

    st.markdown("<h3>USER LOGIN</h3>", unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico", label_visibility="collapsed", placeholder="Usuario")
    contrasena = st.text_input("Contraseña", type="password", label_visibility="collapsed", placeholder="Contraseña")

    acceso = False
    usuario = None

    if st.button("LOGIN"):
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

    st.markdown("""
        <div class="extras">
            <span>¿Recordarme?</span>
            <span style="cursor:pointer; color:#2575fc;" onclick="document.querySelector('button[data-testid=stButton]').click()">¿Olvidaste tu contraseña?</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("¿Olvidaste tu contraseña?", key="hidden_recuperar", help="Este botón es invisible", disabled=True):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    if st.button("Registrarse"):
        st.session_state.vista = "registro"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    return acceso, usuario
