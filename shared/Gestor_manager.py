# json convierte listas/diccionarios a texto y al revés.
import json
# os trabaja con archivos y carpetas del computador.
import os


# Clase = molde. Este molde sabe leer y guardar un archivo JSON.
class GestorJSON:

    # __init__ se ejecuta solo al crear un GestorJSON. ruta = dónde está el archivo.
    def __init__(self, ruta):
        # Guardamos la ruta dentro del objeto (self) para usarla después.
        self.ruta = ruta
        # Sacamos solo la carpeta de la ruta ("data/estudiantes.json" -> "data").
        carpeta = os.path.dirname(ruta)
        # Si la ruta sí trae carpeta...
        if carpeta:
            # ...la creamos; exist_ok=True evita error si ya existe.
            os.makedirs(carpeta, exist_ok=True)

    # Lee los datos del archivo.
    def cargar(self):
        # Si el archivo aún no existe (primera vez)...
        if not os.path.exists(self.ruta):
            # ...no hay datos: devolvemos una lista vacía.
            return []
        # Abrimos para leer ("r") con tildes bien (utf-8). "with" lo cierra solo.
        with open(self.ruta, "r", encoding="utf-8") as f:
            # Convertimos el texto JSON a lista de diccionarios y la devolvemos.
            return json.load(f)

    # Guarda los datos en el archivo.
    def guardar(self, datos):
        # Abrimos para escribir ("w"): reemplaza el contenido anterior.
        with open(self.ruta, "w", encoding="utf-8") as f:
            # Escribimos como JSON; ensure_ascii=False respeta tildes; indent=2 lo ordena.
            json.dump(datos, f, ensure_ascii=False, indent=2)
