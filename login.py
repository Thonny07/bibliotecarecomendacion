import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# ---------- FIREBASE INITIALIZATION (UNCHANGED) ----------
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

# ---------- LOGIN FUNCTION (REDESIGNED FOR MINIMALISM & THEME) ----------
def login():
    # Initialize session state for dark mode if not already present
    if "modo_oscuro" not in st.session_state:
        st.session_state.modo_oscuro = False # Default to light mode

    # Set page config for a wide, minimalist layout
    st.set_page_config(
        layout="centered", # Centered layout is best for a single form card
        initial_sidebar_state="collapsed", # No sidebar for login
        page_title="Biblioteca Alejandría - Iniciar Sesión"
    )

    # Define colors based on theme
    if st.session_state.modo_oscuro:
        bg_color = "#1E1E1E" # Dark background
        text_color = "#FFFFFF" # White text
        card_bg_color = "#2E2E2E" # Slightly lighter dark for card
        input_bg_color = "#3A3A3A"
        input_border_color = "#555555"
        accent_color = "#66B2FF" # Light blue for dark mode
        button_hover_bg = "#509EE0"
        shadow_color = "rgba(0, 0, 0, 0.4)"
        icon_color = "#FFFFFF"
    else:
        bg_color = "#F0F2F5" # Light background
        text_color = "#333333" # Dark text
        card_bg_color = "#FFFFFF" # White for card
        input_bg_color = "#F8F8F8"
        input_border_color = "#E0E0E0"
        accent_color = "#007BFF" # Light blue for light mode
        button_hover_bg = "#0056b3"
        shadow_color = "rgba(0, 0, 0, 0.1)"
        icon_color = "#555555"

    # --- Inject Custom CSS ---
    st.markdown(f"""
    <style>
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] > div:first-child {{
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background-color: {bg_color};
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease; /* Smooth theme transition */
    }}

    /* Main content block to ensure centering */
    [data-testid="stVerticalBlock"] > div:first-child {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}

    /* The Login Card Container */
    .login-card-container {{
        background-color: {card_bg_color};
        padding: 40px 50px;
        border-radius: 12px; /* Slightly more rounded */
        box-shadow: 0 8px 30px {shadow_color}; /* More prominent, soft shadow */
        width: 100%;
        max-width: 450px; /* Optimal width for minimalism */
        text-align: center;
        position: relative;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }}

    /* Header: Logo and Title */
    .header-content {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 35px; /* More space below header */
        gap: 20px; /* Space between logo and title */
    }}

    .logo-placeholder {{
        width: 60px; /* Clean, slightly smaller logo */
        height: 60px;
        background-color: {input_border_color}; /* Subtle color matching theme */
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 10px; /* Or replace with an actual SVG/Image */
        color: {text_color};
        border: 1px solid {input_border_color};
        flex-shrink: 0; /* Prevent shrinking */
    }}

    .title-text {{
        font-size: 32px; /* Prominent title */
        font-weight: 700;
        color: {text_color};
        transition: color 0.3s ease;
    }}

    /* Theme Toggle Button */
    .theme-button-wrapper {{
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 10;
    }}

    .theme-button-wrapper button {{
        background-color: {input_bg_color};
        border: 1px solid {input_border_color};
        border-radius: 25px; /* Pill shape */
        padding: 10px 18px;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        color: {text_color};
        box-shadow: none;
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }}

    .theme-button-wrapper button:hover {{
        background-color: {accent_color};
        color: white;
        border-color: {accent_color};
    }}

    /* Login Heading */
    .login-heading-custom {{
        font-size: 26px; /* Slightly larger, clear heading */
        font-weight: 600;
        color: {text_color};
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px; /* Space between icon and text */
        transition: color 0.3s ease;
    }}

    /* Input Fields */
    .stTextInput label {{
        display: none; /* Hide default Streamlit labels for minimalist look */
    }}

    .stTextInput > div > div > input {{
        background-color: {input_bg_color};
        border: 1px solid {input_border_color};
        border-radius: 8px;
        padding: 14px 18px !important; /* Generous padding */
        font-size: 17px;
        color: {text_color};
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        width: 100%;
        box-sizing: border-box;
        transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
    }}
    .stTextInput {{
        margin-bottom: 20px; /* Space between inputs */
    }}
    .stTextInput input::placeholder {{
        color: {text_color}88; /* Semi-transparent placeholder */
        transition: color 0.3s ease;
    }}

    /* Primary Button (Iniciar Sesión) */
    .stButton > button {{
        background-color: {accent_color}; /* Accent color for primary action */
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 15px 25px; /* Larger click area */
        width: 100%;
        margin-top: 15px;
        font-size: 19px; /* Prominent font */
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 10px {accent_color}66; /* Accent color shadow */
    }}

    .stButton > button:hover {{
        background-color: {button_hover_bg};
        box-shadow: 0 6px 15px {accent_color}99;
    }}

    /* Secondary Buttons (Registrarse, Olvidaste contraseña) */
    /* Adjusting column behavior for these buttons */
    [data-testid="stHorizontalBlock"] {{ /* Targets the columns holding "Iniciar sesión" and "Registrarse" */
        gap: 20px; /* Space between the two columned buttons */
        margin-top: 25px; /* Space below password input */
    }}
    [data-testid="stHorizontalBlock"] > div > div > button {{
        width: 100%; /* Ensure full width within their column */
    }}

    .stButton.secondary-btn > button {{ /* Specific class for secondary buttons */
        background-color: transparent !important;
        color: {accent_color} !important; /* Accent color for links */
        border: 1px solid {accent_color} !important; /* Accent colored border */
        box-shadow: none !important;
        padding: 14px 15px !important; /* Consistent padding */
        font-size: 17px !important;
        margin-top: 0px !important; /* Reset margin from general button style */
        border-radius: 8px;
        transition: all 0.2s ease;
    }}

    .stButton.secondary-btn > button:hover {{
        background-color: {accent_color}22 !important; /* Light accent background on hover */
        color: {accent_color} !important;
        text-decoration: none; /* No underline unless specifically desired */
        box-shadow: none !important;
    }}
    
    /* Forgot Password Button - treated as a link */
    .forgot-password-link button {{
        background-color: transparent !important;
        color: {text_color}88 !important; /* Subtler text color */
        border: none !important;
        box-shadow: none !important;
        padding: 8px 15px !important;
        font-size: 15px !important;
        margin-top: 15px !important; /* Space below other buttons */
        text-decoration: underline;
        transition: color 0.2s ease;
    }}

    .forgot-password-link button:hover {{
        color: {accent_color} !important;
        background-color: transparent !important;
        text-decoration: underline;
    }}

    /* Hide the default separator if st.markdown("---") is used but not wanted visually */
    hr {{
        display: none;
    }}

    </style>
    """, unsafe_allow_html=True)

    # --- Layout and Content ---
    # Create columns to center the login card
    col_left, col_main, col_right = st.columns([1, 2, 1])

    with col_main:
        # Start the main login card container
        st.markdown('<div class="login-card-container">', unsafe_allow_html=True)

        # Theme toggle button
        st.markdown('<div class="theme-button-wrapper">', unsafe_allow_html=True)
        # Using an icon for visual clarity
        theme_icon = "☀️" if not st.session_state.modo_oscuro else "🌙"
        if st.button(f"{theme_icon} Tema", key="theme_toggle_btn_main"): # Unique key
            st.session_state.modo_oscuro = not st.session_state.modo_oscuro
            st.rerun() # Rerun to apply theme changes
        st.markdown('</div>', unsafe_allow_html=True)

        # Header section (Logo and Title)
        st.markdown('<div class="header-content">', unsafe_allow_html=True)
        st.markdown('<div class="logo-placeholder"></div>', unsafe_allow_html=True)
        st.markdown('<div class="title-text">Biblioteca Alejandría</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Login Heading
        # Using a custom div for precise styling
        st.markdown('<div class="login-heading-custom">🔒 Iniciar sesión</div>', unsafe_allow_html=True)

        # Input fields (preserving original Streamlit calls and functionality)
        correo = st.text_input("Correo electrónico", placeholder="Correo electrónico", key="login_email_input_unique")
        contrasena = st.text_input("Contraseña", placeholder="Contraseña", type="password", key="login_password_input_unique")

        # Two columns for Login and Register buttons
        col1, col2 = st.columns(2)
        acceso = False
        usuario = None

        with col1:
            # Login button (main action)
            if st.button("Iniciar sesión", key="login_submit_btn_unique"): # Unique key
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    datos = doc.to_dict()
                    if datos["contrasena"] == contrasena:
                        st.success(f"Bienvenido, {datos['nombre']} 👋")
                        acceso = True
                        usuario = datos
                        st.session_state.logged_in = True
                        st.session_state.logged_user_name = datos['nombre'] # Store user's name
                        st.session_state.vista = "dashboard" # Change view after successful login
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

        with col2:
            # Register button (secondary action, styled as such)
            st.markdown('<div class="stButton secondary-btn">', unsafe_allow_html=True) # Apply custom class
            if st.button("Registrarse", key="register_btn_unique"): # Unique key
                st.session_state.vista = "registro"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Forgot password button (tertiary action, styled as a link)
        st.markdown('<div class="forgot-password-link">', unsafe_allow_html=True) # Apply custom class
        if st.button("¿Olvidaste tu contraseña?", key="forgot_password_btn_unique"): # Unique key
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Close login-card-container

    return acceso, usuario

# ---------- MAIN APPLICATION FLOW (UNCHANGED FUNCTIONALITY) ----------
if __name__ == "__main__":
    # Initialize session state for view if not present
    if "vista" not in st.session_state:
        st.session_state.vista = "login"

    # Display content based on the current view
    if st.session_state.vista == "login":
        login()
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro.")
        # Example register elements (you would add your actual form here)
        # st.text_input("Nombre de Usuario")
        # st.text_input("Correo Electrónico")
        # st.text_input("Contraseña", type="password")
        # st.button("Crear Cuenta")
        if st.button("Volver al Login", key="back_from_register"): # Unique key
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña.")
        # Example recovery elements (you would add your actual form here)
        # st.text_input("Correo Electrónico")
        # st.button("Enviar Código")
        if st.button("Volver al Login", key="back_from_recovery"): # Unique key
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "dashboard":
        st.title(f"🎉 Bienvenido al Dashboard, {st.session_state.get('logged_user_name', 'usuario')}!")
        st.write("¡Has iniciado sesión exitosamente!")
        st.write("Este es tu espacio personal.")
        if st.button("Cerrar Sesión", key="logout_dashboard_btn"): # Unique key
            if 'logged_in' in st.session_state:
                del st.session_state.logged_in
            if 'logged_user_name' in st.session_state:
                del st.session_state.logged_user_name
            st.session_state.vista = "login"
            st.rerun()