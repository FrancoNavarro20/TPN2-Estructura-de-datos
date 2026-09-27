"""
ui/menu.py — Menú de consola interactivo

Este módulo maneja toda la interacción con el usuario.
Cada opción del menú llama a funciones de los módulos de servicios
y estructuras.

¿POR QUÉ SEPARAR EL MENÚ DEL RESTO?
    Porque el menú es la INTERFAZ (la "cara" del programa) y no debe
    contener lógica de negocio. Si mañana quisiéramos cambiar la consola
    por una interfaz gráfica, solo habría que reescribir este archivo;
    el resto del programa seguiría funcionando igual.
"""

from modelos.libro import Libro
from estructuras.arbol_bst import (
    construir_bst, construir_bst_balanceado, inorden
)
from estructuras.arbol_categorias import (
    construir_arbol_categorias, asignar_libros_a_categorias
)
from estructuras.pila import Pila
from estructuras.cola import Cola
from servicios.busquedas import (
    buscar_por_codigo_secuencial, buscar_por_titulo_secuencial,
    buscar_por_autor
)
from servicios.persistencia import guardar_catalogo
from servicios.estadisticas import mostrar_estadisticas
from servicios.comparador import comparar_eficiencia


# ====================================================================== #
#  Constantes                                                              #
# ====================================================================== #

BANNER = """
╔══════════════════════════════════════════════════════╗
║         📚  SISTEMA DE BIBLIOTECA  📚               ║
║         Catálogo de Libros — TP Estructuras          ║
╚══════════════════════════════════════════════════════╝
"""

OPCIONES_MENU = """
┌──────────────────────────────────────────────────────┐
│                   MENÚ PRINCIPAL                     │
├──────────────────────────────────────────────────────┤
│  1. Buscar por código (lista — secuencial)           │
│  2. Buscar por código (árbol BST)                    │
│  3. Buscar por título                                │
│  4. Explorar por categorías                          │
│  5. Listar catálogo ordenado (inorden BST)           │
│  6. Insertar libro                                   │
│  7. Eliminar libro                                   │
│  8. Deshacer última operación                        │
│  9. Ver historial de búsquedas                       │
│ 10. Estadísticas                                     │
│ 11. Comparar eficiencia (tabla + gráfico)            │
│ 12. Guardar catálogo                                 │
│  0. Salir (guarda antes de cerrar)                   │
└──────────────────────────────────────────────────────┘
"""


