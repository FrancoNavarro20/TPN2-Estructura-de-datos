"""
estructuras/arbol_categorias.py — Árbol general (n-ario) de categorías

¿QUÉ ES UN ÁRBOL GENERAL?
    Es una estructura jerárquica donde cada nodo puede tener cualquier
    cantidad de hijos (no solo dos como el BST). Lo usamos para representar
    la clasificación de libros:

        Biblioteca
        ├── Literatura
        │   ├── Ficción
        │   │   ├── Ciencia ficción
        │   │   └── Novela histórica
        │   ├── Poesía
        │   └── Cuento
        └── Técnicos
            ├── Programación
            ├── Matemática
            └── Bases de datos

¿POR QUÉ un árbol y no una lista?
    Porque las categorías tienen una relación padre-hijo natural.
    Con una lista plana perderíamos esa jerarquía y no podríamos, por ejemplo,
    pedir "todos los libros de Literatura" incluyendo los de Ficción,
    Ciencia ficción, Novela histórica, Poesía y Cuento de una sola vez.
"""


class NodoCategoria:
    """
    Un nodo del árbol general de categorías.

    Cada nodo tiene:
        - nombre (str): nombre de la categoría, ej. "Ficción"
        - subcategorias (list): lista de NodoCategoria hijos
        - elementos (list): lista de Libro que pertenecen a esta categoría

    Nota: los libros solo se almacenan en las categorías HOJA (las que no
    tienen subcategorías). Las categorías intermedias agrupan pero no
    contienen libros directamente.
    """

    def __init__(self, nombre: str):
        """
        Crea un nodo de categoría vacío.

        Args:
            nombre: nombre de la categoría (ej. "Ficción").
        """
        self.nombre = nombre
        self.subcategorias = []   # hijos del nodo (otros NodoCategoria)
        self.elementos = []       # libros asignados a ESTA categoría

    # ------------------------------------------------------------------ #
    #  Operaciones sobre la estructura                                    #
    # ------------------------------------------------------------------ #

    def agregar_subcategoria(self, nombre_sub: str) -> "NodoCategoria":
        """
        Agrega una subcategoría (hijo) a este nodo.

        ¿POR QUÉ devuelve el nuevo nodo?
            Para poder encadenar operaciones:
                ficcion = literatura.agregar_subcategoria("Ficción")
                ficcion.agregar_subcategoria("Ciencia ficción")

        Args:
            nombre_sub: nombre de la nueva subcategoría.

        Returns:
            El NodoCategoria recién creado.
        """
        nuevo = NodoCategoria(nombre_sub)
        self.subcategorias.append(nuevo)
        return nuevo

    def es_hoja(self) -> bool:
        """
        Un nodo es hoja si no tiene subcategorías.
        Las hojas son las categorías donde se guardan los libros.
        """
        return len(self.subcategorias) == 0

    # ------------------------------------------------------------------ #
    #  Recorridos                                                         #
    # ------------------------------------------------------------------ #

    def mostrar(self, nivel: int = 0):
        """
        Muestra el árbol completo con indentación, usando recorrido PREORDEN.

        ¿QUÉ ES PREORDEN?
            Primero visitamos el nodo actual y después sus hijos.
            Eso hace que se imprima la categoría padre antes que las sub.

        Args:
            nivel: profundidad actual (para la indentación). Se incrementa
                   en cada llamada recursiva.
        """
        # Indentación: 4 espacios por nivel
        prefijo = "    " * nivel
        # Símbolo visual según si es hoja o no
        marcador = "📄" if self.es_hoja() else "📁"
        cantidad = len(self.elementos)
        print(f"{prefijo}{marcador} {self.nombre} ({cantidad} libro/s)")

        # Llamada recursiva a cada hijo (recorrido preorden)
        for sub in self.subcategorias:
            sub.mostrar(nivel + 1)

    def buscar_categoria(self, nombre_buscado: str) -> "NodoCategoria | None":
        """
        Busca una categoría por nombre en todo el subárbol.

        Usa BÚSQUEDA EN PROFUNDIDAD (DFS) recursiva:
        primero chequea el nodo actual y luego baja por cada hijo.

        Args:
            nombre_buscado: nombre de la categoría a encontrar
                            (comparación case-insensitive).

        Returns:
            El NodoCategoria encontrado, o None si no existe.
        """
        # Caso base: este nodo es el buscado
        if self.nombre.lower() == nombre_buscado.lower():
            return self

        # Caso recursivo: buscar en cada subárbol hijo
        for sub in self.subcategorias:
            resultado = sub.buscar_categoria(nombre_buscado)
            if resultado is not None:
                return resultado

        # No se encontró en ningún subárbol
        return None

    def contar_elementos(self) -> int:
        """
        Cuenta TODOS los libros del subárbol: los propios + los de
        todas las subcategorías (recursivamente).

        ¿POR QUÉ recursiva?
            Porque "Literatura" incluye los libros de Ficción,
            Ciencia ficción, Novela histórica, Poesía y Cuento.
            No basta con contar solo los de este nodo.

        Returns:
            Total de libros en este subárbol.
        """
        total = len(self.elementos)
        for sub in self.subcategorias:
            total += sub.contar_elementos()
        return total

    def altura(self) -> int:
        """
        Calcula la altura del subárbol desde este nodo.

        La altura de una hoja es 0.
        La altura de un nodo interno es 1 + max(altura de sus hijos).

        Returns:
            Altura del subárbol.
        """
        if self.es_hoja():
            return 0
        return 1 + max(sub.altura() for sub in self.subcategorias)

    def listar_todos(self) -> list:
        """
        Devuelve TODOS los libros de este subárbol (propios + descendientes).

        Returns:
            Lista plana con todos los Libro del subárbol.
        """
        todos = list(self.elementos)  # copia de los propios
        for sub in self.subcategorias:
            todos.extend(sub.listar_todos())
        return todos


