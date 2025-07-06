import streamlit as st
from libros_api import buscar_libros_api
from acciones_libros import guardar_libro_para_usuario
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Inicializar Firebase
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

def aplicar_tema_estilo():
    modo_oscuro = st.session_state.get("modo_oscuro", False)
    fondo = "#1e1e1e" if modo_oscuro else "#ffffff"
    texto = "#ffffff" if modo_oscuro else "#000000"
    borde_input = "#ffffff" if modo_oscuro else "#44bba4"
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-color: {fondo};
            color: {texto};
        }}
        .stTextInput input, .stTextArea textarea, .stSelectbox select {{
            background-color: {fondo};
            color: {texto};
            border: 1px solid {borde_input};
            border-radius: 8px;
            padding: 8px;
        }}
        .stSidebar {{
            background-color: #a2ded0;
        }}
        .recomendacion-container {{
            background-color: rgba(200, 200, 200, 0.1);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .estrella-btn {{
            font-size: 24px;
            background: none;
            border: none;
            color: {texto};
            cursor: pointer;
        }}
        .estrella-btn:hover {{
            color: #FFD700;
        }}
        </style>
    """, unsafe_allow_html=True)

def pantalla_inicio(usuario):
    aplicar_tema_estilo()

    with st.sidebar:
        if "modo_oscuro" not in st.session_state:
            st.session_state.modo_oscuro = False
        modo = st.session_state.modo_oscuro
        foco = "🔆" if not modo else "🌙"
        if st.button(f"{foco} Cambiar tema"):
            st.session_state.modo_oscuro = not modo
            st.rerun()

    st.subheader(f"Bienvenido, {usuario['nombre']} {usuario['apellido']}")
    consulta = st.text_input("Buscar libros")
    col1, col2 = st.columns(2)
    idioma = col1.selectbox("Idioma", ["Todos", "es", "en", "fr", "de", "it", "pt"])
    pais = col2.selectbox("País", ["Todos", "PE", "US", "ES", "FR", "AR"])

    col_izq, col_der = st.columns([3, 1.5])

    with col_der:
        st.markdown("<h3>Recomendaciones</h3>", unsafe_allow_html=True)
        temas = ["historia", "filosofía", "ciencia", "novela", "fantasía", "autoayuda"]
        tema_recom = random.choice([t for t in temas if consulta.lower() not in t])
        sugerencias = buscar_libros_api(tema_recom, idioma="Todos", pais="Todos")[:5]
        for s in sugerencias:
            st.markdown(f"<div class='recomendacion-container'><strong>{s['titulo']}</strong>", unsafe_allow_html=True)
            if s.get("imagen"):
                st.image(s["imagen"], width=100)
            if s.get("enlace"):
                st.markdown(f"<a href='{s['enlace']}' target='_blank'><button>Leer libro</button></a>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_izq:
        if consulta:
            resultados = buscar_libros_api(consulta, idioma=idioma, pais=pais)
            if resultados:
                for idx, libro in enumerate(resultados):
                    st.markdown("<hr>", unsafe_allow_html=True)
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if libro.get("imagen"):
                            st.image(libro["imagen"], width=130)
                    with c2:
                        st.subheader(libro["titulo"])
                        st.markdown(f"**Autores:** {libro.get('autores', 'Desconocido')}")
                        with st.expander("Descripción"):
                            st.write(libro.get("descripcion", "Sin descripción"))
                        if st.button("Guardar para leer después", key=f"guardar_{idx}"):
                            guardar_libro_para_usuario(usuario["correo"], libro)
                            st.success("Libro guardado exitosamente.")
                        if libro.get("enlace"):
                            st.markdown(f"<a href='{libro['enlace']}' target='_blank'><button>Leer ahora</button></a>", unsafe_allow_html=True)

                        st.markdown("**Califica este libro:**", unsafe_allow_html=True)
                        if f"calificacion_{idx}" not in st.session_state:
                            st.session_state[f"calificacion_{idx}"] = 0

                        col_estrella = st.columns(5)
                        for i in range(5):
                            if col_estrella[i].button("★" if i < st.session_state[f"calificacion_{idx}"] else "☆", key=f"estrella_{idx}_{i}"):
                                st.session_state[f"calificacion_{idx}"] = i + 1

                        comentario = st.text_area("Comentario (opcional)", key=f"comentario_{idx}")
                        if st.button("Enviar reseña", key=f"resena_{idx}"):
                            guardar_reseña(usuario["correo"], libro["titulo"], st.session_state[f"calificacion_{idx}"], comentario)
                            st.success("¡Gracias por tu reseña!")

                        reseñas = obtener_reseñas(libro["titulo"])
                        if reseñas:
                            st.markdown("<h4>Comentarios de otros usuarios:</h4>", unsafe_allow_html=True)
                            for r in reseñas:
                                estrellas_vista = "★" * r['estrellas'] + "☆" * (5 - r['estrellas'])
                                st.markdown(f"<b>{r['correo']}</b>: {estrellas_vista}", unsafe_allow_html=True)
                                if r["comentario"]:
                                    st.markdown(f"<blockquote>{r['comentario']}</blockquote>", unsafe_allow_html=True)

    st.markdown("<h3>Recomendaciones para ti</h3>", unsafe_allow_html=True)
    edad = usuario.get("edad", 25)
    genero = usuario.get("genero", "Otro")
    if edad < 18:
        st.info("Recomendamos libros juveniles y aventuras.")
    elif genero == "Femenino":
        st.info("Explora novelas históricas y autoayuda.")
    else:
        st.info("Revisa ciencia, historia, tecnología y negocios.")
