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

    # Estilos para centrar y limitar ancho
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #E8F6FC;
        }
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 3vh;
        }
        .centered-box {
            background-color: white;
            border-radius: 16px;
            padding: 2.5rem 2rem;
            width: 50%;
            max-width: 500px;
            min-width: 320px;
            margin: auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        @media (prefers-color-scheme: dark) {
            .centered-box {
                background-color: #1e1e1e;
                color: white;
            }
            input, textarea {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #777 !important;
            }
        }
        .login-title {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #3bb3d4;
        }
        .stTextInput>div>div>input {
            padding: 0.4rem 0.7rem;
            font-size: 0.95rem;
        }
        .stButton>button {
            background-color: #3bb3d4;
            color: white;
            border: none;
            padding: 0.45rem 1rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
            width: 100%;
            font-size: 0.9rem;
        }
        .stButton>button:hover {
            background-color: #34a6c4;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="centered-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)

        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        col1, col2 = st.columns(2)
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
