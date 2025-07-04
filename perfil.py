import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def mostrar_perfil(usuario):
    # Contenedor centrado y más amplio
    with st.container():
        st.markdown(
            """
            <div style='max-width: 800px; margin: auto; padding: 20px;'>
            """,
            unsafe_allow_html=True
        )

        st.subheader("👤 Mi perfil")

        correo = usuario["correo"]
        nombre = st.text_input("Nombre", value=usuario["nombre"])
        apellido = st.text_input("Apellido", value=usuario["apellido"])
        edad = st.number_input("Edad", min_value=1, max_value=120, value=usuario.get("edad", 18))
        genero = st.selectbox(
            "Género",
            ["Masculino", "Femenino", "Otro"],
            index=["Masculino", "Femenino", "Otro"].index(usuario.get("genero", "Otro"))
        )

        if st.button("💾 Guardar cambios"):
            datos_actualizados = {
                "nombre": nombre,
                "apellido": apellido,
                "edad": edad,
                "genero": genero
            }
            db.collection("usuarios").document(correo).update(datos_actualizados)
            st.success("✅ Perfil actualizado correctamente")
            st.session_state.usuario.update(datos_actualizados)

        st.markdown(f"📧 Correo: `{correo}` (no se puede modificar)")

        st.markdown("---")
        if st.button("⬅️ Volver a inicio"):
            st.session_state.vista = "inicio"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
