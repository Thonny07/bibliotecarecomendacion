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
    verde_agua = "#44bba4"
    fondo_derecha = "#ffffff"
    texto = "#000000"
    degradado = "linear-gradient(to right, #6a11cb, #2575fc)"

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        .container {{
            display: flex;
            height: 100vh;
            width: 100vw;
        }}
        .left {{
            flex: 1.3;
        }}
        .left img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .right {{
            flex: 1;
            background-color: {fondo_derecha};
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .form-box {{
            width: 100%;
            max-width: 350px;
            text-align: center;
        }}
        .form-box h3 {{
            margin-bottom: 25px;
            color: {texto};
        }}
        .stTextInput input {{
            background-color: #f4f4f4;
            border: 1px solid #ccc;
            border-radius: 30px;
            padding: 12px 15px;
            width: 100%;
        }}
        .stButton > button {{
            background-image: {degradado};
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 30px;
            padding: 10px;
            width: 100%;
            margin-top: 10px;
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
            top: 15px;
            right: 25px;
            z-index: 9999;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Botón tema arriba a la derecha
    st.markdown('<div class="theme-button">', unsafe_allow_html=True)
    icono = "💡" if not st.session_state.get("modo_oscuro", False) else "🔦"
    if st.button(icono, key="tema_btn"):
        st.session_state.modo_oscuro = not st.session_state.get("modo_oscuro", False)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # CONTENEDOR COMPLETO
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Columna izquierda (imagen)
    st.markdown('<div class="left">', unsafe_allow_html=True)
    try:
        st.image("portadalogin.png", use_column_width=True)
    except:
        st.warning("⚠️ No se pudo cargar la imagen")
    st.markdown('</div>', unsafe_allow_html=True)

    # Columna derecha (formulario)
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

    # Línea inferior: Remember / Olvidaste
    st.markdown("""
        <div class="extras">
            <span>Remember</span>
            <span style="cursor:pointer; color:#2575fc;" onclick="document.querySelector('button[data-testid=stButton]:nth-of-type(2)').click()">Forget password?</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("¿Olvidaste tu contraseña?", key="olvido"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    if st.button("Registrarse", key="registro"):
        st.session_state.vista = "registro"
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)  # Cierra form-box y right
    st.markdown('</div>', unsafe_allow_html=True)        # Cierra container

    return acceso, usuario
