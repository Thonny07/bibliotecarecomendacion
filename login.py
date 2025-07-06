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

# ---------- LOGIN ----------
def login():
    acceso = False
    usuario = None

    st.markdown("""
        <style>
        body {
            background-color: #e0f4ff;
        }
        .custom-box {
            max-width: 460px;
            margin: 5vh auto;
            background-color: #3bb3d4; /* Fondo del recuadro azul */
            border-radius: 20px;
            padding: 2.5rem 2rem;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }
        .app-name {
            text-align: center;
            font-size: 1.7rem;
            font-weight: bold;
            color: white;
            margin-top: 1rem;
            margin-bottom: 1.8rem;
        }
        .stTextInput input {
            font-size: 0.95rem !important;
            padding: 0.4rem 0.8rem !important;
        }
        .stButton>button {
            width: 100% !important;
            font-size: 0.9rem !important;
            padding: 0.5rem 1rem !important;
            background-color: white;
            color: #3bb3d4;
            border-radius: 10px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)

        # ✅ Mostrar el logo (usa imagen local)
        st.image("logobiblioteca.png", width=120)

        # ✅ Nombre de la biblioteca
        st.markdown('<div class="app-name">Biblioteca Alejandría</div>', unsafe_allow_html=True)

        # Entradas
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        # Botones
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Iniciar sesión"):
                if not correo or not contrasena:
                    st.warning("❌ Campos incompletos")
                else:
                    try:
                        doc = db.collection("usuarios").document(correo).get()
                        if doc.exists:
                            datos = doc.to_dict()
                            if datos["contrasena"] == contrasena:
                                st.success(f"Bienvenido, {datos['nombre']} 👋")
                                acceso = True
                                usuario = datos
                            else:
                                st.error("❌ Contraseña incorrecta")
                        else:
                            st.error("❌ Usuario no encontrado")
                    except Exception:
                        st.error("⚠️ Error al iniciar sesión")
        with col2:
            if st.button("Registrarse"):
                st.session_state.vista = "registro"
                st.rerun()

        st.divider()
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
