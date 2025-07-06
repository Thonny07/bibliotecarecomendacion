import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase (keeping your original Firebase initialization)
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
    # Set page config for a wider layout if preferred, or remove for default
    st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

    # Inject custom CSS for the desired design
    st.markdown("""
    <style>
    /* General body and app styling */
    html, body, .stApp {
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background-color: #f0f2f5; /* Light background similar to the image */
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* Target the main content block to center the card */
    .main .block-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh; /* Ensure it takes full viewport height for centering */
        padding-top: 0rem; /* Remove default padding */
        padding-bottom: 0rem;
    }

    /* The main white card container for the login form */
    .login-card {
        background-color: white;
        padding: 40px 50px; /* Increased padding for more space */
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Softer, larger shadow */
        width: 100%;
        max-width: 480px; /* Adjust max-width to match the image's proportions */
        text-align: center;
        position: relative; /* For absolute positioning of theme button */
    }

    /* Header section with logo and title */
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center; /* Center the logo and text */
        margin-bottom: 30px;
        gap: 15px; /* Space between logo and text */
    }

    .header-content .logo-placeholder {
        width: 70px; /* Larger logo size */
        height: 70px;
        background-color: #e0e0e0; /* Placeholder background */
        border-radius: 50%; /* Circular */
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 10px;
        color: #666;
        border: 1px solid #ccc; /* Subtle border */
    }

    .header-content .title-text {
        font-size: 30px; /* Larger title */
        font-weight: 700; /* Bolder */
        color: #333;
    }

    /* Theme button positioning (top-right of the card) */
    .theme-button-wrapper {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 10; /* Ensure it's above other elements */
    }

    .theme-button-wrapper button {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 15px;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #555;
        box-shadow: none; /* Remove Streamlit default shadow */
    }

    .theme-button-wrapper button:hover {
        background-color: #e5e5e5;
    }

    /* Login heading */
    .login-heading {
        font-size: 24px; /* Larger login heading */
        font-weight: 600;
        color: #555;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    /* Styling for Streamlit text inputs */
    .stTextInput label {
        display: none; /* Hide default Streamlit labels */
    }

    .stTextInput div[data-baseweb="input"] {
        background-color: #f8f8f8; /* Lighter background for input fields */
        border: 1px solid #e0e0e0; /* Subtle border */
        border-radius: 8px; /* Slightly rounded corners */
        padding: 5px 15px; /* Adjust padding */
        margin-bottom: 20px; /* More space between inputs */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); /* Inner shadow for depth */
    }

    .stTextInput input {
        border: none !important;
        box-shadow: none !important;
        font-size: 17px; /* Slightly larger font */
        padding: 8px 0; /* Vertical padding inside input */
        color: #333; /* Darker text color */
    }

    .stTextInput input::placeholder {
        color: #aaa; /* Lighter placeholder text */
    }

    /* Styling for Streamlit buttons */
    .stButton > button {
        background-color: #007bff; /* A clear blue */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px; /* Match input fields */
        padding: 14px 25px; /* Larger buttons */
        width: 100%;
        margin-top: 15px; /* Space between buttons and inputs/other buttons */
        font-size: 18px; /* Larger font for buttons */
        cursor: pointer;
        transition: background-color 0.2s ease; /* Smooth transition for hover */
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Subtle shadow for buttons */
    }

    .stButton > button:hover {
        background-color: #0056b3; /* Darker blue on hover */
        box-shadow: 0 4px 8px rgba(0,0,0,0.15); /* Slightly larger shadow on hover */
    }

    /* Specific style for 'Registrarse' and 'Olvidaste tu contraseña?' buttons
       to make them look like links or secondary actions */
    .secondary-button button {
        background-color: transparent !important; /* No background */
        color: #007bff !important; /* Blue link color */
        border: none !important;
        box-shadow: none !important;
        padding: 8px 15px !important; /* Smaller padding */
        font-size: 16px !important; /* Smaller font */
        margin-top: 10px !important; /* Less margin */
    }

    .secondary-button button:hover {
        background-color: transparent !important;
        color: #0056b3 !important;
        text-decoration: underline; /* Underline on hover for link-like buttons */
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Start the main login card container
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # Theme button (positioned absolutely within the card)
    st.markdown('<div class="theme-button-wrapper">', unsafe_allow_html=True)
    icono = "💡 Tema" # Changed to text + icon as in the target image for the button
    if st.button(icono, key="tema_btn_top"): # Unique key for this button
        st.session_state.modo_oscuro = not st.session_state.get("modo_oscuro", False)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Header section: Logo and Title
    st.markdown('<div class="header-content">', unsafe_allow_html=True)
    st.markdown('<div class="logo-placeholder">Logo</div>', unsafe_allow_html=True) # Placeholder for actual logo
    st.markdown('<div class="title-text">Biblioteca Alejandría</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Login heading with lock icon
    st.markdown('<div class="login-heading">🔒 Iniciar sesión</div>', unsafe_allow_html=True)

    # Input fields
    # Streamlit text_input widgets generate their own div structure, so we style their internals.
    correo = st.text_input("", placeholder="Correo electrónico", key="email_input")
    contrasena = st.text_input("", placeholder="Contraseña", type="password", key="password_input")

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
    # Wrap in a div to apply specific secondary button styling
    st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
    if st.button("Registrarse", key="register_btn"):
        st.session_state.vista = "registro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # "¿Olvidaste tu contraseña?" button
    # Wrap in a div for consistent styling, or apply directly if unique.
    st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
    if st.button("¿Olvidaste tu contraseña?", key="forgot_password_btn"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True) # Close login-card

    return acceso, usuario

# Main application logic to handle different views
if __name__ == "__main__":
    if "vista" not in st.session_state:
        st.session_state.vista = "login"

    if st.session_state.vista == "login":
        acceso, usuario = login()
        if acceso:
            st.write(f"Acceso concedido para: {usuario['nombre']}")
            # In a real app, you would redirect to a different page or show main content
            # For this example, we just display a message
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro.")
        # Example registration fields (not implemented fully for this request)
        # st.text_input("Nombre de Usuario")
        # st.text_input("Correo Electrónico")
        # st.text_input("Contraseña", type="password")
        # st.text_input("Confirmar Contraseña", type="password")
        # st.button("Crear Cuenta")
        if st.button("Volver al Login"):
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña.")
        # Example recovery fields (not implemented fully for this request)
        # st.text_input("Correo Electrónico")
        # st.button("Enviar Código")
        if st.button("Volver al Login"):
            st.session_state.vista = "login"
            st.rerun()