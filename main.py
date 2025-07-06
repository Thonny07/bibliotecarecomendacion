import streamlit as st
from PIL import Image
import login
import registro
import inicio
import recuperar
import perfil
from acciones_libros import obtener_libros_guardados

# Configuración de la página
st.set_page_config(layout="wide")

# Estado inicial del tema
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

# Aplicar tema visual
def aplicar_tema():
    if st.session_state.modo_oscuro:
        st.markdown("""
            <style>
            html, body, .stApp {
                background-color: #1e1e1e !important;
                color: white !important;
            }
            .stTextInput input, .stTextArea textarea, .stSelectbox div {
                background-color: #333333 !important;
                color: white !important;
                border: 1px solid #888 !important;
                border-radius: 8px;
            }
            .stSidebar {
                background-color: #a2ded0 !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            html, body, .stApp {
                background-color: white !important;
                color: black !important;
            }
            .stTextInput input, .stTextArea textarea, .stSelectbox div {
                background-color: #ffffff !important;
                color: black !important;
                border: 1px solid #ccc !important;
                border-radius: 8px;
            }
            .stSidebar {
                background-color: #a2ded0 !important;
            }
            </style>
        """, unsafe_allow_html=True)

aplicar_tema()

# Encabezado con logo circular, título centrado y botón de tema a la derecha
try:
    logo = Image.open("logobiblioteca.png")
    col1, col2, col3 = st.columns([1.5, 5, 1.5])
    with col2:
        col_logo, col_texto = st.columns([1, 5])
        with col_logo:
            st.image(logo, width=80)
        with col_texto:
            st.markdown("<h1 style='margin-top: 22px;'>Biblioteca Alejandría</h1>", unsafe_allow_html=True)
    with col3:
        tema_texto = "Tema"
        foco_style = """
        <style>
        .switch {
          position: relative;
          display: inline-block;
          width: 50px;
          height: 26px;
        }

        .switch input {
          opacity: 0;
          width: 0;
          height: 0;
        }

        .slider {
          position: absolute;
          cursor: pointer;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: #ccc;
          transition: .4s;
          border-radius: 26px;
        }

        .slider:before {
          position: absolute;
          content: "";
          height: 20px;
          width: 20px;
          left: 3px;
          bottom: 3px;
          background-color: white;
          transition: .4s;
          border-radius: 50%;
        }

        input:checked + .slider {
          background-color: #44bba4;
        }

        input:checked + .slider:before {
          transform: translateX(24px);
        }
        </style>
        """
        st.markdown(f"""
        {foco_style}
        <label class="switch">
          <input type="checkbox" {'checked' if st.session_state.modo_oscuro else ''} onclick="window.location.reload()">
          <span class="slider"></span>
        </label>
        """, unsafe_allow_html=True)
        if st.button("Tema", key="toggle_tema"):
            st.session_state.modo_oscuro = not st.session_state.modo_oscuro
            st.rerun()
except Exception as e:
    st.error("No se pudo cargar el logo. Asegúrate de que 'logobiblioteca.png' esté en el mismo directorio que main.py")

# Estado inicial de navegación
if "vista" not in st.session_state:
    st.session_state.vista = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# Menú lateral si inició sesión
if st.session_state.usuario and st.session_state.vista not in ["recuperar", "registro"]:
    st.sidebar.title("Menú")
    opcion = st.sidebar.selectbox("Opciones", ["Inicio", "Mis libros guardados", "Mi perfil", "Cerrar sesión"])

    if opcion == "Inicio":
        st.session_state.vista = "inicio"
    elif opcion == "Mis libros guardados":
        st.session_state.vista = "guardados"
    elif opcion == "Mi perfil":
        st.session_state.vista = "perfil"
    elif opcion == "Cerrar sesión":
        st.session_state.vista = "login"
        st.session_state.usuario = None
        st.success("Sesión cerrada correctamente.")
        st.rerun()

# Control de navegación
if st.session_state.vista == "login":
    acceso, usuario = login.login()
    if acceso:
        st.session_state.usuario = usuario
        st.session_state.vista = "inicio"
        st.rerun()

elif st.session_state.vista == "registro":
    registro.registrar_usuario()

elif st.session_state.vista == "recuperar":
    recuperar.recuperar_contrasena()

elif st.session_state.vista == "inicio":
    inicio.pantalla_inicio(st.session_state.usuario)

elif st.session_state.vista == "perfil":
    perfil.mostrar_perfil(st.session_state.usuario)

elif st.session_state.vista == "guardados":
    st.title("Mis libros guardados")
    libros = obtener_libros_guardados(st.session_state.usuario["correo"])

    if libros:
        st.markdown(f"### Tienes **{len(libros)}** libro(s) guardado(s).")
        for i, libro in enumerate(libros):
            st.markdown("---")
            cols = st.columns([2, 6, 2])

            with cols[0]:
                if libro["imagen"]:
                    st.image(libro["imagen"], width=100)

            with cols[1]:
                st.subheader(libro["titulo"])
                st.markdown(f"**Autores:** {libro.get('autores', 'Desconocido')}")
                with st.expander("Descripción"):
                    st.write(libro["descripcion"])

            with cols[2]:
                if st.button(f"Leer", key=f"leer_{i}"):
                    url_google = f"https://www.google.com/search?q={libro['titulo'].replace(' ', '+')}"
                    st.markdown(f"[Abrir libro en Google Books]({url_google})", unsafe_allow_html=True)

                if st.button(f"Eliminar", key=f"eliminar_{i}"):
                    from acciones_libros import eliminar_libro_guardado
                    eliminar_libro_guardado(st.session_state.usuario["correo"], libro["titulo"])
                    st.success("Libro eliminado.")
                    st.rerun()
    else:
        st.info("No has guardado ningún libro aún.")
