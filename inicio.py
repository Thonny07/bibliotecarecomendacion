import streamlit as st
from libros_api import buscar_libros_api
from acciones_libros import guardar_libro_para_usuario
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Inicializar Firebase si aún no está
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def obtener_reseñas(titulo):
    reseñas = db.collection("reseñas").where("titulo", "==", titulo).stream()
    return [r.to_dict() for r in reseñas]

def guardar_reseña(correo, titulo, estrellas, comentario):
    db.collection("reseñas").add({
        "correo": correo,
        "titulo": titulo,
        "estrellas": estrellas,
        "comentario": comentario
    })

def mostrar_estrellas(valor):
    return "".join(["⭐" if i < valor else "☆" for i in range(5)])

def pantalla_inicio(usuario):
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #222;
    }
    .stTextInput > div > input, .stTextArea > div > textarea {
        background-color: #f4fefc;
        color: #000;
    }
    .stSelectbox > div, .stRadio > div {
        background-color: #f4fefc;
        color: #000;
    }
    .custom-btn {
        background-color: #20c997;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin-top: 5px;
    }
    .custom-btn:hover {
        background-color: #1aa179;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <h2 style="margin: 0; color: #20c997;">Biblioteca Alexandrina</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Usuario:** {usuario['nombre']} {usuario['apellido']}")

    st.subheader("Buscar libros")
    consulta = st.text_input("Nombre del libro, tema o autor")

    col1, col2 = st.columns(2)
    with col1:
        idioma = st.selectbox("Idioma", ["Todos", "es", "en", "fr", "de", "it", "pt"])
    with col2:
        pais = st.selectbox("País (relevancia)", ["Todos", "PE", "US", "ES", "FR", "AR"])

    col_izq, col_der = st.columns([2.5, 1.5])

    with col_der:
        st.markdown("#### Libros sugeridos")
        temas_generales = ["historia", "filosofía", "ciencia", "novela", "fantasía", "autoayuda", "biografías"]
        tema_aleatorio = random.choice(temas_generales)
        sugerencias_generales = buscar_libros_api(tema_aleatorio, idioma="Todos", pais="Todos")[:7]

        for sugerido in sugerencias_generales:
            st.markdown(f"**{sugerido['titulo']}**")
            if sugerido.get("imagen"):
                st.image(sugerido["imagen"], width=100)
            if sugerido.get("enlace"):
                st.markdown(f"<a href='{sugerido['enlace']}' class='custom-btn' target='_blank'>Leer</a>", unsafe_allow_html=True)
            st.markdown("---")

    with col_izq:
        if consulta:
            resultados = buscar_libros_api(consulta, idioma=idioma, pais=pais)
            if resultados:
                for idx, libro in enumerate(resultados):
                    st.markdown("---")
                    col_img, col_info = st.columns([1, 3])
                    with col_img:
                        if libro.get("imagen"):
                            st.image(libro["imagen"], width=130)
                    with col_info:
                        st.subheader(libro["titulo"])
                        st.markdown(f"**Autores:** {libro.get('autores', 'Desconocido')}")
                        with st.expander("Descripción"):
                            st.write(libro.get("descripcion", "Sin descripción"))

                        if st.button(f"Guardar para leer después - {libro['titulo']}", key=f"guardar_{idx}"):
                            guardar_libro_para_usuario(usuario["correo"], libro)
                            st.success("Libro guardado exitosamente.")

                        if libro.get("enlace"):
                            st.markdown(
                                f"""<a href="{libro['enlace']}" target="_blank" class="custom-btn">
                                Leer ahora</a>""",
                                unsafe_allow_html=True
                            )

                        st.markdown("Califica este libro:")
                        estrellas = st.radio("Selecciona estrellas:", [1, 2, 3, 4, 5], horizontal=True, key=f"rating_{idx}")
                        comentario = st.text_area("Comentario (opcional):", key=f"comentario_{idx}")
                        if st.button("Enviar reseña", key=f"resena_{idx}"):
                            guardar_reseña(usuario["correo"], libro["titulo"], estrellas, comentario)
                            st.success("¡Gracias por tu reseña!")

                        reseñas = obtener_reseñas(libro["titulo"])
                        if reseñas:
                            st.markdown("Comentarios de otros usuarios:")
                            for r in reseñas:
                                st.markdown(f"- **{r['correo']}**: {mostrar_estrellas(r['estrellas'])}")
                                if r["comentario"]:
                                    st.markdown(f"> {r['comentario']}")

    st.markdown("---")
    st.markdown("#### Recomendaciones personalizadas")
    edad = usuario.get("edad", 25)
    genero_usuario = usuario.get("genero", "Otro")

    if edad < 18:
        st.info("Recomendamos libros juveniles, fantasía y aventuras.")
    elif genero_usuario == "Femenino":
        st.info("Puedes explorar novelas históricas, ficción y autoayuda.")
    else:
        st.info("Revisa libros de ciencia, historia, negocios o tecnología.")
