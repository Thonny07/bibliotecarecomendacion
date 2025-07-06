import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json  # Necesario para convertir el string del secret

# ---------- CONFIGURACIÓN GLOBAL ----------
st.set_page_config(page_title="Login", layout="centered")

st.markdown("""
    <style>
        html, body, [class*="stApp"] {
            background-color: #E0F7FA;
            height: 100%;
            overflow: hidden;
        }
        .login-container {
            background-color: white;
            padding: 40px 30px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            width: 380px;
            margin: auto;
            margin-top: 8vh;
        }
        .stButton>button {
            width: 100%;
            margin-top: 10px;
            background-color: #0288D1;
            color: white;
        }
        .stTextInput>div>input {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

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

# ---------- FUNCIÓN LOGIN ----------
def login():
    acceso = False
    usuario = None

    # Contenedor visual
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Generic_Login_Icon.svg/1200px-Generic_Login_Icon.svg.png", width=80)
        st.markdown("### 🔐 Iniciar sesión")

        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Iniciar sesión"):
                if not correo or not contrasena:
                    st.warning("⚠️ Completa ambos campos antes de continuar.")
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
                    except Exception as e:
                        st.error(f"❌ Error de conexión: {e}")

        with col2:
            if st.button("Registrarse"):
                st.session_state.vista = "registro"
                st.rerun()

        st.markdown("---")
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
