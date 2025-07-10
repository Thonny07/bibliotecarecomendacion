import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import json

if not firebase_admin._apps:
    firebase_config_str = st.secrets["FIREBASE_CONFIG"]
    firebase_config = json.loads(firebase_config_str)
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def aplicar_estilos():
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    color_alerta = "#ffffff" if modo_oscuro else "#000000"

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo};
            color: {texto};
        }}
        .stTextInput input {{
            background-color: transparent;
            color: {texto};
            border: 1px solid #20c997;
            border-radius: 8px;
            padding: 8px;
        }}
        .stAlert-success p, .stAlert-error p {{
            color: {color_alerta} !important;
        }}
        .stButton>button {{
            background-color: #20c997 !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            width: 100%;
        }}
        .stButton>button:hover {{
            background-color: #17a88b !important;
        }}
        label {{
            color: {texto} !important;
            font-weight: bold;
        }}
        .mensaje-personalizado {{
            color: {color_alerta};
            font-size: 1.1rem;
            font-weight: bold;
            margin-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

def enviar_codigo_smtp(destinatario, codigo):
    try:
        remitente = st.secrets["EMAIL"]
        password = st.secrets["EMAIL_PASSWORD"]

        mensaje = MIMEMultipart()
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = "Código de verificación - Recuperar contraseña"

        cuerpo = f"""
        <html>
        <body>
            <h3>Tu código de verificación es:</h3>
            <h2>{codigo}</h2>
            <p>Úsalo para recuperar tu contraseña en la app de biblioteca.</p>
        </body>
        </html>
        """

        mensaje.attach(MIMEText(cuerpo, "html"))

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
        return True
    except Exception as e:
        st.error(f"Error al enviar correo: {e}")
        return False

def recuperar_contrasena():
    aplicar_estilos()
    st.subheader("Recuperar contraseña")

    if "codigo_enviado" not in st.session_state:
        st.session_state.codigo_enviado = False
    if "correo_recuperar" not in st.session_state:
        st.session_state.correo_recuperar = ""
    if "codigo_verificacion" not in st.session_state:
        st.session_state.codigo_verificacion = ""

    if not st.session_state.codigo_enviado:
        with st.form("form_enviar_codigo"):
            correo = st.text_input("Ingrese su correo registrado")
            col1, col2 = st.columns([1, 1])
            with col1:
                enviar = st.form_submit_button("Enviar código")
            with col2:
                volver = st.form_submit_button("Volver al login")

            if enviar:
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    codigo = str(random.randint(100000, 999999))
                    st.session_state.codigo_verificacion = codigo
                    st.session_state.correo_recuperar = correo

                    if enviar_codigo_smtp(correo, codigo):
                        st.success("Código enviado al correo")
                        st.session_state.codigo_enviado = True
                        st.rerun()
                else:
                    st.markdown(
                        f'<div class="mensaje-personalizado">Este correo no está registrado</div>',
                        unsafe_allow_html=True
                    )
            elif volver:
                st.session_state.vista = "login"
                st.rerun()

    else:
        st.markdown("### Verifica tu código y crea una nueva contraseña")
        st.markdown(
            f'<div class="mensaje-personalizado">Código enviado a: {st.session_state.correo_recuperar}</div>',
            unsafe_allow_html=True
        )

        with st.form("form_verificar_codigo"):
            codigo_ingresado = st.text_input("Ingresa el código recibido")
            nueva_contrasena = st.text_input("Nueva contraseña", type="password")
            col1, col2 = st.columns([1, 1])
            with col1:
                cambiar = st.form_submit_button("Cambiar contraseña")
            with col2:
                volver = st.form_submit_button("Volver al login")

            if cambiar:
                if codigo_ingresado == st.session_state.codigo_verificacion:
                    doc_ref = db.collection("usuarios").document(st.session_state.correo_recuperar)
                    doc_ref.update({"contrasena": nueva_contrasena})
                    st.success("Contraseña actualizada correctamente")
                    st.session_state.vista = "login"
                    st.session_state.codigo_enviado = False
                    st.session_state.codigo_verificacion = ""
                    st.session_state.correo_recuperar = ""
                    st.rerun()
                else:
                    st.error("Código incorrecto")
            elif volver:
                st.session_state.vista = "login"
                st.session_state.codigo_enviado = False
                st.session_state.codigo_verificacion = ""
                st.session_state.correo_recuperar = ""
                st.rerun()
