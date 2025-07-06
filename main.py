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
    if st.session_state.modo_oscuro:
        st.markdown("""
            <style>
            html, body, .stApp {
                background-color: #1e1e1e !important;
                color: white !important;
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
            </style>
        """, unsafe_allow_html=True)

aplicar_tema()

# -------- Logo centrado --------
try:
    logo = Image.open("logobiblioteca.png")
    st.image(logo, width=150)
except:
    st.warning("⚠️ No se pudo cargar el logo")

# -------- Estado inicial de navegación --------
if "vista" not in st.session_state:
    st.session_state.vista = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None


# -------- Menú lateral si inició sesión --------
if st.session_state.usuario and st.session_state.vista not in ["recuperar", "registro"]:
    st.sidebar.title("📚 Menú")
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
        st.success("🔒 Sesión cerrada correctamente.")
        st.rerun()

# -------- Menú superior derecho --------
if st.session_state.usuario and st.session_state.vista not in ["recuperar", "registro"]:
    col1, col2 = st.columns([10, 1])
    with col2:
        with st.expander("👤", expanded=False):
            st.markdown(f"**{st.session_state.usuario['nombre']}**")
            if st.button("🧾 Mi perfil"):
                st.session_state.vista = "perfil"
                st.rerun()
            if st.button("🔒 Cerrar sesión"):
                st.session_state.vista = "login"
                st.session_state.usuario = None
                st.success("Sesión cerrada.")
                st.rerun()

    # 🌗 Botón de cambio de tema
    icono = "🌙" if not st.session_state.modo_oscuro else "🌞"
    if st.button(f"{icono} Cambiar tema"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro
        st.rerun()

# -------- Control de navegación --------
if st.session_state.vista == "login":
    st.write("🔐 Cargando login...")
    acceso, usuario = login.login()
    if acceso:
        st.session_state.usuario = usuario
        st.session_state.vista = "inicio"
        st.rerun()

elif st.session_state.vista == "registro":
    st.write("📝 Cargando registro...")
    registro.registrar_usuario()

elif st.session_state.vista == "recuperar":
    st.write("📩 Cargando recuperación...")
    recuperar.recuperar_contrasena()

elif st.session_state.vista == "inicio":
    st.write("🏠 Cargando inicio...")
    inicio.pantalla_inicio(st.session_state.usuario)

elif st.session_state.vista == "perfil":
    st.write("👤 Cargando perfil...")
    perfil.mostrar_perfil(st.session_state.usuario)

elif st.session_state.vista == "guardados":
    st.title("📌 Mis libros guardados")
    st.write("📦 Cargando libros guardados...")

    libros = obtener_libros_guardados(st.session_state.usuario["correo"])

    if libros:
        st.markdown(f"### 📦 Tienes **{len(libros)}** libro(s) guardado(s).")
        for i, libro in enumerate(libros):
            st.markdown("---")
            cols = st.columns([2, 6, 2])

            with cols[0]:
                if libro["imagen"]:
                    st.image(libro["imagen"], width=100)

            with cols[1]:
                st.subheader(libro["titulo"])
                st.markdown(f"**Autores:** {libro.get('autores', 'Desconocido')}")
                with st.expander("📘 Descripción"):
                    st.write(libro["descripcion"])

            with cols[2]:
                if st.button(f"📖 Leer", key=f"leer_{i}"):
                    url_google = f"https://www.google.com/search?q={libro['titulo'].replace(' ', '+')}"
                    st.markdown(f"[Abrir libro en Google Books]({url_google})", unsafe_allow_html=True)

                if st.button(f"🗑️ Eliminar", key=f"eliminar_{i}"):
                    from acciones_libros import eliminar_libro_guardado
                    eliminar_libro_guardado(st.session_state.usuario["correo"], libro["titulo"])
                    st.success("✅ Libro eliminado.")
                    st.rerun()
    else:
        st.info("📭 No has guardado ningún libro aún.")
