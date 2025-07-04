import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json  # Necesario para convertir string a dict

# ✅ Inicializa Firebase desde secrets de Streamlit
if not firebase_admin._apps:
    firebase_config = json.loads(st.secrets["FIREBASE_CONFIG"])  # OJO: mayúsculas aquí
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------- LOGIN ----------
def login():
    st.subheader("🔐 Iniciar sesión")
    
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns(2)
    acceso = False
    usuario = None

    with col1:
        if st.button("Iniciar sesión"):
            doc = db.collection("usuarios").document(correo).get()
            if doc.exists:
                datos = doc.to_dict()
                if datos["contrasena"] == contrasena:
                    st.success(f"Bienvenido, {datos['nombre']} 👋")
                    acceso = True
                    usuario = datos
                else:
                    st.error("❌ Contraseña incorrecta")
            else:
                st.error("❌ Usuario no encontrado")

    with col2:
        if st.button("Registrarse"):
            st.session_state.vista = "registro"
            st.rerun()

    # Recuperar contraseña
    st.markdown("---")
    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    return acceso, usuario