# ====================================================================== #
#  Función para armar la jerarquía completa de la biblioteca              #
# ====================================================================== #

def construir_arbol_categorias() -> NodoCategoria:
    """
    Construye y devuelve el árbol de categorías de la biblioteca.

    Jerarquía:
        Biblioteca
        ├── Literatura
        │   ├── Ficción
        │   │   ├── Ciencia ficción
        │   │   └── Novela histórica
        │   ├── Poesía
        │   └── Cuento
        └── Técnicos
            ├── Programación
            ├── Matemática
            └── Bases de datos

    Returns:
        NodoCategoria raíz ("Biblioteca").
    """
    raiz = NodoCategoria("Biblioteca")

    # --- Rama "Literatura" ---
    literatura = raiz.agregar_subcategoria("Literatura")
    ficcion = literatura.agregar_subcategoria("Ficción")
    ficcion.agregar_subcategoria("Ciencia ficción")
    ficcion.agregar_subcategoria("Novela histórica")
    literatura.agregar_subcategoria("Poesía")
    literatura.agregar_subcategoria("Cuento")

    # --- Rama "Técnicos" ---
    tecnicos = raiz.agregar_subcategoria("Técnicos")
    tecnicos.agregar_subcategoria("Programación")
    tecnicos.agregar_subcategoria("Matemática")
    tecnicos.agregar_subcategoria("Bases de datos")

    return raiz


def asignar_libros_a_categorias(raiz: NodoCategoria, catalogo: list):
    """
    Recorre el catálogo y asigna cada libro al nodo hoja que corresponda
    según su atributo 'categoria'.

    Args:
        raiz: nodo raíz del árbol de categorías.
        catalogo: lista de objetos Libro.
    """
    for libro in catalogo:
        nodo = raiz.buscar_categoria(libro.categoria)
        if nodo is not None:
            nodo.elementos.append(libro)
        else:
            # Si la categoría no existe en el árbol, lo dejamos en la raíz
            raiz.elementos.append(libro)
