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
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde = "#ffffff" if modo_oscuro else "#44bba4"
    verde_agua = "#44bba4"

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo};
            color: {texto};
            overflow: hidden;
        }}
        .stTextInput input, .stTextArea textarea {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid {borde};
            border-radius: 8px;
        }}
        .stButton > button {{
            background-color: {verde_agua};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: bold;
        }}
        .stButton > button:hover {{
            background-color: #379d8e;
        }}
        .login-container {{
            display: flex;
            flex-direction: row;
            height: 100vh;
            overflow: hidden;
        }}
        .left-side {{
            width: 70%;
        }}
        .right-side {{
            width: 30%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 30px;
        }}
        .theme-button {{
            position: absolute;
            top: 20px;
            right: 30px;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Contenedor externo
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Columna izquierda - Imagen
    with st.container():
        st.markdown('<div class="left-side">', unsafe_allow_html=True)
        try:
            st.image("portadalogin.png", use_container_width=True)
        except:
            st.warning("No se pudo cargar la imagen")
        st.markdown('</div>', unsafe_allow_html=True)

    # Columna derecha - Login y logo
    with st.container():
        st.markdown('<div class="right-side">', unsafe_allow_html=True)

        # Botón de tema (arriba derecha)
        st.markdown('<div class="theme-button">', unsafe_allow_html=True)
        icono = "💡" if not modo_oscuro else "🔦"
        if st.button(f"{icono}", key="tema_login"):
            st.session_state.modo_oscuro = not modo_oscuro
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        try:
            st.image("logobiblioteca.png", width=80)
        except:
            st.warning("No se pudo cargar el logo")

        st.markdown(f"<h2 style='text-align: center; color: {texto}; margin: 20px 0;'>Biblioteca Alejandría</h2>", unsafe_allow_html=True)

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

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return acceso, usuario
