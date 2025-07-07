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

    # Estilos personalizados
    st.markdown(f"""
        <style>
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid {borde};
            border-radius: 8px;
            padding: 8px;
        }}
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label {{
            color: {texto};
            font-weight: bold;
        }}
        .stMarkdown h2 {{
            color: {texto};
        }}
        .stButton > button {{
            background-color: #44bba4;
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
        }}
        .stButton > button:hover {{
            background-color: #379d8e;
        }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='max-width: 800px; margin: auto; padding: 20px;'>", unsafe_allow_html=True)

        st.subheader("Mi perfil")

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
            st.success("Perfil actualizado correctamente")
            st.session_state.usuario.update(datos_actualizados)

        st.markdown(f"<p style='color:{texto}; font-weight:bold;'>Correo: {correo} (no se puede modificar)</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
