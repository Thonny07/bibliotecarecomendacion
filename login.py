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

# --- Custom CSS for Minimalist Card Design and Theme ---
def inject_custom_css(modo_oscuro):
    # Define colors based on theme
    if modo_oscuro:
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

    st.markdown(f"""
    <style>
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"], .main {{
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background-color: {bg_color};
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease, color 0.3s ease; /* Smooth theme transition */
        color: {text_color}; /* Global text color */
    }}

    /* Remove Streamlit's default padding on the main content block */
    .main .block-container {{
        padding-top: 0rem;
        padding-bottom: 0rem;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        min-height: 100vh;
    }}

    /* The Login Card Container */
    /* Targeting a more general Streamlit container element or a custom div */
    .st-emotion-cache-nahz7x {{ /* This is a common Streamlit container class */
        background-color: {card_bg_color};
        padding: 40px;
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
    
    /* Specific overrides for common Streamlit components */
    .stTextInput > label {{
        display: none; /* Hide default labels */
    }}
    .stTextInput > div > div > input {{
        background-color: {input_bg_color};
        border: 1px solid {input_border_color};
        border-radius: 8px;
        padding: 10px 12px; /* Slightly less padding to reduce space */
        font-size: 16px;
        color: {text_color};
        width: 100%;
        box-sizing: border-box;
        transition: all 0.2s ease;
    }}
    .stTextInput > div > div > input::placeholder {{
        color: {text_color}77;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {accent_color};
        outline: none;
        box-shadow: 0 0 0 2px {accent_color}40;
    }}

    /* Buttons general style */
    .stButton > button {{
        background-color: {accent_color};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px; /* Consistent padding */
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease, color 0.2s ease;
        box-shadow: 0 4px 10px {accent_color}40;
        margin: 0 !important; /* Eliminate extra margins from Streamlit defaults */
    }}

    .stButton > button:hover {{
        background-color: {button_hover_bg};
        box-shadow: 0 6px 15px {accent_color}60;
    }}

    /* Adjust columns for buttons to remove excessive gap */
    .st-emotion-cache-ocqkz7.e1f1d6gn4 {{ /* Targets the div containing the two-column button layout */
        gap: 15px !important; /* Smaller gap between login and register buttons */
    }}

    /* Specific style for 'Registrarse' button in columns */
    .st-emotion-cache-ocqkz7.e1f1d6gn4 > div:last-child .stButton > button {{
        background-color: transparent;
        color: {accent_color};
        border: 1px solid {accent_color};
        box-shadow: none;
    }}
    .st-emotion-cache-ocqkz7.e1f1d6gn4 > div:last-child .stButton > button:hover {{
        background-color: {accent_color}20;
        box-shadow: none;
        color: {accent_color};
    }}

    /* Forgot password button as a link */
    .forgot-password-link-btn > button {{
        background-color: transparent !important;
        color: {text_color}88 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 5px 10px !important; /* Smaller padding for link style */
        font-size: 14px !important;
        text-decoration: underline;
        width: auto !important; /* Size to content */
        margin-top: 10px !important; /* Space above */
        transition: color 0.2s ease;
    }}
    .forgot-password-link-btn > button:hover {{
        color: {accent_color} !important;
        background-color: transparent !important;
        text-decoration: underline;
    }}

    /* Header styling */
    .header-content {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-bottom: 20px; /* Space below header */
    }}

    .app-logo {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover; /* Ensures image fits well */
        margin-right: 15px; /* Space between logo and title */
    }}

    .app-title {{
        font-size: 28px;
        font-weight: 700;
        color: {text_color};
        margin: 0;
    }}
    
    /* Login heading */
    .login-heading {{
        font-size: 22px;
        font-weight: 500;
        color: {text_color};
        margin-bottom: 15px; /* Space below heading */
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Theme toggle button specific styling */
    .theme-toggle-btn > button {{
        background-color: {input_bg_color};
        color: {text_color};
        border: 1px solid {input_border_color};
        border-radius: 20px;
        padding: 8px 12px;
        font-size: 14px;
        gap: 5px;
        width: auto;
        box-shadow: none;
        transition: all 0.2s ease;
    }}
    .theme-toggle-btn > button:hover {{
        background-color: {accent_color}20;
        border-color: {accent_color};
        color: {text_color};
    }}

    /* Hide the default separator */
    hr {{
        display: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- LOGIN FUNCTION ----------
def login():
    # Initialize session state for dark mode if not already present
    if "modo_oscuro" not in st.session_state:
        st.session_state.modo_oscuro = False

    # Inject CSS (must be called inside the function to use session state for theme)
    inject_custom_css(st.session_state.modo_oscuro)

    # Set page config once at the beginning
    st.set_page_config(
        layout="centered",
        initial_sidebar_state="collapsed",
        page_title="Biblioteca Alejandría - Iniciar Sesión"
    )

    # --- Layout and Content ---
    # Use st.container for the card effect. Streamlit applies its own internal class.
    # We will target this class with CSS for the card effect.
    with st.container(): # This will become the 'login-card-container' visually

        # Header Section (Logo, Title, and Theme Button)
        header_area = st.empty() # Placeholder for the header and theme toggle
        with header_area.container():
            col_logo, col_title, col_theme_toggle = st.columns([1, 4, 1.5]) # Adjusted ratios

            with col_logo:
                # Replace with actual image path or URL if you have one
                st.image("https://via.placeholder.com/50", use_column_width=False, output_format="PNG", caption="") # Placeholder image
                # OR: st.markdown('<img src="your_logo_url_here.png" class="app-logo">', unsafe_allow_html=True)
            with col_title:
                st.markdown('<p class="app-title">Biblioteca Alejandría</p>', unsafe_allow_html=True)
            with col_theme_toggle:
                st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True)
                theme_icon = "☀️" if not st.session_state.modo_oscuro else "🌙"
                if st.button(f"{theme_icon} Tema", key="theme_toggle_main_btn"): # Unique key
                    st.session_state.modo_oscuro = not st.session_state.modo_oscuro
                    st.rerun() # Rerun to apply theme changes
                st.markdown('</div>', unsafe_allow_html=True)

        # Login Heading
        st.markdown('<h3 class="login-heading">🔐 Iniciar sesión</h3>', unsafe_allow_html=True)
        # st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True) # Small spacer

        # Input Fields (preserving original Streamlit calls and functionality)
        correo = st.text_input("Correo electrónico", placeholder="Correo electrónico", key="login_email_input_final")
        contrasena = st.text_input("Contraseña", placeholder="Contraseña", type="password", key="login_password_input_final")

        acceso = False
        usuario = None

        # Two columns for Login and Register buttons
        col_btn_login, col_btn_register = st.columns(2)

        with col_btn_login:
            if st.button("Iniciar sesión", key="login_submit_btn_final"): # UNIQUE KEY
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    datos = doc.to_dict()
                    if datos["contrasena"] == contrasena:
                        st.success(f"Bienvenido, {datos['nombre']} 👋")
                        acceso = True
                        usuario = datos
                        st.session_state.logged_in = True
                        st.session_state.logged_user_name = datos['nombre']
                        st.session_state.vista = "dashboard" # Redirect
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

        with col_btn_register:
            if st.button("Registrarse", key="register_button_final"): # UNIQUE KEY
                st.session_state.vista = "registro"
                st.rerun()

        # Small spacer between buttons and forgot password link
        # st.markdown('<div style="height:15px;"></div>', unsafe_allow_html=True)

        # Forgot password button (unique key, styled as a link)
        st.markdown('<div class="forgot-password-link-btn">', unsafe_allow_html=True)
        if st.button("¿Olvidaste tu contraseña?", key="forgot_password_button_final"): # UNIQUE KEY
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario

# ---------- MAIN APPLICATION FLOW (UNCHANGED FUNCTIONALITY) ----------
if __name__ == "__main__":
    if "vista" not in st.session_state:
        st.session_state.vista = "login"
    
    # Initialize logged_in state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Conditional rendering based on view
    if st.session_state.vista == "login":
        login()
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro. (Implementa tu lógica aquí)")
        if st.button("Volver al Login", key="back_from_register_page_final"):
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña. (Implementa tu lógica aquí)")
        if st.button("Volver al Login", key="back_from_recovery_page_final"):
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "dashboard":
        # Ensure user is logged in to see dashboard
        if st.session_state.get('logged_in'):
            st.title(f"🎉 Bienvenido al Dashboard, {st.session_state.get('logged_user_name', 'usuario')}!")
            st.write("¡Has iniciado sesión exitosamente!")
            st.write("Este es tu espacio personal.")
            if st.button("Cerrar Sesión", key="logout_dashboard_final"):
                del st.session_state.logged_in
                if 'logged_user_name' in st.session_state:
                    del st.session_state.logged_user_name
                st.session_state.vista = "login"
                st.rerun()
        else:
            # If somehow they reach dashboard without being logged in, redirect to login
            st.warning("No has iniciado sesión. Por favor, inicia sesión para acceder al dashboard.")
            st.session_state.vista = "login"
            st.rerun()