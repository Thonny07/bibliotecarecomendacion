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

    # CSS para centrar y limitar ancho real del contenido
    st.markdown("""
        <style>
        body {
            background-color: #e0f4ff;
        }
        .custom-box {
            max-width: 450px;
            margin: 5vh auto;
            background-color: white;
            border-radius: 16px;
            padding: 2rem 2rem;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        }
        @media (prefers-color-scheme: dark) {
            .custom-box {
                background-color: #1e1e1e;
                color: white;
            }
        }
        .login-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #3bb3d4;
        }
        .stTextInput input {
            font-size: 0.95rem !important;
            padding: 0.4rem 0.8rem !important;
        }
        .stButton>button {
            width: 100% !important;
            font-size: 0.9rem !important;
            padding: 0.5rem 1rem !important;
            background-color: #3bb3d4;
            color: white;
            border-radius: 10px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #34a6c4;
        }
        </style>
    """, unsafe_allow_html=True)

    # Contenedor centrado
    with st.container():
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)

        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        # Botones en columnas internas
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Iniciar sesión"):
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
