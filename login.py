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
    degradado = "linear-gradient(to right, #6a11cb, #2575fc)"
    texto = "#000000"
    
    # ✅ Ajustar fondo con ruta local de Streamlit (usa la imagen desde carpeta)
    fondo_path = "fondologin.jpg"

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-image: url('{fondo_path}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }}

        .center-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}

        .login-card {{
            width: 400px;
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

    # Botón de tema
    st.markdown('<div class="theme-button">', unsafe_allow_html=True)
    icono = "💡" if not modo_oscuro else "🔦"
    if st.button(icono, key="tema_login"):
        st.session_state.modo_oscuro = not modo_oscuro
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Contenedor centrado
    st.markdown('<div class="center-container"><div class="login-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="top-section">
        <h2>HELLO & WELCOME</h2>
        <p>Bienvenido al sistema. Ingresa tus datos para continuar.</p>
    </div>
    <div class="bottom-section">
    """, unsafe_allow_html=True)

    st.markdown("<h3>USER LOGIN</h3>", unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico", label_visibility="collapsed", placeholder="Correo")
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

    st.markdown("</div></div></div>", unsafe_allow_html=True)

    return acceso, usuario
