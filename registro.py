import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
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
    fondo_input = "#333333" if modo_oscuro else "#ffffff"
    borde = "#20c997"
    color_alerta = texto

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo};
            color: {texto};
        }}
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"],
        input[type="number"] {{
            background-color: {fondo_input};
            color: {texto} !important;
            border: 1px solid {borde};
            border-radius: 8px;
            padding: 8px;
        }}
        input[type="number"]::-webkit-inner-spin-button,
        input[type="number"]::-webkit-outer-spin-button {{
            -webkit-appearance: none;
            margin: 0;
        }}
        label {{
            color: {texto} !important;
            font-weight: bold;
        }}
        .stButton>button {{
            background-color: #20c997 !important;
            color: white !important;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #17a88b !important;
        }}
        .mensaje-personalizado {{
            color: {color_alerta};
            font-size: 1rem;
            font-weight: bold;
            margin-top: 10px;
        }}
        .botones-centrados {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1.5rem;
        }}
        </style>
    """, unsafe_allow_html=True)

def registrar_usuario():
    aplicar_estilos()
    st.subheader("Registro de nuevo usuario")

    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    edad = st.number_input("Edad", min_value=10, max_value=100, step=1)
    genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    st.markdown('<div class="botones-centrados">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registrar"):
            if len(contrasena) < 6:
                st.markdown('<div class="mensaje-personalizado">La contraseña debe tener al menos 6 caracteres.</div>', unsafe_allow_html=True)
            elif not nombre or not apellido or not correo:
                st.markdown('<div class="mensaje-personalizado">Por favor completa todos los campos obligatorios.</div>', unsafe_allow_html=True)
            else:
                doc_ref = db.collection("usuarios").document(correo)
                if doc_ref.get().exists:
                    st.markdown('<div class="mensaje-personalizado">Este correo ya está registrado.</div>', unsafe_allow_html=True)
                else:
                    doc_ref.set({
                        "nombre": nombre,
                        "apellido": apellido,
                        "edad": edad,
                        "genero": genero,
                        "correo": correo,
                        "contrasena": contrasena,
                        "fecha_registro": datetime.now()
                    })
                    st.success("✅ Usuario registrado con éxito")
                    st.session_state.vista = "login"
                    st.rerun()

    with col2:
        if st.button("Volver al login"):
            st.session_state.vista = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
