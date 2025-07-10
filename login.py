import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64

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
    acceso = False
    usuario = None

    st.markdown("""
        <style>
        /* OCULTAR HEADERS Y RECTÁNGULOS RESIDUALES */
        header, footer {
            visibility: hidden !important;
            height: 0px !important;
        }

        /* ESTA CLASE ES LA QUE CREA ESE RECTÁNGULO NEGRO SUPERIOR */
        .css-18ni7ap.e8zbici2, .css-1avcm0n.e8zbici2, .css-1dp5vir.e1tzin5v1 {
            background-color: transparent !important;
            box-shadow: none !important;
            height: 0px !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
        }

        /* CONTENEDOR PRINCIPAL */
        .login-container {
            background-color: white;
            border-radius: 20px;
            padding: 2.5rem;
            max-width: 450px;
            margin: 3rem auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
        }

        @media (prefers-color-scheme: dark) {
            .login-container {
                background-color: #1e1e1e;
                color: white;
            }
            input {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #777 !important;
            }
        }

        /* LOGO */
        .logo-img {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            display: block;
            margin: 0 auto 1rem auto;
        }

        /* TÍTULO */
        .login-title {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            color: #20c997;
        }

        /* BOTONES */
        .stButton>button {
            background-color: #20c997;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
            width: 100%;
        }

        .stButton>button:hover {
            background-color: #17a88b;
            color: white;
        }

        /* ETIQUETAS */
        label {
            color: black !important;
            font-weight: bold;
        }

        /* MENSAJE CAMPOS INCOMPLETOS */
        .warning-text {
            color: black !important;
            font-weight: bold;
        }

        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    try:
        with open("logobiblioteca.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f'<img src="data:image/png;base64,{encoded}" class="logo-img">',
                unsafe_allow_html=True
            )
    except:
        st.warning("⚠️ No se pudo cargar el logo.")

    st.markdown('<div class="login-title">Biblioteca Alexandrina</div>', unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico", key="correo")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Iniciar sesión"):
            if not correo or not contrasena:
                st.markdown('<p class="warning-text">⚠️ Campos incompletos</p>', unsafe_allow_html=True)
            else:
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

    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return acceso, usuario