class Menu:
    """
    Controlador del menú de consola.

    Mantiene el estado del programa:
        - catalogo: lista de Libro
        - arbol_categorias: NodoCategoria raíz
        - bst_balanceado: NodoBST raíz
        - bst_degenerado: NodoBST raíz (solo para comparación)
        - pila_deshacer: Pila para operaciones de undo
        - historial_busquedas: Cola con las últimas 5 búsquedas
        - archivo_json: ruta del archivo de persistencia
    """

    def __init__(self, catalogo: list, archivo_json: str = "datos/catalogo.json"):
        """
        Inicializa el menú con el catálogo cargado.

        Args:
            catalogo: lista de objetos Libro ya cargados del JSON.
            archivo_json: ruta del archivo JSON para guardar.
        """
        self.catalogo = catalogo
        self.archivo_json = archivo_json

        # Armar las estructuras
        self.arbol_categorias = construir_arbol_categorias()
        asignar_libros_a_categorias(self.arbol_categorias, self.catalogo)

        self.bst_balanceado = construir_bst_balanceado(self.catalogo, "codigo")
        self.bst_degenerado = construir_bst(self.catalogo, "codigo")

        # Pila para deshacer (LIFO)
        self.pila_deshacer = Pila()

        # Cola para historial de búsquedas (FIFO, máx 5)
        self.historial_busquedas = Cola(maximo=5)

    def _reconstruir_estructuras(self):
        """
        Reconstruye el árbol de categorías y los BSTs después de
        insertar o eliminar un libro.

        ¿POR QUÉ RECONSTRUIR?
            Porque los árboles no se modifican fácilmente después de
            crearse. Es más simple y seguro reconstruirlos desde cero.
            Con 30 elementos es instantáneo.
        """
        self.arbol_categorias = construir_arbol_categorias()
        asignar_libros_a_categorias(self.arbol_categorias, self.catalogo)
        self.bst_balanceado = construir_bst_balanceado(self.catalogo, "codigo")
        self.bst_degenerado = construir_bst(self.catalogo, "codigo")

    # ================================================================== #
    #  Bucle principal del menú                                           #
    # ================================================================== #

    def ejecutar(self):
        """
        Bucle principal: muestra el menú, lee la opción y ejecuta
        la acción correspondiente. Se repite hasta que el usuario
        elige "0. Salir".
        """
        print(BANNER)

        while True:
            print(OPCIONES_MENU)
            opcion = input("  👉 Elegí una opción: ").strip()

            if opcion == "1":
                self._buscar_codigo_secuencial()
            elif opcion == "2":
                self._buscar_codigo_bst()
            elif opcion == "3":
                self._buscar_titulo()
            elif opcion == "4":
                self._explorar_categorias()
            elif opcion == "5":
                self._listar_inorden()
            elif opcion == "6":
                self._insertar_libro()
            elif opcion == "7":
                self._eliminar_libro()
            elif opcion == "8":
                self._deshacer()
            elif opcion == "9":
                self._ver_historial()
            elif opcion == "10":
                self._estadisticas()
            elif opcion == "11":
                self._comparar_eficiencia()
            elif opcion == "12":
                self._guardar()
            elif opcion == "0":
                self._salir()
                break
            else:
                print("\n  ❌ Opción inválida. Ingresá un número del 0 al 12.")

    # ================================================================== #
    #  Implementación de cada opción                                      #
    # ================================================================== #

    def _buscar_codigo_secuencial(self):
        """Opción 1: Buscar por código usando búsqueda secuencial en la lista."""
        codigo = input("  📖 Ingresá el código (ej. L015): ").strip().upper()
        if not codigo:
            print("  ❌ El código no puede estar vacío.")
            return

        libro, comparaciones = buscar_por_codigo_secuencial(self.catalogo, codigo)
        self.historial_busquedas.encolar(f"Código(seq): {codigo}")

        if libro:
            print(f"\n  ✅ Encontrado en {comparaciones} comparaciones:")
            print(f"     {libro}")
        else:
            print(f"\n  ❌ No se encontró '{codigo}' "
                  f"({comparaciones} comparaciones realizadas).")

    def _buscar_codigo_bst(self):
        """Opción 2: Buscar por código usando el BST balanceado."""
        codigo = input("  📖 Ingresá el código (ej. L015): ").strip().upper()
        if not codigo:
            print("  ❌ El código no puede estar vacío.")
            return

        if self.bst_balanceado is None:
            print("  ❌ El árbol BST está vacío.")
            return

        libro, comparaciones = self.bst_balanceado.buscar(codigo)
        self.historial_busquedas.encolar(f"Código(BST): {codigo}")

        if libro:
            print(f"\n  ✅ Encontrado en {comparaciones} comparaciones (BST):")
            print(f"     {libro}")
        else:
            print(f"\n  ❌ No se encontró '{codigo}' "
                  f"({comparaciones} comparaciones realizadas en BST).")

    def _buscar_titulo(self):
        """Opción 3: Buscar por título (parcial, sin distinguir mayúsculas)."""
        titulo = input("  📖 Ingresá parte del título: ").strip()
        if not titulo:
            print("  ❌ El título no puede estar vacío.")
            return

        libro, comparaciones = buscar_por_titulo_secuencial(self.catalogo, titulo)
        self.historial_busquedas.encolar(f"Título: {titulo}")

        if libro:
            print(f"\n  ✅ Encontrado en {comparaciones} comparaciones:")
            print(f"     {libro}")
        else:
            print(f"\n  ❌ No se encontró ningún libro con '{titulo}' "
                  f"({comparaciones} comparaciones).")

    def _explorar_categorias(self):
        """Opción 4: Mostrar el árbol de categorías y explorar una."""
        print("\n  🌳 ÁRBOL DE CATEGORÍAS:\n")
        self.arbol_categorias.mostrar(nivel=1)

        print()
        nombre = input("  📂 Ingresá el nombre de una categoría para ver "
                        "sus libros (o Enter para volver): ").strip()
        if not nombre:
            return

        nodo = self.arbol_categorias.buscar_categoria(nombre)
        if nodo is None:
            print(f"  ❌ No se encontró la categoría '{nombre}'.")
            return

        libros = nodo.listar_todos()
        if not libros:
            print(f"  📂 La categoría '{nodo.nombre}' no tiene libros.")
        else:
            print(f"\n  📂 Libros en '{nodo.nombre}' "
                  f"({len(libros)} encontrado/s):\n")
            for libro in libros:
                print(f"     {libro}")

    def _listar_inorden(self):
        """Opción 5: Listar el catálogo ordenado por código (recorrido inorden del BST)."""
        if self.bst_balanceado is None:
            print("  ❌ El catálogo está vacío.")
            return

        libros_ordenados = inorden(self.bst_balanceado)
        print(f"\n  📋 CATÁLOGO ORDENADO POR CÓDIGO "
              f"(recorrido inorden del BST, {len(libros_ordenados)} libros):\n")
        for i, libro in enumerate(libros_ordenados, 1):
            print(f"  {i:3}. {libro}")

    def _insertar_libro(self):
        """Opción 6: Insertar un nuevo libro al catálogo."""
        print("\n  📝 INSERTAR NUEVO LIBRO")
        print("  " + "-" * 40)

        try:
            codigo = input("  Código (ej. L031): ").strip().upper()
            if not codigo:
                print("  ❌ El código no puede estar vacío.")
                return

            # Verificar que no exista ya
            for libro in self.catalogo:
                if libro.codigo == codigo:
                    print(f"  ❌ Ya existe un libro con código '{codigo}'.")
                    return

            titulo = input("  Título: ").strip()
            if not titulo:
                print("  ❌ El título no puede estar vacío.")
                return

            autor = input("  Autor: ").strip()
            categoria = input("  Categoría: ").strip()

            # Verificar que la categoría exista en el árbol
            nodo_cat = self.arbol_categorias.buscar_categoria(categoria)
            if nodo_cat is None:
                print(f"  ⚠️  La categoría '{categoria}' no existe en el árbol.")
                print("  Categorías disponibles:")
                self.arbol_categorias.mostrar(nivel=2)
                return

            anio_str = input("  Año de publicación: ").strip()
            anio = int(anio_str)

            cantidad_str = input("  Cantidad de ejemplares: ").strip()
            cantidad = int(cantidad_str)

            # Crear el libro (las validaciones están en el constructor)
            nuevo_libro = Libro(codigo, titulo, autor, categoria, anio, cantidad)
            self.catalogo.append(nuevo_libro)

            # Apilar operación inversa para deshacer
            self.pila_deshacer.apilar(("eliminar", nuevo_libro))

            # Reconstruir las estructuras
            self._reconstruir_estructuras()

            print(f"\n  ✅ Libro insertado: {nuevo_libro}")

        except ValueError as e:
            print(f"  ❌ Error en los datos: {e}")

    def _eliminar_libro(self):
        """Opción 7: Eliminar un libro del catálogo por código."""
        codigo = input("  📖 Código del libro a eliminar: ").strip().upper()
        if not codigo:
            print("  ❌ El código no puede estar vacío.")
            return

        # Buscar el libro
        libro_a_eliminar = None
        for libro in self.catalogo:
            if libro.codigo == codigo:
                libro_a_eliminar = libro
                break

        if libro_a_eliminar is None:
            print(f"  ❌ No se encontró un libro con código '{codigo}'.")
            return

        # Eliminar
        self.catalogo.remove(libro_a_eliminar)

        # Apilar operación inversa para deshacer
        self.pila_deshacer.apilar(("insertar", libro_a_eliminar))

        # Reconstruir las estructuras
        self._reconstruir_estructuras()

        print(f"\n  🗑️  Libro eliminado: {libro_a_eliminar}")

    def _deshacer(self):
        """
        Opción 8: Deshacer la última operación de insertar o eliminar.

        ¿CÓMO FUNCIONA?
            La pila guarda tuplas (acción_inversa, libro).
            Si la última operación fue "insertar", la inversa es "eliminar".
            Si fue "eliminar", la inversa es "insertar".
        """
        if self.pila_deshacer.esta_vacia():
            print("  ❌ No hay operaciones para deshacer.")
            return

        accion, libro = self.pila_deshacer.desapilar()

        if accion == "insertar":
            # Deshacer una eliminación → re-insertar el libro
            self.catalogo.append(libro)
            print(f"  ↩️  Deshecho: se re-insertó '{libro.titulo}'.")
        elif accion == "eliminar":
            # Deshacer una inserción → eliminar el libro
            self.catalogo.remove(libro)
            print(f"  ↩️  Deshecho: se eliminó '{libro.titulo}'.")

        # Reconstruir las estructuras
        self._reconstruir_estructuras()

    def _ver_historial(self):
        """Opción 9: Muestra las últimas 5 búsquedas realizadas."""
        historial = self.historial_busquedas.listar()
        if not historial:
            print("  📜 El historial de búsquedas está vacío.")
            return

        print(f"\n  📜 ÚLTIMAS {len(historial)} BÚSQUEDAS:")
        for i, busqueda in enumerate(historial, 1):
            print(f"  {i}. {busqueda}")

    def _estadisticas(self):
        """Opción 10: Muestra estadísticas del catálogo."""
        mostrar_estadisticas(
            self.catalogo,
            self.arbol_categorias,
            self.bst_balanceado,
            self.bst_degenerado,
        )

    def _comparar_eficiencia(self):
        """Opción 11: Compara eficiencia lista vs BST y genera gráfico."""
        comparar_eficiencia(self.catalogo)

    def _guardar(self):
        """Opción 12: Guarda el catálogo en el archivo JSON."""
        guardar_catalogo(self.catalogo, self.archivo_json)

    def _salir(self):
        """Opción 0: Guarda el catálogo y sale del programa."""
        print("\n  💾 Guardando catálogo antes de salir...")
        guardar_catalogo(self.catalogo, self.archivo_json)
        print("  👋 ¡Hasta la próxima!")
