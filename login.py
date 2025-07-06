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

    # Estilos para centrar vertical y horizontalmente
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #E8F6FC;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .main {
            padding: 0 !important;
        }
        .login-box {
            background-color: rgba(255,255,255,0.95);
            color: black;
            border-radius: 16px;
            padding: 2rem 1.5rem;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: auto;
        }
        @media (prefers-color-scheme: dark) {
            .login-box {
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
            font-size: 1.7rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #3bb3d4;
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
        }
        .stButton>button:hover {
            background-color: #34a6c4;
        }
        .stTextInput>div>div>input {
            padding: 0.5rem 0.75rem;
            font-size: 0.95rem;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Iniciar sesión</div>', unsafe_allow_html=True)

        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        # Botones centrados y ajustados en ancho
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
