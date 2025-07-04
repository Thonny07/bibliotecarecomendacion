import streamlit as st
from libros_api import buscar_libros_api
from acciones_libros import guardar_libro_para_usuario
import firebase_admin
from firebase_admin import credentials, firestore
import random

# 🔥 Inicializar Firebase si aún no está
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
    st.markdown("## 📚 Bienvenido a la Biblioteca Alexandrina")
    st.markdown(f"👤 Usuario: **{usuario['nombre']} {usuario['apellido']}**")

    st.title("🔍 Buscar libros")
    consulta = st.text_input("🔎 Escribe el nombre del libro, tema o autor:")

    col1, col2 = st.columns(2)
    with col1:
        idioma = st.selectbox("🌐 Idioma", ["Todos", "es", "en", "fr", "de", "it", "pt"])
    with col2:
        pais = st.selectbox("📍 País (relevancia)", ["Todos", "PE", "US", "ES", "FR", "AR"])

    # ⏱️ Cargar recomendaciones IA desde el inicio
    with st.container():
        col_izq, col_der = st.columns([2.5, 1.5])

        with col_der:
            st.markdown("## 🤖 Libros sugeridos por IA:")
            temas_generales = ["historia", "filosofía", "ciencia", "novela", "fantasía", "autoayuda", "biografías"]
            tema_aleatorio = random.choice(temas_generales)
            sugerencias_generales = buscar_libros_api(tema_aleatorio, idioma="Todos", pais="Todos")[:7]

            for sugerido in sugerencias_generales:
                st.markdown(f"**📘 {sugerido['titulo']}**")
                if sugerido.get("imagen"):
                    st.image(sugerido["imagen"], width=100)
                if sugerido.get("enlace"):
                    st.markdown(f"[📖 Leer libro]({sugerido['enlace']})", unsafe_allow_html=True)
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
                            with st.expander("📘 Descripción"):
                                st.write(libro.get("descripcion", "Sin descripción"))

                            if st.button(f"📌 Guardar para leer después - {libro['titulo']}", key=f"guardar_{idx}"):
                                guardar_libro_para_usuario(usuario["correo"], libro)
                                st.success("✅ Libro guardado exitosamente.")

                            if libro.get("enlace"):
                                st.markdown(
                                    f"""<a href="{libro['enlace']}" target="_blank">
                                    <button style='background-color:#4CAF50; color:white; padding:10px 20px;
                                    border:none; border-radius:5px; margin-top:5px; cursor:pointer;'>
                                    📖 Leer ahora
                                    </button></a>""",
                                    unsafe_allow_html=True
                                )

                            # ⭐ Calificación
                            st.markdown("#### ⭐ Califica este libro:")
                            estrellas = st.radio("Selecciona estrellas:", [1, 2, 3, 4, 5], horizontal=True, key=f"rating_{idx}")
                            comentario = st.text_area("📝 Comentario (opcional):", key=f"comentario_{idx}")
                            if st.button("✅ Enviar reseña", key=f"resena_{idx}"):
                                guardar_reseña(usuario["correo"], libro["titulo"], estrellas, comentario)
                                st.success("✅ ¡Gracias por tu reseña!")

                            reseñas = obtener_reseñas(libro["titulo"])
                            if reseñas:
                                st.markdown("### 🗣️ Comentarios de otros usuarios:")
                                for r in reseñas:
                                    st.markdown(f"- **{r['correo']}**: {mostrar_estrellas(r['estrellas'])}")
                                    if r["comentario"]:
                                        st.markdown(f"  > {r['comentario']}")

    # 🎯 Recomendaciones personalizadas según perfil
    st.markdown("### 🎯 Recomendaciones personalizadas:")
    edad = usuario.get("edad", 25)
    genero_usuario = usuario.get("genero", "Otro")

    if edad < 18:
        st.info("👦 Te recomendamos libros juveniles, fantasía y aventuras.")
    elif genero_usuario == "Femenino":
        st.info("👩 Puedes explorar novelas históricas, ficción y autoayuda.")
    else:
        st.info("👨 Revisa libros de ciencia, historia, negocios o tecnología.")
