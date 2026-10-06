
# HERRAMIENTAS: colores, títulos y validaciones.
# Son funciones pequeñas y reutilizables que no dependen de estudiantes.
# os se usa abajo para activar los colores en la terminal de Windows.
import os

# Truco: en Windows, esta línea "despierta" los colores ANSI de la terminal.
os.system("")

# ---------------- COLORES ----------------
# Códigos ANSI: secuencias especiales que la terminal convierte en color.
VERDE = "\033[92m"
# Rojo para errores.
ROJO = "\033[91m"
# Cian para títulos.
CIAN = "\033[96m"
# RESET devuelve el texto a su color normal.
RESET = "\033[0m"


# Envuelve un texto con un color y luego lo resetea.
def con_color(texto, color):
    # Color + texto + RESET: lo que va entre medio se ve de ese color.
    return f"{color}{texto}{RESET}"


# ---------------- TÍTULOS Y MENSAJES ----------------
# Imprime un título llamativo.
def titulo(texto):
    # \n deja una línea en blanco antes; el título sale en cian.
    print(con_color(f"\n=== {texto} ===", CIAN))


# Imprime un mensaje de éxito en verde.
def exito(texto):
    print(con_color(texto, VERDE))


# Imprime un mensaje de error en rojo.
def error(texto):
    print(con_color(texto, ROJO))


# ---------------- VALIDACIONES ----------------
# Quita espacios sobrantes al inicio y al final de un texto.
def limpiar_texto(texto):
    # strip() hace justo eso: "  Ana " -> "Ana".
    return texto.strip()


# Revisa que un email tenga forma básica: algo@algo.algo
def email_valido(email):
    # Debe tener "@" y, después del "@", al menos un punto.
    # split("@")[-1] toma lo que está después del último "@".
    return "@" in email and "." in email.split("@")[-1]


# Revisa que una nota esté entre 0 y 20 (ambos incluidos).
def nota_valida(nota):
    # Comparación encadenada: True solo si 0 <= nota <= 20.
    return 0 <= nota <= 20


# ---------------- ENTRADA POR TECLADO ----------------
# Pide un texto por teclado.
def pedir_texto(mensaje):
    # input() muestra el mensaje y espera; limpiar_texto quita espacios.
    return limpiar_texto(input(mensaje))


# Pide un número entero por teclado (por ejemplo, un id).
def pedir_entero(mensaje):
    # try: intentamos algo que puede fallar sin que el programa se caiga.
    try:
        # Convertimos lo escrito a entero.
        return int(input(mensaje))
    # Si escribieron letras, int() lanza ValueError.
    except ValueError:
        # Devolvemos None; el programa avisará que el id no existe.
        return None
