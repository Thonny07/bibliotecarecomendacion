import streamlit as st
from PIL import Image
import login
import registro
import inicio
import recuperar
import perfil
from acciones_libros import obtener_libros_guardados

# -------- Configuración de página --------
st.set_page_config(layout="wide")

# -------- Estado inicial de tema --------
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False  # modo claro por defecto

# -------- Aplicar tema visual --------
def aplicar_tema():
    modo_oscuro = st.session_state.modo_oscuro
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde = "#888888" if modo_oscuro else "#cccccc"
    campo_fondo = "#333333" if modo_oscuro else "#ffffff"

    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo} !important;
            color: {texto} !important;
        }}
        input, textarea, select {{
            background-color: {campo_fondo} !important;
            color: {texto} !important;
            border: 1px solid {borde} !important;
            border-radius: 8px;
        }}
        .stSidebar {{
            background-color: #a2ded0 !important;
        }}
        .modo-btn {{
            background: none;
            border: none;
            cursor: pointer;
        }}
        .modo-icono {{
            width: 30px;
            height: 30px;
        }}
        </style>
    """, unsafe_allow_html=True)

aplicar_tema()

# -------- Logo y título superior --------
col_logo, col_modo = st.columns([10, 1])
with col_logo:
    try:
        logo = Image.open("logobiblioteca.png")
        st.markdown("""
            <div style='display: flex; align-items: center; justify-content: center;'>
                <img src='data:image/png;base64,""" + Image.open("logobiblioteca.png").tobytes().hex() + """' width='60' style='margin-right: 15px;' />
                <h2>Biblioteca Alejandría</h2>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='text-align: center;'>Biblioteca Alejandría</h2>", unsafe_allow_html=True)

with col_modo:
    foco_encendido = "https://img.icons8.com/fluency/48/light-on.png"
    foco_apagado = "https://img.icons8.com/fluency/48/light-off.png"
    icono_foco = foco_encendido if st.session_state.modo_oscuro else foco_apagado
    if st.button("", key="modo_btn"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()
    st.markdown(f"<img class='modo-icono' src='{icono_foco}' />", unsafe_allow_html=True)

# -------- Estado inicial de navegación --------
if "vista" not in st.session_state:
    st.session_state.vista = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# -------- Menú lateral si inició sesión --------
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

# -------- Control de navegación --------
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
                if st.button("Leer", key=f"leer_{i}"):
                    url_google = f"https://www.google.com/search?q={libro['titulo'].replace(' ', '+')}"
                    st.markdown(f"[Abrir libro en Google Books]({url_google})", unsafe_allow_html=True)

                if st.button("Eliminar", key=f"eliminar_{i}"):
                    from acciones_libros import eliminar_libro_guardado
                    eliminar_libro_guardado(st.session_state.usuario["correo"], libro["titulo"])
                    st.success("Libro eliminado.")
                    st.rerun()
    else:
        st.info("No has guardado ningún libro aún.")
