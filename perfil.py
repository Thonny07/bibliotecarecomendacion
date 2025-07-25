import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def mostrar_perfil(usuario):
    modo_oscuro = st.session_state.get("modo_oscuro", False)

    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde = "#44bba4"
    mensaje_color = texto
    fondo_mensaje = "#d4edda" if not modo_oscuro else "#2e2e2e"

    st.markdown(f"""
        <style>
        .stTextInput > div > input,
        .stNumberInput input,
        .stSelectbox div {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid {borde};
            border-radius: 8px;
        }}

        /* === BOTÓN ESTILO VERDE AGUA === */
        div.stButton > button {{
            background-color: #20c997 !important;
            color: white !important;
            font-weight: bold;
            padding: 8px 20px;
            border-radius: 8px;
            margin-top: 10px;
            border: none;
        }}
        div.stButton > button:hover {{
            background-color: #17a88b !important;
            color: white !important;
        }}

        .correo-label {{
            font-size: 16px;
            color: {texto};
            margin-top: 15px;
        }}

        .mensaje-exito {{
            background-color: {fondo_mensaje};
            color: {mensaje_color};
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(
            "<div style='max-width: 800px; margin: auto; padding: 20px;'>",
            unsafe_allow_html=True
        )

        st.title("Mi perfil")

        correo = usuario["correo"]
        nombre = st.text_input("Nombre", value=usuario["nombre"])
        apellido = st.text_input("Apellido", value=usuario["apellido"])
        edad = st.number_input("Edad", min_value=1, max_value=120, value=usuario.get("edad", 18))
        genero = st.selectbox(
            "Género",
            ["Masculino", "Femenino", "Otro"],
            index=["Masculino", "Femenino", "Otro"].index(usuario.get("genero", "Otro"))
        )

        if st.button("Guardar cambios"):
            datos_actualizados = {
                "nombre": nombre,
                "apellido": apellido,
                "edad": edad,
                "genero": genero
            }
            db.collection("usuarios").document(correo).update(datos_actualizados)
            st.session_state.usuario.update(datos_actualizados)

            st.markdown('<div class="mensaje-exito">Perfil actualizado correctamente</div>', unsafe_allow_html=True)

        st.markdown(f"<div class='correo-label'>Correo: {correo} (no se puede modificar)</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
