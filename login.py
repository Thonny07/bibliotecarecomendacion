import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64
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

    # Cargar el logo como base64
    def load_logo_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    logo_path = "logobiblioteca.png"
    if os.path.exists(logo_path):
        logo_base64 = load_logo_base64(logo_path)
        logo_html = f'''
            <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover;">
            </div>
        '''
    else:
        logo_html = "<p style='color:red;text-align:center;'>⚠️ Logo no encontrado</p>"

    # Estilos
    st.markdown(f"""
        <style>
        .login-container {{
            background-color: white;
            padding: 2rem;
            max-width: 400px;
            margin: auto;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
        .app-title {{
            text-align: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: #3bb3d4;
            margin-bottom: 1rem;
        }}
        input[type="text"], input[type="password"] {{
            color: black !important;
        }}
        input::placeholder {{
            color: #555 !important;
        }}
        .button-row {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 1rem;
        }}
        .custom-button > button {{
            background-color: #20c997 !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            font-size: 15px;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .custom-button > button:hover {{
            background-color: #18b089 !important;
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # UI
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown('<div class="app-title">Biblioteca Alejandría</div>', unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico", placeholder="Ingresa tu correo")
    contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

    st.markdown('<div class="button-row">', unsafe_allow_html=True)

    # Botón: Iniciar sesión
    st.markdown('<div class="custom-button">', unsafe_allow_html=True)
    if st.button("Iniciar sesión", key="btn_login"):
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
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón: Registrarse
    st.markdown('<div class="custom-button">', unsafe_allow_html=True)
    if st.button("Registrarse", key="btn_register"):
        st.session_state.vista = "registro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Botón: ¿Olvidaste tu contraseña?
    st.markdown('<div class="custom-button">', unsafe_allow_html=True)
    if st.button("¿Olvidaste tu contraseña?", key="btn_forgot"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Cierre .button-row
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre .login-container

    return acceso, usuario
