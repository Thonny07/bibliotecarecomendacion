import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import random
import requests

# -------- Inicializar Firebase solo una vez --------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# -------- Envío de código con Nodemailer --------
def enviar_codigo_api(correo, codigo):
    try:
        url = "http://localhost:3001/enviar-correo"
        datos = {
            "destinatario": correo,
            "codigo": codigo
        }
        r = requests.post(url, json=datos)
        if r.status_code == 200:
            return True
        else:
            st.error("❌ No se pudo enviar el correo desde el servidor.")
            return False
    except Exception as e:
        st.error(f"Error al conectar con el servidor de correo: {e}")
        return False

# -------- Función principal --------
def recuperar_contrasena():
    st.subheader("🔑 Recuperar contraseña")

    # Inicializar estado
    if "codigo_enviado" not in st.session_state:
        st.session_state.codigo_enviado = False
    if "correo_recuperar" not in st.session_state:
        st.session_state.correo_recuperar = ""
    if "codigo_verificacion" not in st.session_state:
        st.session_state.codigo_verificacion = ""

    # -------- Paso 1: Enviar código --------
    if not st.session_state.codigo_enviado:
        with st.form("form_enviar_codigo"):
            correo = st.text_input("📧 Ingrese su correo registrado")
            enviar = st.form_submit_button("📤 Enviar código")

            if enviar:
                doc = db.collection("usuarios").document(correo).get()
                if doc.exists:
                    codigo = str(random.randint(100000, 999999))
                    st.session_state.codigo_verificacion = codigo
                    st.session_state.correo_recuperar = correo

                    exito = enviar_codigo_api(correo, codigo)
                    if exito:
                        st.success("✅ Código enviado al correo")
                        st.session_state.codigo_enviado = True
                        st.rerun()
                else:
                    st.error("❌ Este correo no está registrado")

    # -------- Paso 2: Verificar código y cambiar contraseña --------
    else:
        st.markdown("### 🧾 Verifica tu código y crea una nueva contraseña")
        st.info(f"📩 Código enviado a: {st.session_state.correo_recuperar}")

        with st.form("form_verificar_codigo"):
            codigo_ingresado = st.text_input("🔐 Ingresa el código recibido")
            nueva_contrasena = st.text_input("🔏 Nueva contraseña", type="password")
            cambiar = st.form_submit_button("🔁 Cambiar contraseña")

            if cambiar:
                if codigo_ingresado == st.session_state.codigo_verificacion:
                    doc_ref = db.collection("usuarios").document(st.session_state.correo_recuperar)
                    doc_ref.update({"contrasena": nueva_contrasena})
                    st.success("✅ Contraseña actualizada correctamente")

                    # Limpiar estados y volver al login
                    st.session_state.vista = "login"
                    st.session_state.codigo_enviado = False
                    st.session_state.codigo_verificacion = ""
                    st.session_state.correo_recuperar = ""
                    st.rerun()
                else:
                    st.error("❌ Código incorrecto")

        st.markdown("---")
        if st.button("⬅️ Volver al login"):
            st.session_state.vista = "login"
            st.session_state.codigo_enviado = False
            st.session_state.codigo_verificacion = ""
            st.session_state.correo_recuperar = ""
            st.rerun()
