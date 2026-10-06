# main.py: el menú. Pide datos al usuario y muestra resultados.
# os nos ayuda a armar la ruta del archivo de datos.
import os
# Importamos el controlador (las operaciones) desde views.py.
from views import ControladorEstudiantes
# Importamos las herramientas para pedir datos por teclado.
from shared.herramientas import pedir_texto, pedir_entero, titulo, exito, error


# Muestra el menú y devuelve la opción elegida.
def mostrar_menu():
    # titulo() imprime el encabezado en color (viene de herramientas).
    titulo("GESTIÓN DE ESTUDIANTES")
    # Cada print muestra una opción.
    print("1. Crear estudiante")
    print("2. Listar estudiantes")
    print("3. Buscar estudiantes")
    print("4. Actualizar estudiante")
    print("5. Eliminar estudiante")
    print("6. Agregar nota")
    print("7. Ver promedio")
    print("8. Materias en común")
    print("9. Materias ofertadas")
    print("0. Salir")
    # Pedimos la opción y la devolvemos.
    return pedir_texto("Opción: ")


# Muestra una lista de estudiantes.
def mostrar_estudiantes(lista):
    # Si la lista está vacía...
    if not lista:
        print("No hay estudiantes.")
        # return sin valor termina la función aquí.
        return
    # Recorremos la lista.
    for e in lista:
        # print(e) usa el __str__ que definimos en models.py.
        print(e)


# Muestra un conjunto de materias.
def mostrar_materias(materias):
    # Si el conjunto está vacío...
    if not materias:
        print("No hay materias.")
    # Si tiene materias...
    else:
        # sorted() las ordena; join() las une separadas por coma.
        print(", ".join(sorted(materias)))


# Muestra un resultado: verde si salió bien, rojo si falló.
def mostrar_resultado(ok, msg):
    # ok es True/False; decide el color del mensaje.
    if ok:
        exito(msg)
    else:
        error(msg)


# Función principal.
def main():
    # Ruta de data/estudiantes.json junto a este archivo (funciona desde cualquier carpeta).
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "estudiantes.json")
    # Creamos el controlador; carga los datos guardados.
    c = ControladorEstudiantes(ruta)
    # Bucle infinito: el menú se repite hasta elegir salir.
    while True:
        # Mostramos el menú y guardamos la opción.
        op = mostrar_menu()

        # Opción 1: crear estudiante.
        if op == "1":
            # Pedimos los 3 datos; el controlador valida y crea.
            # ok = True/False; msg = texto para mostrar.
            ok, msg = c.crear_estudiante(pedir_texto("Carnet: "),
                                         pedir_texto("Nombre: "),
                                         pedir_texto("Email: "))
            # Mostramos el resultado.
            mostrar_resultado(ok, msg)
        # Opción 2: listar todos.
        elif op == "2":
            mostrar_estudiantes(c.obtener_todos())
        # Opción 3: buscar.
        elif op == "3":
            mostrar_estudiantes(c.buscar_estudiantes(pedir_texto("Buscar: ")))
        # Opción 4: actualizar.
        elif op == "4":
            # Pedimos el id a modificar.
            id = pedir_entero("Id: ")
            # "or None": si dejan vacío (""), se vuelve None = no cambiar.
            ok, msg = c.actualizar_estudiante(
                id,
                pedir_texto("Nuevo carnet (vacío = no cambiar): ") or None,
                pedir_texto("Nuevo nombre (vacío = no cambiar): ") or None,
                pedir_texto("Nuevo email (vacío = no cambiar): ") or None)
            mostrar_resultado(ok, msg)
        # Opción 5: eliminar.
        elif op == "5":
            ok, msg = c.eliminar_estudiante(pedir_entero("Id: "))
            mostrar_resultado(ok, msg)
        # Opción 6: agregar nota.
        elif op == "6":
            # Pedimos id, materia y nota; el controlador valida 0-20.
            ok, msg = c.agregar_nota(pedir_entero("Id: "),
                                     pedir_texto("Materia: "),
                                     pedir_texto("Nota (0-20): "))
            mostrar_resultado(ok, msg)
        # Opción 7: ver promedio.
        elif op == "7":
            ok, res = c.calcular_promedio(pedir_entero("Id: "))
            # Si ok es True, res es el número (verde); si no, es un error (rojo).
            if ok:
                exito(f"Promedio: {res:.2f}")
            else:
                error(res)
        # Opción 8: materias en común.
        elif op == "8":
            ok, res = c.estudiantes_en_comun(pedir_entero("Id estudiante A: "),
                                             pedir_entero("Id estudiante B: "))
            # Si salió bien, res es un set de materias.
            if ok:
                mostrar_materias(res)
            # Si falló, res es el mensaje de error.
            else:
                error(res)
        # Opción 9: todas las materias ofertadas.
        elif op == "9":
            mostrar_materias(c.materias_ofertadas())
        # Opción 0: salir.
        elif op == "0":
            # break rompe el while y el programa termina.
            break
        # Cualquier otra cosa es opción inválida.
        else:
            error("Opción inválida.")


# Esto se cumple solo al ejecutar este archivo directamente (python main.py).
if __name__ == "__main__":
    # Arrancamos el programa.
    main()


