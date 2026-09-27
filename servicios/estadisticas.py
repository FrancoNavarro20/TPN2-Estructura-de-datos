"""
servicios/estadisticas.py — Estadísticas del catálogo

Este módulo calcula métricas globales del catálogo para la opción
"Estadísticas" del menú. Trabaja sobre la lista de libros y los
árboles (categorías y BST) para dar un panorama completo.
"""


def mostrar_estadisticas(catalogo: list, arbol_categorias, bst_balanceado,
                          bst_degenerado):
    """
    Calcula y muestra todas las estadísticas del catálogo.

    Args:
        catalogo: lista de objetos Libro.
        arbol_categorias: NodoCategoria raíz del árbol de categorías.
        bst_balanceado: NodoBST raíz del BST balanceado (puede ser None).
        bst_degenerado: NodoBST raíz del BST degenerado (puede ser None).
    """
    if not catalogo:
        print("📊 El catálogo está vacío. No hay estadísticas que mostrar.")
        return

    print("\n" + "=" * 60)
    print("📊  ESTADÍSTICAS DEL CATÁLOGO")
    print("=" * 60)

    # --- Total de libros (títulos distintos) ---
    total_libros = len(catalogo)
    print(f"\n📚 Total de títulos en catálogo: {total_libros}")

    # --- Suma total de ejemplares ---
    total_ejemplares = sum(libro.cantidad for libro in catalogo)
    print(f"📦 Total de ejemplares (suma): {total_ejemplares}")

    # --- Libros sin stock ---
    sin_stock = [libro for libro in catalogo if not libro.disponible()]
    print(f"🚫 Títulos sin stock: {len(sin_stock)}")
    for libro in sin_stock:
        print(f"    - {libro}")

    # --- Alturas de los árboles ---
    print(f"\n🌳 Altura del árbol de categorías: {arbol_categorias.altura()}")
    if bst_balanceado:
        print(f"🌲 Altura del BST balanceado: {bst_balanceado.altura()}")
    else:
        print("🌲 BST balanceado: (vacío)")
    if bst_degenerado:
        print(f"🌲 Altura del BST degenerado: {bst_degenerado.altura()}")
    else:
        print("🌲 BST degenerado: (vacío)")

    # --- Cantidad por categoría (recorriendo el árbol de categorías) ---
    print("\n📂 Libros por categoría (árbol de categorías):")
    _mostrar_cantidad_por_categoria(arbol_categorias, nivel=1)

    # --- Autor con más obras ---
    conteo_autores = {}
    for libro in catalogo:
        conteo_autores[libro.autor] = conteo_autores.get(libro.autor, 0) + 1

    autor_max = max(conteo_autores, key=conteo_autores.get)
    print(f"\n✍️  Autor con más obras: {autor_max} "
          f"({conteo_autores[autor_max]} libro/s)")

    # --- Año más antiguo y más nuevo ---
    anio_min = min(catalogo, key=lambda l: l.anio)
    anio_max = max(catalogo, key=lambda l: l.anio)
    print(f"📅 Libro más antiguo: {anio_min.titulo} ({anio_min.anio})")
    print(f"📅 Libro más reciente: {anio_max.titulo} ({anio_max.anio})")

    print("\n" + "=" * 60)


def _mostrar_cantidad_por_categoria(nodo, nivel: int = 0):
    """
    Muestra recursivamente la cantidad de libros en cada categoría
    del árbol (incluyendo subcategorías).

    Args:
        nodo: NodoCategoria a recorrer.
        nivel: profundidad para la indentación.
    """
    prefijo = "    " * nivel
    total = nodo.contar_elementos()
    propios = len(nodo.elementos)

    if nodo.es_hoja():
        print(f"{prefijo}📄 {nodo.nombre}: {propios} libro/s")
    else:
        print(f"{prefijo}📁 {nodo.nombre}: {total} libro/s (total con sub)")
        for sub in nodo.subcategorias:
            _mostrar_cantidad_por_categoria(sub, nivel + 1)
