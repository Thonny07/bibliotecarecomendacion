import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json  # Necesario para convertir el secret

# Inicializa Firebase solo una vez
if not firebase_admin._apps:
    firebase_config_str = st.secrets["FIREBASE_CONFIG"]
    firebase_config = json.loads(firebase_config_str)
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- REGISTRO ----------
def registrar_usuario():
    st.subheader("📝 Registro de nuevo usuario")

    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    edad = st.number_input("Edad", min_value=10, max_value=100, step=1)
    genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
    correo = st.text_input("Correo electrónico")

    col1, col2 = st.columns([4, 1])
    with col1:
        contrasena = st.text_input("Contraseña", type="password")
    with col2:
        mostrar = st.checkbox("👁️", help="Mostrar contraseña")
    if mostrar:
        contrasena = st.text_input("Contraseña (visible)", type="default")

    if st.button("Registrar"):
        if len(contrasena) < 6:
            st.error("⚠️ La contraseña debe tener al menos 6 caracteres.")
        elif not nombre or not apellido or not correo:
            st.warning("⚠️ Por favor completa todos los campos obligatorios.")
        else:
            doc_ref = db.collection("usuarios").document(correo)
            if doc_ref.get().exists:
                st.warning("⚠️ Este correo ya está registrado.")
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
