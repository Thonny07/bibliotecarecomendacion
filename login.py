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

    /* Remove Streamlit's default padding on the main content block to allow full centering */
    .main .block-container {{
        padding-top: 0rem;
        padding-bottom: 0rem;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        min-height: 100vh;
    }}

    /* The Login Card Container (st.container default class) */
    /* Adjust this class name if inspection shows a different one for st.container */
    .st-emotion-cache-nahz7x {{ /* Common class for the st.container wrapper */
        background-color: {card_bg_color};
        padding: 40px; /* Internal padding for the card */
        border-radius: 12px;
        box-shadow: 0 10px 30px {shadow_color};
        width: 100%;
        max-width: 450px; /* Control card width */
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
        /* Use flexbox for internal vertical spacing and alignment */
        display: flex;
        flex-direction: column;
        align-items: center; /* Center items horizontally within the card */
        gap: 20px; /* Space between main elements inside the card */
    }}
    
    /* Input field styling - Avoid manipulating width/height/padding here */
    .stTextInput > label {{
        display: none; /* Hide default labels */
    }}
    .stTextInput > div > div > input {{
        background-color: {input_bg_color};
        border: 1px solid {input_border_color};
        border-radius: 8px;
        font-size: 16px;
        color: {text_color};
        /* NO FIXED PADDING/WIDTH HERE - LET STREAMLIT HANDLE IT */
        /* Use transition for smooth color changes */
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

    /* Buttons general style - Avoid manipulating width/height/padding here */
    .stButton > button {{
        background-color: {accent_color};
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease, color 0.2s ease;
        box-shadow: 0 4px 10px {accent_color}40;
        /* NO FIXED PADDING/WIDTH/MARGIN HERE - LET STREAMLIT HANDLE IT */
    }}

    .stButton > button:hover {{
        background-color: {button_hover_bg};
        box-shadow: 0 6px 15px {accent_color}60;
    }}

    /* Adjust columns for buttons to control gap */
    /* Target the specific column container */
    [data-testid="stHorizontalBlock"] {{
        width: 100%; /* Ensure columns take full width within the card */
        justify-content: space-between; /* Distribute content */
        gap: 15px; /* Smaller gap between login and register buttons */
    }}
    /* This rule ensures buttons inside columns take full width of their column */
    [data-testid="stHorizontalBlock"] > div > div > button {{
        width: 100%;
    }}

    /* Specific style for 'Registrarse' button in columns */
    /* This targets the button in the second column more reliably */
    [data-testid="stHorizontalBlock"] > div:last-child .stButton > button {{
        background-color: transparent;
        color: {accent_color};
        border: 1px solid {accent_color};
        box-shadow: none;
    }}
    [data-testid="stHorizontalBlock"] > div:last-child .stButton > button:hover {{
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
        font-size: 14px !important;
        text-decoration: underline;
        /* NO FIXED PADDING/WIDTH/MARGIN HERE - LET STREAMLIT HANDLE IT */
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
        justify-content: center; /* Center header content */
        width: 100%; /* Take full width of parent container */
        gap: 15px; /* Space between logo and title */
        margin-bottom: 10px; /* Space below header content */
    }}

    .app-logo {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover; /* Ensures image fits well */
    }}

    .app-title {{
        font-size: 28px;
        font-weight: 700;
        color: {text_color};
        margin: 0; /* Remove default margins */
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
        width: 100%; /* Ensure it spans width within card */
        justify-content: center; /* Center the heading text itself */
    }}

    /* Theme toggle button styling (now within a column) */
    .theme-toggle-btn > button {{
        background-color: {input_bg_color};
        color: {text_color};
        border: 1px solid {input_border_color};
        border-radius: 20px;
        padding: 8px 12px;
        font-size: 14px;
        gap: 5px;
        width: auto; /* Allow Streamlit to determine width */
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

# ---------- LOGIN FUNCTION (Integrates design but retains original core logic) ----------
def login():
    # Initialize session state for dark mode if not already present
    if "modo_oscuro" not in st.session_state:
        st.session_state.modo_oscuro = False

    # Inject CSS (must be called inside the function to use session state for theme)
    inject_custom_css(st.session_state.modo_oscuro)

    # Set page config once at the beginning
    st.set_page_config(
        layout="centered", # Best for a single form card
        initial_sidebar_state="collapsed",
        page_title="Biblioteca Alejandría - Iniciar Sesión"
    )

    # --- Layout and Content ---
    # Use st.container for the card effect. Streamlit applies its own internal class.
    # This acts as the visual 'card'
    with st.container():
        # Header Section (Logo, Title, and Theme Button)
        # We will use columns to lay these out horizontally.
        # The 'app-logo' class will size the image correctly.
        col_logo, col_title, col_theme_toggle = st.columns([1, 3, 1.2]) # Adjusted ratios

        with col_logo:
            # Using st.image for robust logo display. Replace URL with your actual logo path/URL.
            # You can also use a local file: st.image("logo.png", use_column_width=False, width=50)
            st.image("https://via.placeholder.com/50/007BFF/FFFFFF?text=Logo", use_column_width=False, output_format="PNG", caption="", clamp=True)

        with col_title:
            st.markdown('<p class="app-title">Biblioteca Alejandría</p>', unsafe_allow_html=True)

        with col_theme_toggle:
            st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True) # Apply CSS class for styling
            theme_icon = "☀️" if not st.session_state.modo_oscuro else "🌙"
            if st.button(f"{theme_icon} Tema", key="theme_toggle_btn_main_final"): # UNIQUE KEY
                st.session_state.modo_oscuro = not st.session_state.modo_oscuro
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Login Heading (centered by flexbox in card container)
        st.markdown('<h3 class="login-heading">🔐 Iniciar sesión</h3>', unsafe_allow_html=True)

        # Input Fields (original logic)
        # The 'placeholder' argument adds the hint text directly.
        correo = st.text_input("Correo electrónico", placeholder="Correo electrónico", key="login_email_input_final_v2") # UNIQUE KEY
        contrasena = st.text_input("Contraseña", placeholder="Contraseña", type="password", key="login_password_input_final_v2") # UNIQUE KEY

        col1, col2 = st.columns(2) # Original column structure for buttons
        acceso = False
        usuario = None

        with col1:
            if st.button("Iniciar sesión", key="login_submit_btn_final_v2"): # UNIQUE KEY
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    datos = doc.to_dict()
                    if datos["contrasena"] == contrasena:
                        st.success(f"Bienvenido, {datos['nombre']} 👋")
                        acceso = True
                        usuario = datos
                        st.session_state.logged_in = True # Set session state
                        st.session_state.logged_user_name = datos['nombre']
                        st.session_state.vista = "dashboard" # Navigate
                        st.rerun() # Trigger a rerun to change view
                    else:
                        st.error("❌ Contraseña incorrecta")
                else:
                    st.error("❌ Usuario no encontrado")

        with col2:
            if st.button("Registrarse", key="register_button_final_v2"): # UNIQUE KEY
                st.session_state.vista = "registro"
                st.rerun() # Trigger a rerun to change view

        # Forgot password button (original logic)
        # st.markdown("---") # Removed this for cleaner look, as requested
        st.markdown('<div class="forgot-password-link-btn">', unsafe_allow_html=True) # Apply CSS class
        if st.button("¿Olvidaste tu contraseña?", key="forgot_password_button_final_v2"): # UNIQUE KEY
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.session_state.vista = "recuperar"
            st.rerun() # Trigger a rerun to change view
        st.markdown('</div>', unsafe_allow_html=True)

    return acceso, usuario

# ---------- MAIN APPLICATION FLOW (UNCHANGED FUNCTIONALITY) ----------
if __name__ == "__main__":
    # Initialize session state variables if they don't exist
    if "vista" not in st.session_state:
        st.session_state.vista = "login"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "logged_user_name" not in st.session_state:
        st.session_state.logged_user_name = ""

    # Conditional rendering based on the current view
    if st.session_state.vista == "login":
        login()
    elif st.session_state.vista == "registro":
        st.title("Página de Registro")
        st.write("Aquí iría el formulario de registro. (Implementa tu lógica aquí)")
        if st.button("Volver al Login", key="back_from_register_page_final_v2"): # UNIQUE KEY
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "recuperar":
        st.title("Recuperar Contraseña")
        st.write("Aquí iría el proceso para recuperar la contraseña. (Implementa tu lógica aquí)")
        if st.button("Volver al Login", key="back_from_recovery_page_final_v2"): # UNIQUE KEY
            st.session_state.vista = "login"
            st.rerun()
    elif st.session_state.vista == "dashboard":
        # Ensure user is logged in to see dashboard, otherwise redirect
        if st.session_state.get('logged_in'):
            st.title(f"🎉 Bienvenido al Dashboard, {st.session_state.get('logged_user_name', 'usuario')}!")
            st.write("¡Has iniciado sesión exitosamente!")
            st.write("Este es tu espacio personal.")
            if st.button("Cerrar Sesión", key="logout_dashboard_final_v2"): # UNIQUE KEY
                del st.session_state.logged_in
                if 'logged_user_name' in st.session_state:
                    del st.session_state.logged_user_name
                st.session_state.vista = "login"
                st.rerun()
        else:
            st.warning("No has iniciado sesión. Por favor, inicia sesión para acceder al dashboard.")
            st.session_state.vista = "login"
            st.rerun()