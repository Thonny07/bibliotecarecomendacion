import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


# ---------- INICIALIZAR FIREBASE ----------
if not firebase_admin._apps:
    try:
        firebase_config = st.secrets["FIREBASE_CONFIG"]

        # 🔍 Verificar tipo de dato (solo para depuración, puedes eliminarlo luego)
        print("Tipo de FIREBASE_CONFIG:", type(firebase_config))  # Esperado: <class 'dict'>

        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error("❌ Error al conectar con Firebase. Verifica tu secrets.toml.")
        st.stop()

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

    # Opción de recuperación de contraseña
    st.markdown("---")
    if st.button("¿Olvidaste tu contraseña?"):
        st.session_state.codigo_enviado = False
        st.session_state.codigo_verificacion = ""
        st.session_state.correo_recuperar = ""
        st.session_state.vista = "recuperar"
        st.rerun()

    return acceso, usuario
