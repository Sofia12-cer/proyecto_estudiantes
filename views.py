# VIEWS: aquí están las operaciones del CRUD (según la guía) y las reglas.
# Importamos el modelo, el gestor de archivos y las herramientas.
from models import Estudiante
from shared.Gestor_manager import GestorJSON
from shared.herramientas import limpiar_texto, email_valido, nota_valida


# Clase que coordina todo: valida, crea, busca, actualiza, elimina.
class ControladorEstudiantes:

    # Constructor: prepara todo al iniciar el programa.
    def __init__(self, ruta="data/estudiantes.json"):
        # Creamos el gestor que lee/guarda en esa ruta (data/estudiantes.json).
        self.gestor = GestorJSON(ruta)
        # Cargamos los diccionarios del archivo y los volvemos objetos Estudiante.
        self.estudiantes = [Estudiante.from_dict(d)
                            for d in self.gestor.cargar()]
        # SET de carnets usados: no admite repetidos y buscar en él es rápido.
        self.carnets = {e.carnet for e in self.estudiantes}
        # SET de emails usados.
        self.emails = {e.email for e in self.estudiantes}

    # Método interno (el _ avisa "no usar desde afuera"): guarda en el archivo.
    def _guardar(self):
        # Convertimos cada estudiante a diccionario y guardamos la lista.
        self.gestor.guardar([e.to_dict() for e in self.estudiantes])

    # Calcula el id del próximo estudiante.
    def _siguiente_id(self):
        # max(...) busca el id mayor (default=0 si no hay nadie); sumamos 1.
        return max((e.id for e in self.estudiantes), default=0) + 1

    # Busca un estudiante por su id.
    def _por_id(self, id):
        # Recorremos los estudiantes uno por uno.
        for e in self.estudiantes:
            # Si el id coincide...
            if e.id == id:
                # ...lo devolvemos y la función termina.
                return e
        # Si no lo encontró, devolvemos None (no existe).
        return None

    # ---------------- CRUD ----------------

    # C = Create (crear).
    def crear_estudiante(self, carnet, nombre, email):
        # Limpiamos espacios de los tres datos.
        carnet, nombre, email = (limpiar_texto(carnet), limpiar_texto(nombre),
                                 limpiar_texto(email))
        # Si alguno quedó vacío ("" cuenta como falso)...
        if not carnet or not nombre or not email:
            # ...devolvemos una tupla (False, mensaje): falló y por qué.
            return False, "Todos los campos son obligatorios."
        # Revisamos que el email tenga forma válida.
        if not email_valido(email):
            return False, "El email no es válido."
        # PUNTO 3: ¿el carnet ya está en el set?
        if carnet in self.carnets:
            # Si ya existe, rechazamos.
            return False, "El carnet ya existe."
        # Misma validación con el email.
        if email in self.emails:
            return False, "El email ya existe."
        # Pasó todas las validaciones: creamos el objeto con un id nuevo.
        est = Estudiante(self._siguiente_id(), carnet, nombre, email)
        # Lo agregamos a la lista.
        self.estudiantes.append(est)
        # Anotamos su carnet en el set para que nadie más lo use.
        self.carnets.add(carnet)
        # Anotamos su email también.
        self.emails.add(email)
        # Guardamos en el archivo.
        self._guardar()
        # Devolvemos (True, mensaje): todo salió bien.
        return True, f"Estudiante creado con id {est.id}."

    # R = Read (leer): todos los estudiantes.
    def obtener_todos(self):
        # list(...) entrega una copia para no dañar la original por error.
        return list(self.estudiantes)

    # R = Read: buscar por texto.
    def buscar_estudiantes(self, texto):
        # Pasamos a minúsculas para que "ana" encuentre "Ana".
        t = limpiar_texto(texto).lower()
        # Devolvemos los que tengan el texto en nombre, carnet o email.
        return [e for e in self.estudiantes
                if t in e.nombre.lower() or t in e.carnet.lower()
                or t in e.email.lower()]

    # U = Update (actualizar). carnet=None significa "opcional".
    def actualizar_estudiante(self, id, carnet=None, nombre=None, email=None):
        # Buscamos al estudiante.
        est = self._por_id(id)
        # Si no existe...
        if est is None:
            return False, "No existe un estudiante con ese id."
        # Si quiere un carnet distinto y ese carnet ya lo usa otro...
        if carnet and carnet != est.carnet and carnet in self.carnets:
            return False, "El carnet ya existe."
        # Si quiere un email distinto y ya lo usa otro...
        if email and email != est.email and email in self.emails:
            return False, "El email ya existe."
        # Si el email nuevo no tiene forma válida...
        if email and not email_valido(email):
            return False, "El email no es válido."
        # Si mandaron un carnet nuevo...
        if carnet:
            # ...sacamos el carnet viejo del set (discard no da error si no está).
            self.carnets.discard(est.carnet)
            # Cambiamos el carnet del estudiante.
            est.carnet = carnet
            # Metemos el carnet nuevo al set.
            self.carnets.add(carnet)
        # Mismo proceso con el email.
        if email:
            self.emails.discard(est.email)
            est.email = email
            self.emails.add(email)
        # El nombre sí puede repetirse: solo lo cambiamos.
        if nombre:
            est.nombre = nombre
        # Guardamos en el archivo.
        self._guardar()
        return True, "Estudiante actualizado."

    # D = Delete (eliminar).
    def eliminar_estudiante(self, id):
        # Buscamos al estudiante.
        est = self._por_id(id)
        # Si no existe, avisamos.
        if est is None:
            return False, "No existe un estudiante con ese id."
        # Lo quitamos de la lista.
        self.estudiantes.remove(est)
        # Liberamos su carnet y su email: otro estudiante podrá usarlos.
        self.carnets.discard(est.carnet)
        self.emails.discard(est.email)
        # Guardamos en el archivo.
        self._guardar()
        return True, "Estudiante eliminado."

    # ---------------- NOTAS Y CONJUNTOS ----------------

    # PUNTO 4: agregar una nota a una materia.
    def agregar_nota(self, id, materia, nota):
        # Buscamos al estudiante.
        est = self._por_id(id)
        # Si no existe, devolvemos el error.
        if est is None:
            return False, "No existe un estudiante con ese id."
        # Limpiamos espacios de la materia.
        materia = limpiar_texto(materia)
        # La materia no puede estar vacía.
        if not materia:
            return False, "La materia no puede estar vacía."
        # try/except: intentamos algo que puede fallar sin que el programa se caiga.
        try:
            # Intentamos convertir la nota a número decimal.
            nota = float(nota)
        # Si no se pudo ("abc", por ejemplo)...
        except (TypeError, ValueError):
            return False, "La nota debe ser un número."
        # Usamos la herramienta: ¿la nota está entre 0 y 20?
        if not nota_valida(nota):
            # Si no, devolvemos (False, mensaje) como pide la guía.
            return False, "La nota debe estar entre 0 y 20."
        # setdefault: si la materia no existe crea su lista vacía; luego agregamos la nota.
        est.notas.setdefault(materia, []).append(nota)
        # Guardamos en el archivo.
        self._guardar()
        return True, f"Nota {nota} agregada en {materia}."

    # "Ver promedio" (el menú lo pide, aunque la guía no nombra la función).
    def calcular_promedio(self, id):
        # Buscamos al estudiante.
        est = self._por_id(id)
        # Si no existe...
        if est is None:
            return False, "No existe un estudiante con ese id."
        # Pedimos el promedio al modelo.
        prom = est.promedio()
        # Si devolvió None, es porque no tiene notas.
        if prom is None:
            return False, "El estudiante aún no tiene notas."
        # Todo bien: devolvemos True y el número.
        return True, prom

    # PUNTO 5: set con todas las materias de todos los estudiantes, sin repetir.
    def materias_ofertadas(self):
        # Empezamos con un set vacío (set() y no {}, porque {} es un diccionario).
        materias = set()
        # Recorremos cada estudiante.
        for e in self.estudiantes:
            # |= es UNIÓN de conjuntos: agrega las materias de e sin repetir.
            materias |= e.materias
        # Devolvemos el set completo.
        return materias

    # PUNTO 6: materias que comparten dos estudiantes.
    def estudiantes_en_comun(self, id_a, id_b):
        # Buscamos a los dos estudiantes.
        a, b = self._por_id(id_a), self._por_id(id_b)
        # Si alguno no existe...
        if a is None or b is None:
            return False, "Uno de los ids no existe."
        # & es INTERSECCIÓN de conjuntos: solo lo que está en los dos.
        return True, a.materias & b.materias
