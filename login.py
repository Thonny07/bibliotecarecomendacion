import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

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

    # ---- ESTILOS ----
    st.markdown("""
        <style>
        .login-box {
            background-color: white;
            color: black;
            border-radius: 20px;
            padding: 3rem 2rem;
            max-width: 450px;
            margin: auto;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        @media (prefers-color-scheme: dark) {
            .login-box {
                background-color: #1e1e1e;
                color: white;
            }
        }
        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #3bb3d4;
        }
        .stTextInput input {
            color: black !important;
        }
        .stButton > button {
            background-color: #20c997 !important;
            color: white !important;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #17b08b !important;
            color: white !important;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .logo-container img {
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- UI ----
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        # LOGO
        if os.path.exists("logobiblioteca.png"):
            st.markdown(f"""
                <div class="logo-container">
                    <img src="data:image/png;base64,{base64.b64encode(open('logobiblioteca.png', 'rb').read()).decode()}">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Logo no encontrado.")

        # TÍTULO
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)

        # CAMPOS
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        # BOTONES
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Iniciar sesión"):
                if not correo or not contrasena:
                    st.warning("⚠️ Campos incompletos")
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

        # CAMBIAR CONTRASEÑA
        st.divider()
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
