import requests

def buscar_libros_api(consulta, idioma="Todos", pais="Todos"):
    url = f"https://www.googleapis.com/books/v1/volumes?q={consulta}"

    # Agregar filtros si se seleccionan
    if idioma != "Todos":
        url += f"&langRestrict={idioma}"
    if pais != "Todos":
        url += f"&country={pais}"

    url += "&maxResults=10"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        libros = []

        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            titulo = info.get("title", "Sin título")
            autores = info.get("authors", ["Desconocido"])
            imagen = info.get("imageLinks", {}).get("thumbnail", "")
            descripcion = info.get("description", "Sin descripción")
            enlace = info.get("previewLink", "")  # 🔗 Agregado: enlace al libro

            libros.append({
                "titulo": titulo,
                "autores": ", ".join(autores),
                "imagen": imagen,
                "descripcion": descripcion,
                "enlace": enlace  # ✅ Incluido en cada resultado
            })

        return libros
    else:
        return []
