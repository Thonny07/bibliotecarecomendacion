import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64

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

    # ---------- CSS PERSONALIZADO ----------
    st.markdown("""
        <style>
        /* OCULTAR HEADER, FOOTER Y RECTÁNGULOS DEFAULT */
        /* LA ÚNICA MODIFICACIÓN ES LA ADICIÓN DE '[data-testid="stHeader"]' A ESTA REGLA */
        header, footer, .css-18ni7ap.e8zbici2, .css-1avcm0n.e8zbici2, [data-testid="stHeader"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }
        .block-container {
            padding-top: 0rem !important;
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
            width: 130px;
            height: 130px;
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

    # ---------- CONTENEDOR PRINCIPAL ----------
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # ---------- LOGO ----------
    try:
        with open("logobiblioteca.png", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f'<img src="data:image/png;base64,{encoded}" class="logo-img">',
                unsafe_allow_html=True
            )
    except:
        st.warning("⚠️ No se pudo cargar el logo.")

    # ---------- TÍTULO ----------
    st.markdown('<div class="login-title">Biblioteca Alejandría</div>', unsafe_allow_html=True)

    # ---------- CAMPOS ----------
    correo = st.text_input("Correo electrónico", key="correo")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena")

    # ---------- BOTONES ----------
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
                        # Asegúrate de que estos estados de sesión sean manejados en el flujo principal del app
                        if 'logged_in' not in st.session_state:
                            st.session_state.logged_in = False
                        if 'logged_user_name' not in st.session_state:
                            st.session_state.logged_user_name = ""
                        st.session_state.logged_in = True
                        st.session_state.logged_user_name = datos['nombre']
                        st.session_state.vista = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

    with col2:
        if st.button("Registrarse"):
            st.session_state.vista = "registro"
            st.rerun()

    if st.button("¿Olvidaste tu contraseña?"):
        # Asegúrate de que estos estados de sesión sean manejados en el flujo principal del app
        if 'codigo_enviado' not in st.session_state:
            st.session_state.codigo_enviado = False
        if 'codigo_verificacion' not in st.session_state:
            st.session_state.codigo_verificacion = ""
        if 'correo_recuperar' not in st.session_state:
            st.session_state.correo_recuperar = ""

        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return acceso, usuario

# ---------- MAIN APPLICATION FLOW (AS PROVIDED IN YOUR ORIGINAL CODE) ----------
if __name__ == "__main__":
    # Asegúrate de que 'vista' esté inicializada en st.session_state
    if 'vista' not in st.session_state:
        st.session_state.vista = "login"
    
    # Asegúrate de que 'logged_in' y 'logged_user_name' estén inicializados
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'logged_user_name' not in st.session_state:
        st.session_state.logged_user_name = ""


    if st.session_state.vista == "login":
        login()
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro. (Implementa tu lógica aquí)")
        # Asegúrate de que los botones en otras vistas también tengan keys únicas si los añades
        if st.button("Volver al Login"): # Podría necesitar key única si hay otros botones sin key
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña. (Implementa tu lógica aquí)")
        # Asegúrate de que los botones en otras vistas también tengan keys únicas si los añades
        if st.button("Volver al Login"): # Podría necesitar key única si hay otros botones sin key
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "dashboard":
        # Asegúrate de que 'logged_user_name' existe antes de usarlo
        user_name = st.session_state.get('logged_user_name', 'usuario')
        st.title(f"🎉 Bienvenido al Dashboard, {user_name}!")
        st.write("¡Has iniciado sesión exitosamente!")
        st.write("Este es tu espacio personal.")
        # Asegúrate de que los botones en otras vistas también tengan keys únicas si los añades
        if st.button("Cerrar Sesión"): # Podría necesitar key única si hay otros botones sin key
            # Al cerrar sesión, limpia el estado de inicio de sesión
            if 'logged_in' in st.session_state:
                del st.session_state.logged_in
            if 'logged_user_name' in st.session_state:
                del st.session_state.logged_user_name
            st.session_state.vista = "login"
            st.rerun()