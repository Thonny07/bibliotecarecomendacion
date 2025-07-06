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
        </style>
    """, unsafe_allow_html=True)

    # Botón de tema arriba derecha
    col_tema = st.columns([9, 1])[1]
    with col_tema:
        icono = "💡" if not modo_oscuro else "🔦"
        if st.button(f"{icono}", key="tema_login"):
            st.session_state.modo_oscuro = not modo_oscuro
            st.rerun()

    # Pantalla dividida
    col1, col2 = st.columns([7, 3])

    with col1:
        try:
            st.image("portadalogin.png", use_container_width=True)
        except:
            st.warning("No se pudo cargar la imagen")

    with col2:
        st.markdown(f"<div style='height: 95vh; display: flex; flex-direction: column; justify-content: center; align-items: center;'>", unsafe_allow_html=True)

        try:
            st.image("logobiblioteca.png", width=80)
        except:
            st.warning("No se pudo cargar el logo")

        st.markdown(f"<h2 style='text-align: center; color: {texto}; margin-bottom: 30px;'>Biblioteca Alejandría</h2>", unsafe_allow_html=True)

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

        st.markdown("</div>", unsafe_allow_html=True)

        return acceso, usuario
