import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def mostrar_perfil(usuario):
    # Detectar modo oscuro
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde = "#44bba4"
    mensaje_color = texto
    fondo_mensaje = "#d4edda"

    # Estilo personalizado
    st.markdown(f"""
        <style>
        .stTextInput > div > input,
        .stNumberInput input,
        .stSelectbox div {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid {borde};
            border-radius: 8px;
            padding: 8px;
        }}

        .guardar-btn > button {{
            background-color: #44bba4;
            color: white;
            font-weight: bold;
            padding: 8px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }}

        .guardar-btn > button:hover {{
            background-color: #379d8e;
        }}

        .correo-texto {{
            font-size: 16px;
            color: {texto};
            background-color: transparent;
            padding: 8px 0;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Contenedor centrado
    with st.container():
        st.markdown(
            """
            <div style='max-width: 800px; margin: auto; padding: 20px;'>
            """,
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

        # Botón guardar con mensaje personalizado
        st.markdown('<div class="guardar-btn">', unsafe_allow_html=True)
        if st.button("Guardar cambios"):
            datos_actualizados = {
                "nombre": nombre,
                "apellido": apellido,
                "edad": edad,
                "genero": genero
            }
            db.collection("usuarios").document(correo).update(datos_actualizados)
            st.session_state.usuario.update(datos_actualizados)

            st.markdown(f"""
                <div style="background-color: {fondo_mensaje}; color: {mensaje_color}; 
                            padding: 10px 20px; border-radius: 10px; 
                            font-weight: bold; text-align: center; margin-top: 10px;">
                    Perfil actualizado correctamente
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Mostrar correo sin fondo ni emoji
        st.markdown(f"<div class='correo-texto'>Correo: <code>{correo}</code> (no se puede modificar)</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
