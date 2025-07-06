import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ---------- INITIALIZE FIREBASE (UNCHANGED) ----------
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

# ---------- LOGIN FUNCTION (REDESIGNED FOR MINIMALISM & THEME, FOCUS ON STABILITY) ----------
def login():
    # Initialize session state for dark mode if not already present
    if "modo_oscuro" not in st.session_state:
        st.session_state.modo_oscuro = False # Default to light mode

    # Set page config for centered layout, collapsible sidebar (default), and page title
    st.set_page_config(
        layout="centered", # Best for a single form card
        initial_sidebar_state="collapsed",
        page_title="Biblioteca Alejandría - Iniciar Sesión"
    )

    # Define colors based on theme, simplified
    if st.session_state.modo_oscuro:
        bg_color = "#121212" # Very dark background
        text_color = "#E0E0E0" # Light grey text
        card_bg_color = "#1E1E1E" # Dark card
        input_bg_color = "#2C2C2C"
        input_border_color = "#444444"
        accent_color = "#66B2FF" # Light blue for dark mode
        button_hover_bg = "#509EE0"
        shadow_color = "rgba(0, 0, 0, 0.6)"
    else:
        bg_color = "#F0F2F5" # Light grey background
        text_color = "#333333" # Dark text
        card_bg_color = "#FFFFFF" # White card
        input_bg_color = "#FFFFFF" # White input background
        input_border_color = "#E0E0E0"
        accent_color = "#007BFF" # Standard light blue for light mode
        button_hover_bg = "#0056b3"
        shadow_color = "rgba(0, 0, 0, 0.15)"

    # --- Inject Minimal Custom CSS ---
    st.markdown(f"""
    <style>
    /* General body and app styling */
    html, body, [data-testid="stAppViewContainer"] {{
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background-color: {bg_color};
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease; /* Smooth theme transition */
        color: {text_color}; /* Global text color */
    }}

    /* Remove default Streamlit block padding */
    .main > div {{
        padding: 0 !important;
    }}

    /* Target the container for the card effect */
    .st-emotion-cache-nahz7x {{ /* This is a Streamlit specific class for containers, might vary slightly */
        background-color: {card_bg_color};
        padding: 40px; /* Generous internal padding */
        border-radius: 12px;
        box-shadow: 0 10px 30px {shadow_color};
        width: 100%;
        max-width: 450px; /* Control card width */
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center; /* Center contents of the card */
        gap: 15px; /* Default gap between direct children for better spacing */
    }}

    /* Specific styles for elements inside the card */
    .header-section {{
        display: flex;
        align-items: center;
        margin-bottom: 25px; /* Space below header */
        gap: 15px;
        justify-content: center;
        width: 100%;
    }}

    .logo-placeholder {{
        width: 50px; /* Smaller, cleaner logo */
        height: 50px;
        background-color: {input_border_color};
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: {text_color};
        font-size: 8px; /* For the 'Logo' text */
    }}

    .app-title {{
        font-size: 28px; /* Clean title size */
        font-weight: 600;
        color: {text_color};
        margin: 0; /* Remove default margins */
    }}

    .login-heading {{
        font-size: 22px; /* Subheader size */
        font-weight: 500;
        color: {text_color};
        margin-bottom: 20px; /* Space below heading */
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Input field styling */
    .stTextInput > label {{
        display: none; /* Hide default labels */
    }}
    .stTextInput {{
        width: 100%; /* Ensure inputs take full available width */
        margin-bottom: 10px; /* Space between inputs */
    }}
    .stTextInput > div > div > input {{
        background-color: {input_bg_color};
        border: 1px solid {input_border_color};
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 16px;
        color: {text_color};
        width: 100%;
        box-sizing: border-box; /* Include padding in width */
        transition: all 0.2s ease;
    }}
    .stTextInput > div > div > input::placeholder {{
        color: {text_color}77; /* Slightly transparent */
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {accent_color};
        outline: none;
        box-shadow: 0 0 0 2px {accent_color}40; /* Light glow on focus */
    }}


    /* Button Styling */
    .stButton > button {{
        background-color: {accent_color};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 17px;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease, color 0.2s ease;
        box-shadow: 0 4px 10px {accent_color}40; /* Soft shadow for primary button */
        margin-bottom: 0 !important; /* Remove default Streamlit button margin */
        height: auto !important; /* Allow height to adjust */
    }}

    .stButton > button:hover {{
        background-color: {button_hover_bg};
        box-shadow: 0 6px 15px {accent_color}60;
    }}
    
    /* Specific styling for the 'Registrarse' button when in columns */
    .st-emotion-cache-ocqkz7.e1f1d6gn4 > div:last-child .stButton > button {{ /* Targeting the right column button */
        background-color: transparent;
        color: {accent_color};
        border: 1px solid {accent_color};
        box-shadow: none;
    }}

    .st-emotion-cache-ocqkz7.e1f1d6gn4 > div:last-child .stButton > button:hover {{
        background-color: {accent_color}20; /* Light fill on hover */
        box-shadow: none;
        color: {accent_color};
    }}

    /* Forgot password button as a link */
    .forgot-password-link-btn > button {{
        background-color: transparent !important;
        color: {text_color}88 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 8px 15px !important;
        font-size: 14px !important;
        text-decoration: underline;
        width: auto !important; /* Allow button to size to content */
        margin-top: 15px !important; /* Space above */
    }}

    .forgot-password-link-btn > button:hover {{
        color: {accent_color} !important;
        background-color: transparent !important;
        text-decoration: underline;
    }}

    /* Theme toggle button specific styling */
    .theme-toggle-btn > button {{
        background-color: {input_bg_color};
        color: {text_color};
        border: 1px solid {input_border_color};
        border-radius: 20px; /* Pill shape */
        padding: 8px 15px;
        font-size: 15px;
        gap: 5px; /* Icon and text gap */
        width: auto;
        box-shadow: none;
        transition: all 0.2s ease;
    }}
    .theme-toggle-btn > button:hover {{
        background-color: {accent_color}20;
        border-color: {accent_color};
        color: {text_color};
    }}

    /* Hide the default separator if st.markdown("---") is used */
    hr {{
        display: none;
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- Layout and Content ---
    # Create columns for robust centering of the entire card
    col_left_spacer, col_center_content, col_right_spacer = st.columns([1, 3, 1]) # Adjust ratio for good centering

    with col_center_content:
        # Use st.container to get a distinct block for the card
        # We need to manually add a class for targeting with CSS
        st.markdown('<div class="login-card-container">', unsafe_allow_html=True)

        # Theme Toggle Button (placed at the top-right of the card container)
        # Using a div to position it relative to the card, if CSS positioning is used
        # For simplicity, we'll place it as a normal element for now,
        # and rely on the container's flexbox centering or a simple `st.columns`
        # for a clean top-right corner if needed.
        # For this setup, let's put it as the first element inside the card,
        # and center the rest.
        
        # Header Section (Logo, Title, and Theme Button in same row)
        header_cols = st.columns([1, 4, 1]) # Logo, Title, Theme Button
        with header_cols[0]:
            st.markdown('<div class="logo-placeholder"></div>', unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown('<p class="app-title">Biblioteca Alejandría</p>', unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True)
            theme_icon = "☀️" if not st.session_state.modo_oscuro else "🌙"
            if st.button(f"{theme_icon} Tema", key="theme_toggle_btn"):
                st.session_state.modo_oscuro = not st.session_state.modo_oscuro
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Login Heading (centered)
        st.markdown('<h3 class="login-heading">🔐 Iniciar sesión</h3>', unsafe_allow_html=True)

        # Input Fields (maintaining original keys and functionality)
        # Placeholder added for better UX
        correo = st.text_input("Correo electrónico", placeholder="Correo electrónico", key="login_email_input_fixed")
        contrasena = st.text_input("Contraseña", placeholder="Contraseña", type="password", key="login_password_input_fixed")

        # Login and Register Buttons in 2 columns (maintaining original structure)
        col_btn_login, col_btn_register = st.columns(2)
        acceso = False
        usuario = None

        with col_btn_login:
            # Login button (unique key)
            if st.button("Iniciar sesión", key="login_submit_btn_fixed"):
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    datos = doc.to_dict()
                    if datos["contrasena"] == contrasena:
                        st.success(f"Bienvenido, {datos['nombre']} 👋")
                        acceso = True
                        usuario = datos
                        st.session_state.logged_in = True # Set session state for successful login
                        st.session_state.logged_user_name = datos['nombre']
                        st.session_state.vista = "dashboard" # Redirect
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

        with col_btn_register:
            # Register button (unique key, styled as secondary)
            # The custom class 'secondary-btn' will apply to the button inside this column
            if st.button("Registrarse", key="register_button_fixed"):
                st.session_state.vista = "registro"
                st.rerun()

        # Forgot Password Button (unique key, styled as a link)
        # This button is intentionally placed outside the columns for a single centered line
        st.markdown('<div class="forgot-password-link-btn">', unsafe_allow_html=True)
        if st.button("¿Olvidaste tu contraseña?", key="forgot_password_button_fixed"):
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Close login-card-container div

    return acceso, usuario

# ---------- MAIN APPLICATION FLOW (UNCHANGED FUNCTIONALITY) ----------
if __name__ == "__main__":
    if "vista" not in st.session_state:
        st.session_state.vista = "login"

    if st.session_state.vista == "login":
        login()
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro. (Implementa tu lógica aquí)")
        # Add your actual registration form elements here
        if st.button("Volver al Login", key="back_from_register_page"): # Unique key
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña. (Implementa tu lógica aquí)")
        # Add your actual password recovery form elements here
        if st.button("Volver al Login", key="back_from_recovery_page"): # Unique key
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "dashboard":
        st.title(f"🎉 Bienvenido al Dashboard, {st.session_state.get('logged_user_name', 'usuario')}!")
        st.write("¡Has iniciado sesión exitosamente!")
        st.write("Este es tu espacio personal.")
        if st.button("Cerrar Sesión", key="logout_dashboard_fixed"): # Unique key
            if 'logged_in' in st.session_state:
                del st.session_state.logged_in
            if 'logged_user_name' in st.session_state:
                del st.session_state.logged_user_name
            st.session_state.vista = "login"
            st.rerun()