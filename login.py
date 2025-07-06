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
    # Estilos CSS
    st.markdown("""
        <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
        }
        .login-box {
            background-color: var(--background-color);
            border: 1px solid #ccc;
            border-radius: 16px;
            padding: 50px 40px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        .login-box h2 {
            margin-bottom: 30px;
            color: var(--text-color);
        }
        .stTextInput>div>div>input,
        .stTextArea>div>textarea {
            border-radius: 10px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        .login-button {
            background-color: #a2ded0;
            color: black;
            border-radius: 10px;
            padding: 0.6em 1.5em;
            font-weight: bold;
        }
        .bottom-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        .forgot-password {
            margin-top: 20px;
        }
        /* Tema claro/oscuro dinámico */
        .stApp {
            --background-color: white;
            --text-color: black;
        }
        @media (prefers-color-scheme: dark) {
            .stApp {
                --background-color: #1e1e1e;
                --text-color: white;
            }
            .login-box {
                border: 1px solid #444;
            }
            .stTextInput>div>div>input,
            .stTextArea>div>textarea {
                background-color: #333;
                color: white;
                border: 1px solid #666;
            }
            .login-button {
                background-color: #a2ded0;
                color: black;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Diseño visual
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2>🔐 Iniciar sesión</h2>', unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns(2)
    acceso = False
    usuario = None

    with col1:
        if st.button("Iniciar sesión", use_container_width=True):
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
        if st.button("Registrarse", use_container_width=True):
            st.session_state.vista = "registro"
            st.rerun()

    st.markdown('<div class="forgot-password">', unsafe_allow_html=True)
    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario
