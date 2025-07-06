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

    # Estilos
    st.markdown("""
        <style>
        .main {
            padding-top: 2rem;
        }
        .custom-box {
            max-width: 460px;
            margin: 5vh auto;
            background-color: #3bb3d4; /* Fondo del recuadro */
            border-radius: 20px;
            padding: 3rem 2rem;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
        }
        .app-name {
            font-size: 1.8rem;
            font-weight: bold;
            color: white;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }
        .stTextInput label {
            color: white;
            font-weight: bold;
        }
        .stTextInput input {
            background-color: white !important;
            color: black !important;
            padding: 0.45rem 0.8rem;
            border-radius: 8px;
            font-size: 0.95rem;
        }
        .logo-img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 10px;
        }
        .stButton>button {
            width: 100% !important;
            font-size: 0.9rem !important;
            padding: 0.6rem 1rem !important;
            background-color: white;
            color: #3bb3d4;
            border-radius: 10px;
            font-weight: bold;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #f0f0f0;
        }
        .secondary-button>button {
            background-color: #3bb3d4 !important;
            color: white !important;
            border: none !important;
        }
        .secondary-button>button:hover {
            background-color: #36a0c2 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)

        # ✅ Logo centrado, circular y grande
        st.markdown(f"""
            <img src="logobiblioteca.png" class="logo-img">
        """, unsafe_allow_html=True)

        # ✅ Nombre de la biblioteca
        st.markdown('<div class="app-name">Biblioteca Alejandría</div>', unsafe_allow_html=True)

        # Inputs
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        # Botones
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                if st.button("Iniciar sesión", key="login_button"):
                    if not correo or not contrasena:
                        st.warning("⚠️ Campos incompletos")
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
            with st.container():
                st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
                if st.button("Registrarse", key="register_button"):
                    st.session_state.vista = "registro"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # Recuperar contraseña
        st.divider()
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        if st.button("¿Olvidaste tu contraseña?", key="forgot_button"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
