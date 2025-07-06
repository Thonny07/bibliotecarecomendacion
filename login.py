import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from PIL import Image

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

# ---------- APLICAR ESTILO DE TEMA ----------
def aplicar_tema_login():
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo};
            color: {texto};
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        .stTextInput input, .stTextArea textarea, .stSelectbox select {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid #44bba4;
            border-radius: 8px;
            padding: 8px;
        }}
        .stButton button {{
            background-color: #44bba4;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 16px;
        }}
        .stButton button:hover {{
            background-color: #379d8e;
        }}
        .login-container {{
            display: flex;
            height: 100vh;
        }}
        .left-side {{
            flex: 7;
            overflow: hidden;
        }}
        .left-side img {{
            width: 100%;
            height: 100vh;
            object-fit: cover;
        }}
        .right-side {{
            flex: 3;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .theme-button {{
            position: absolute;
            top: 10px;
            right: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ---------- LOGIN ----------
def login():
    aplicar_tema_login()

    if "modo_oscuro" not in st.session_state:
        st.session_state.modo_oscuro = False

    # Contenedor principal con HTML
    st.markdown("""
        <div class='login-container'>
            <div class='left-side'>
                <img src='portadalogin.png' />
            </div>
            <div class='right-side'>
                <div class='theme-button'>
                    <form action="#" method="post">
                        <button name="toggle" type="submit">{}</button>
                    </form>
                </div>
    """.format("🔆" if not st.session_state.modo_oscuro else "🌙"), unsafe_allow_html=True)

    # Detectar clic del botón de tema manualmente (fuera del form)
    if st.query_params.get("toggle") == "":
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

    # CONTENIDO DEL FORMULARIO DE LOGIN
    st.markdown("""
                <div style='text-align: center;'>
                    <img src='logobiblioteca.png' width='80' style='border-radius: 50%;'/><br>
                    <h2>Biblioteca Alejandría</h2>
                </div>
    """, unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    acceso = False
    usuario = None

    if st.button("Iniciar sesión"):
        doc = db.collection("usuarios").document(correo).get()
        if doc.exists:
            datos = doc.to_dict()
            if datos["contrasena"] == contrasena:
                st.success(f"Bienvenido, {datos['nombre']}")
                acceso = True
                usuario = datos
            else:
                st.error("❌ Contraseña incorrecta")
        else:
            st.error("❌ Usuario no encontrado")

    col_links = st.columns(2)
    with col_links[0]:
        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()

    with col_links[1]:
        if st.button("Registrarse"):
            st.session_state.vista = "registro"
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    return acceso, usuario
