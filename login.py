import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ---------- INITIALIZE FIREBASE (KEEPING AS IS) ----------
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

# ---------- LOGIN FUNCTION (INTEGRATING DESIGN) ----------
def login():
    # Set page config once at the beginning. "centered" is usually good for forms.
    # Set page_title for browser tab title
    st.set_page_config(layout="centered", initial_sidebar_state="collapsed", page_title="Biblioteca Alejandría")

    # --- Custom CSS for the desired design ---
    st.markdown("""
    <style>
    /* General body and app styling */
    html, body, [data-testid="stAppViewContainer"] {
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
    [data-testid="stVerticalBlock"] > div:first-child { /* Targets the main content area */
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column; /* Align items vertically */
        min-height: 100vh; /* Ensure it takes full viewport height for centering */
        width: 100%; /* Ensure it uses full width for columns */
        max-width: 100%; /* Override any default max-width */
        padding-top: 0 !important; /* Remove default padding */
        padding-bottom: 0 !important;
    }

    /* The main white card container for the login form */
    .login-card-container {
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
    .login-heading-custom { /* Custom class to distinguish from st.subheader */
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
    /* Target based on their parent div attributes for robustness */
    .stTextInput label {
        display: none; /* Hide default Streamlit labels */
    }

    .stTextInput > div > div > input { /* Target the actual input element more directly */
        background-color: #f8f8f8; /* Lighter background for input fields */
        border: 1px solid #e0e0e0; /* Subtle border */
        border-radius: 8px; /* Slightly rounded corners */
        padding: 12px 15px !important; /* Adjust padding, !important for override */
        font-size: 17px; /* Slightly larger font */
        color: #333; /* Darker text color */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); /* Inner shadow for depth */
        width: 100%; /* Ensure full width */
        box-sizing: border-box; /* Include padding in width */
    }
    .stTextInput {
        margin-bottom: 20px; /* More space between inputs */
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

    /* Specific style for 'Registrarse' and 'Olvidaste tu contraseña?' buttons */
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
    
    /* Adjust columns for buttons if needed, ensuring they don't break functionality */
    div[data-testid="stColumns"] {
        width: 100% !important; /* Ensure columns take full width */
        display: flex;
        justify-content: space-between; /* Space out buttons */
        gap: 20px; /* Gap between columns */
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(5) > div > div { /* Target the specific div wrapping the two buttons */
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

    # --- Use Streamlit's column system to center the content ---
    # Create three columns: left_spacer, main_content_column, right_spacer
    col_left, col_main, col_right = st.columns([1, 2, 1]) # Adjust ratios as needed for centering

    with col_main:
        # --- Start the main white card container ---
        st.markdown('<div class="login-card-container">', unsafe_allow_html=True)

        # Theme button (positioned absolutely within the card div)
        st.markdown('<div class="theme-button-wrapper">', unsafe_allow_html=True)
        icono = "💡 Tema"
        # Using a unique key for this specific button
        if st.button(icono, key="theme_btn_top_right"):
            st.session_state.modo_oscuro = not st.session_state.get("modo_oscuro", False)
            st.rerun() # Rerun to apply theme changes
        st.markdown('</div>', unsafe_allow_html=True)

        # Header section: Logo and Title
        st.markdown('<div class="header-content">', unsafe_allow_html=True)
        st.markdown('<div class="logo-placeholder"></div>', unsafe_allow_html=True) # Placeholder for actual logo
        st.markdown('<div class="title-text">Biblioteca Alejandría</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Login heading with lock icon - Using custom class instead of st.subheader for direct control
        st.markdown('<div class="login-heading-custom">🔒 Iniciar sesión</div>', unsafe_allow_html=True)

        # Input fields (keeping your existing structure and keys, but hiding labels with CSS)
        correo = st.text_input("Correo electrónico", key="login_email_input") # Added specific key
        contrasena = st.text_input("Contraseña", type="password", key="login_password_input") # Added specific key

        acceso = False
        usuario = None

        # Buttons - Keep your original col1, col2 structure for these specific buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Iniciar sesión", key="login_submit_btn"): # Ensure unique key
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    datos = doc.to_dict()
                    if datos["contrasena"] == contrasena:
                        st.success(f"Bienvenido, {datos['nombre']} 👋")
                        acceso = True
                        usuario = datos
                        # Store user info and change view on successful login
                        st.session_state.logged_in = True
                        st.session_state.logged_user = datos['nombre'] # Store relevant user info
                        st.session_state.vista = "dashboard" # Assuming a dashboard or main app view
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

        with col2:
            st.markdown('<div class="secondary-button">', unsafe_allow_html=True) # Apply secondary style
            if st.button("Registrarse", key="register_button_from_login"): # Ensure unique key
                st.session_state.vista = "registro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Opción de recuperación de contraseña (keeping your original structure)
        st.markdown("---") # Keep the separator if you like it, or remove for cleaner look
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True) # Apply secondary style
        if st.button("¿Olvidaste tu contraseña?", key="forgot_password_button_from_login"): # Ensure unique key
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Close login-card-container div
    # st.columns context automatically closes here

    return acceso, usuario

# ---------- MAIN APPLICATION FLOW (KEEPING AS IS) ----------
if __name__ == "__main__":
    if "vista" not in st.session_state:
        st.session_state.vista = "login"

    # Handle routing based on session state
    if st.session_state.vista == "login":
        login() # Call the login function
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro.")
        # Your registration fields and logic here
        if st.button("Volver al Login", key="back_to_login_from_register"):
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña.")
        # Your recovery fields and logic here
        if st.button("Volver al Login", key="back_to_login_from_recovery"):
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "dashboard":
        # Example Dashboard content after successful login
        st.title(f"Bienvenido al Dashboard, {st.session_state.get('logged_user', 'Usuario')}!")
        st.write("Este es el contenido principal de la aplicación después de iniciar sesión.")
        if st.button("Cerrar Sesión", key="logout_btn"):
            # Clear relevant session state variables on logout
            if 'logged_in' in st.session_state:
                del st.session_state.logged_in
            if 'logged_user' in st.session_state:
                del st.session_state.logged_user
            st.session_state.vista = "login"
            st.rerun()