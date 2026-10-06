# MODELO: representa a un estudiante y sus datos.
# No pide datos, no imprime menús y no guarda archivos.
class Estudiante:

    # Constructor: se ejecuta al crear un estudiante nuevo.
    # notas=None significa que es opcional.
    def __init__(self, id, carnet, nombre, email, notas=None):
        # Número único que identifica al estudiante en el sistema.
        self.id = id
        # Carnet académico (no puede repetirse).
        self.carnet = carnet
        # Nombre del estudiante.
        self.nombre = nombre
        # Correo del estudiante (tampoco puede repetirse).
        self.email = email
        # Notas: diccionario {"Mate": [15, 18], "Física": [12]}.
        # Si nos pasaron notas las usamos; si no, empezamos con {} vacío.
        self.notas = notas if notas is not None else {}

    # @property: se usa como dato (estudiante.materias), sin paréntesis.
    @property
    def materias(self):
        # .keys() son las materias; set(...) las vuelve conjunto (sin repetidos).
        return set(self.notas.keys())

    # Calcula el promedio de todas las notas del estudiante.
    def promedio(self):
        # Juntamos las notas de todas las materias en una sola lista.
        todas = [n for lista in self.notas.values() for n in lista]
        # Si no hay ninguna nota...
        if not todas:
            # ...no se puede promediar: devolvemos None (nada).
            return None
        # Promedio = suma / cantidad.
        return sum(todas) / len(todas)

    # Convierte el estudiante a diccionario para guardarlo en JSON.
    def to_dict(self):
        # Devolvemos un diccionario con todos sus datos.
        return {"id": self.id, "carnet": self.carnet,
                "nombre": self.nombre, "email": self.email,
                "notas": self.notas}

    # @staticmethod: no necesita un estudiante ya creado para usarse.
    @staticmethod
    def from_dict(d):
        # Hace lo contrario de to_dict: de diccionario a objeto Estudiante.
        # d.get("notas", {}) usa {} si el diccionario no trae notas.
        return Estudiante(d["id"], d["carnet"], d["nombre"],
                          d["email"], d.get("notas", {}))

    # __str__ define cómo se ve el estudiante al hacer print(estudiante).
    def __str__(self):
        # Pedimos el promedio (puede ser None).
        prom = self.promedio()
        # Con 2 decimales si existe; si no, "sin notas".
        txt = f"{prom:.2f}" if prom is not None else "sin notas"
        # Armamos el texto final (los paréntesis permiten partir la línea).
        return (f"[{self.id}] {self.carnet} | {self.nombre} | "
                f"{self.email} | promedio: {txt}")
