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
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stRadio div {{
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
        }}
        button {{
            background-color: #44bba4 !important;
            color: white !important;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #379d8e !important;
        }}
        .estrella-rating input[type="radio"] {{
            display: none;
        }}
        .estrella-rating label {{
            font-size: 24px;
            color: #ddd;
            cursor: pointer;
        }}
        .estrella-rating input[type="radio"]:checked ~ label,
        .estrella-rating label:hover,
        .estrella-rating label:hover ~ label {{
            color: gold;
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
        if consulta:
            tema_base = consulta.split()[0]
            sugerencias = [libro for libro in buscar_libros_api(tema_base, idioma="Todos", pais="Todos") if libro['titulo'].lower() != consulta.lower()][:5]
        else:
            sugerencias = buscar_libros_api(random.choice(temas), idioma="Todos", pais="Todos")[:5]

        for s in sugerencias:
            st.markdown(f"<div class='recomendacion-container'><strong>{s['titulo']}</strong>", unsafe_allow_html=True)
            if s.get("imagen"):
                st.image(s["imagen"], width=100)
            if s.get("enlace"):
                st.markdown(f"<a href='{s['enlace']}' target='_blank'><button>Leer libro</button></a>", unsafe_allow_html=True)
            st.markdown("</div><br>", unsafe_allow_html=True)

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
                        st.markdown(f"<strong>Autores:</strong> {libro.get('autores', 'Desconocido')}", unsafe_allow_html=True)
                        with st.expander("Descripción"):
                            st.write(libro.get("descripcion", "Sin descripción"))
                        if st.button("Guardar para leer después", key=f"guardar_{idx}"):
                            guardar_libro_para_usuario(usuario["correo"], libro)
                            st.success("Libro guardado exitosamente.")
                        if libro.get("enlace"):
                            st.markdown(f"<a href='{libro['enlace']}' target='_blank'><button>Leer ahora</button></a>", unsafe_allow_html=True)

                        st.markdown("<strong>Califica este libro:</strong>", unsafe_allow_html=True)
                        estrellas_html = "".join([
                            f"<input type='radio' id='estrella_{idx}_{i}' name='rating_{idx}' value='{i}'><label for='estrella_{idx}_{i}'>★</label>"
                            for i in range(5, 0, -1)
                        ])
                        st.markdown(f"<div class='estrella-rating'>{estrellas_html}</div>", unsafe_allow_html=True)

                        comentario = st.text_area("Comentario (opcional)", key=f"comentario_{idx}")
                        if st.button("Enviar reseña", key=f"resena_{idx}"):
                            guardar_reseña(usuario["correo"], libro["titulo"], 5, comentario)  # Estrellas hardcodeado por HTML
                            st.success("¡Gracias por tu reseña!")

                        reseñas = obtener_reseñas(libro["titulo"])
                        if reseñas:
                            st.markdown("<h4>Comentarios de otros usuarios:</h4>", unsafe_allow_html=True)
                            for r in reseñas:
                                st.markdown(f"<b>{r['correo']}</b>: {'★'*int(r['estrellas']) + '☆'*(5-int(r['estrellas']))}", unsafe_allow_html=True)
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
