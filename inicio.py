import streamlit as st
from PIL import Image
import login
import registro
import inicio
import recuperar
import perfil
from acciones_libros import obtener_libros_guardados

# Configurar página
st.set_page_config(layout="wide", page_title="Biblioteca Alejandría")

# Estado inicial
if "vista" not in st.session_state:
    st.session_state.vista = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

# Tema visual dinámico
def aplicar_tema():
    modo = st.session_state.modo_oscuro
    st.markdown(
        f"""
        <style>
        html, body, .stApp {{
            background-color: {"#1e1e1e" if modo else "white"} !important;
            color: {"white" if modo else "black"} !important;
        }}
        .stTextInput>div>div>input,
        .stTextArea>div>textarea,
        .stSelectbox>div>div>div>div,
        .stRadio>div>label,
        .stButton>button {{
            background-color: {"#2a2a2a" if modo else "#f9f9f9"} !important;
            color: {"white" if modo else "black"} !important;
            border: 1px solid {"#ccc" if not modo else "#555"} !important;
            border-radius: 8px !important;
        }}
        .sidebar .sidebar-content {{
            background-color: #c7f3ef !important;
        }}
        .stSidebar {{
            background-color: #c7f3ef !important;
        }}
        </style>
        """, unsafe_allow_html=True
    )

aplicar_tema()

# Header con logo
col_logo, col_titulo, col_vacio = st.columns([1, 4, 1])
with col_logo:
    try:
        logo = Image.open("logobiblioteca.png")
        st.image(logo, width=80)
    except:
        pass
with col_titulo:
    st.markdown(
        "<h1 style='text-align: center; color: #1abc9c; font-size: 36px;'>Biblioteca Alejandría</h1>",
        unsafe_allow_html=True
    )

# Menú lateral si hay sesión
if st.session_state.usuario and st.session_state.vista not in ["recuperar", "registro"]:
    st.sidebar.markdown("### Menú")
    opcion = st.sidebar.selectbox("", ["Inicio", "Mis libros guardados", "Mi perfil", "Cerrar sesión"])

    if opcion == "Inicio":
        st.session_state.vista = "inicio"
    elif opcion == "Mis libros guardados":
        st.session_state.vista = "guardados"
    elif opcion == "Mi perfil":
        st.session_state.vista = "perfil"
    elif opcion == "Cerrar sesión":
        st.session_state.vista = "login"
        st.session_state.usuario = None
        st.rerun()

# Botón tema modo claro/oscuro (con icono no emoji)
col_esquina = st.columns([12, 1])[1]
with col_esquina:
    if st.button("", key="toggle_tema", help="Cambiar tema"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

# Control de navegación
vista = st.session_state.vista
usuario = st.session_state.usuario

if vista == "login":
    acceso, user = login.login()
    if acceso:
        st.session_state.usuario = user
        st.session_state.vista = "inicio"
        st.rerun()

elif vista == "registro":
    registro.registrar_usuario()

elif vista == "recuperar":
    recuperar.recuperar_contrasena()

elif vista == "inicio":
    inicio.pantalla_inicio(usuario)

elif vista == "perfil":
    perfil.mostrar_perfil(usuario)

elif vista == "guardados":
    st.title("Mis libros guardados")
    libros = obtener_libros_guardados(usuario["correo"])

    if libros:
        for i, libro in enumerate(libros):
            st.markdown("---")
            cols = st.columns([1, 5, 1])

            with cols[0]:
                if libro["imagen"]:
                    st.image(libro["imagen"], width=100)

            with cols[1]:
                st.subheader(libro["titulo"])
                st.markdown(f"**Autores:** {libro.get('autores', 'Desconocido')}")
                with st.expander("Descripción"):
                    st.write(libro["descripcion"])

            with cols[2]:
                if st.button("Leer", key=f"leer_{i}"):
                    url_google = f"https://www.google.com/search?q={libro['titulo'].replace(' ', '+')}"
                    st.markdown(f"[Abrir libro en Google Books]({url_google})", unsafe_allow_html=True)

                if st.button("Eliminar", key=f"eliminar_{i}"):
                    from acciones_libros import eliminar_libro_guardado
                    eliminar_libro_guardado(usuario["correo"], libro["titulo"])
                    st.success("Libro eliminado.")
                    st.rerun()
    else:
        st.info("No has guardado ningún libro aún.")
