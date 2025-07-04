import firebase_admin
from firebase_admin import credentials, firestore

# Solo inicializar si no está ya
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def guardar_libro_para_usuario(usuario_correo, libro):
    doc_ref = db.collection("usuarios").document(usuario_correo).collection("guardados").document(libro["titulo"])
    doc_ref.set(libro)

def obtener_libros_guardados(usuario_correo):
    docs = db.collection("usuarios").document(usuario_correo).collection("guardados").stream()
    libros = []
    for doc in docs:
        libros.append(doc.to_dict())
    return libros

def eliminar_libro_guardado(usuario_correo, titulo_libro):
    doc_ref = db.collection("usuarios").document(usuario_correo).collection("guardados").document(titulo_libro)
    doc_ref.delete()
