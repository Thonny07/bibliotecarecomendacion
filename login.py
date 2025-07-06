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
    # Estilo según tema
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde_input = "#ffffff" if modo_oscuro else "#44bba4"

    st.markdown(f"""
        <style>
        .fondo {{
            background-color: {fondo};
            color: {texto};
        }}
        .stTextInput input, .stTextArea textarea {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid {borde_input};
            border-radius: 8px;
        }}
        .boton {{
            background-color: #44bba4;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
        }}
        .boton:hover {{
            background-color: #379d8e;
        }}
        </style>
    """, unsafe_allow_html=True)

    col_izq, col_der = st.columns([7, 3])

    with col_izq:
        st.image("portadalogin.png", use_column_width=True)

    with col_der:
        # Botón de tema
        icono = "🔆" if not modo_oscuro else "🌙"
        if st.button(f"{icono} Cambiar tema"):
            st.session_state.modo_oscuro = not modo_oscuro
            st.rerun()

        # Logo y nombre biblioteca
        try:
            logo = Image.open("logobiblioteca.png")
            st.image(logo, width=100)
        except:
            st.warning("⚠️ No se pudo cargar el logo")
        st.markdown("<h2 style='text-align:center;'>Biblioteca Alejandría</h2>", unsafe_allow_html=True)

        # Campos de login
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        acceso = False
        usuario = None

        if st.button("Iniciar sesión", key="login", type="primary"):
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
            if st.button("¿Olvidaste tu contraseña?"):
                st.session_state.codigo_enviado = False
                st.session_state.codigo_verificacion = ""
                st.session_state.correo_recuperar = ""
                st.session_state.vista = "recuperar"
                st.rerun()

    return acceso, usuario
