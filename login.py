import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Inicializar Firebase
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
    st.set_page_config(layout="centered")  # Changed to centered layout

    st.markdown("""
    <style>
    html, body, .stApp {
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow: hidden;
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f2f5; /* Light grey background */
    }

    .main .block-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh; /* Ensure it takes full viewport height */
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .login-container {
        background-color: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 450px; /* Increased max-width to match image */
        text-align: center;
    }

    .header-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 30px;
    }

    .header-section .logo-text {
        display: flex;
        align-items: center;
        gap: 15px; /* Space between logo and text */
    }

    .header-section .logo {
        width: 60px; /* Adjust logo size */
        height: 60px;
        background-color: #e0e0e0; /* Placeholder for logo image */
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 10px; /* For the text inside the placeholder */
        color: #666;
        border: 1px solid #ccc;
    }

    .header-section .title {
        font-size: 28px; /* Adjust title size */
        font-weight: 600;
        color: #333;
    }

    .theme-button-container {
        margin-left: auto; /* Pushes theme button to the right */
        display: flex;
        align-items: center;
    }

    .theme-button-container button {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 12px;
        font-size: 18px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: none; /* Remove Streamlit's default button shadow */
        color: #555;
    }

    .theme-button-container button:hover {
        background-color: #e5e5e5;
    }

    .login-heading {
        font-size: 22px;
        font-weight: 600;
        color: #555;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .stTextInput label {
        display: none; /* Hide default Streamlit labels */
    }

    .stTextInput div[data-baseweb="input"] {
        background-color: #f8f8f8;
        border: 1px solid #e0e0e0;
        border-radius: 5px; /* More subtle border radius */
        padding: 5px 10px;
        margin-bottom: 15px; /* Space between inputs */
    }

    .stTextInput input {
        border: none !important; /* Remove inner border */
        box-shadow: none !important; /* Remove inner shadow */
        font-size: 16px;
        padding: 5px 0;
    }

    .stTextInput input::placeholder {
        color: #aaa;
    }

    .stButton > button {
        background-color: #007bff; /* Example primary color */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px; /* Match input fields */
        padding: 12px 20px;
        width: 100%;
        margin-top: 20px;
        font-size: 18px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #0056b3; /* Darker shade on hover */
    }

    /* Style for the "Registrarse" button */
    .register-button-container {
        margin-top: 15px;
        display: flex;
        justify-content: center; /* Center the register button */
    }

    .register-button-container button {
        background-color: transparent;
        color: #007bff; /* Link color */
        border: none;
        padding: 0;
        font-size: 16px;
        cursor: pointer;
        text-decoration: underline;
    }

    .register-button-container button:hover {
        color: #0056b3;
    }

    .forgot-password-button {
        background-color: transparent;
        color: #888; /* Softer color for forgotten password */
        border: none;
        padding: 0;
        font-size: 14px;
        cursor: pointer;
        margin-top: 10px; /* Space above */
    }

    .forgot-password-button:hover {
        text-decoration: underline;
    }

    </style>
    """, unsafe_allow_html=True)

    # Main container for the login form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Header section with logo, title, and theme button
    st.markdown('<div class="header-section">', unsafe_allow_html=True)
    st.markdown('<div class="logo-text">', unsafe_allow_html=True)
    st.markdown('<div class="logo"></div>', unsafe_allow_html=True) # Placeholder for the logo
    st.markdown('<div class="title">Biblioteca Alejandría</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Close logo-text div

    st.markdown('<div class="theme-button-container">', unsafe_allow_html=True)
    icono = "💡 Tema" # Icon and text for the theme button
    if st.button(icono, key="tema_btn"):
        st.session_state.modo_oscuro = not st.session_state.get("modo_oscuro", False)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True) # Close theme-button-container

    st.markdown('</div>', unsafe_allow_html=True) # Close header-section

    st.markdown('<div class="login-heading">🔒 Iniciar sesión</div>', unsafe_allow_html=True)

    correo = st.text_input("Correo electrónico", placeholder="Correo electrónico", key="email_input")
    contrasena = st.text_input("Contraseña", placeholder="Contraseña", type="password", key="password_input")

    acceso = False
    usuario = None

    # Login button
    if st.button("Iniciar sesión", key="login_btn"):
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

    # "Registrarse" button
    st.markdown('<div class="register-button-container">', unsafe_allow_html=True)
    if st.button("Registrarse", key="register_btn"):
        st.session_state.vista = "registro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # "Olvidaste tu contraseña?" button (placed below register)
    if st.button("¿Olvidaste tu contraseña?", key="forgot_password_btn"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) # Close login-container

    return acceso, usuario

# Example of how to run the login function
if __name__ == "__main__":
    if "vista" not in st.session_state:
        st.session_state.vista = "login"

    if st.session_state.vista == "login":
        acceso, usuario = login()
        if acceso:
            st.write(f"Acceso concedido para: {usuario['nombre']}")
            # Here you would typically redirect to the main application page
    elif st.session_state.vista == "registro":
        st.write("Página de Registro (implementar lógica de registro aquí)")
        if st.button("Volver al Login"):
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.write("Página de Recuperación de Contraseña (implementar lógica aquí)")
        if st.button("Volver al Login"):
            st.session_state.vista = "login"
            st.rerun()