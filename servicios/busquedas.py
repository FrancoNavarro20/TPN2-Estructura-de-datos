"""
servicios/busquedas.py — Búsquedas secuenciales sobre el catálogo

¿QUÉ ES UNA BÚSQUEDA SECUENCIAL?
    Es recorrer la lista elemento por elemento, desde el primero hasta
    encontrar lo que buscamos (o hasta el final si no está).

    Es la forma más simple de buscar, pero la más lenta: en el PEOR CASO
    hay que mirar TODOS los elementos → O(n).

¿POR QUÉ CONTAMOS COMPARACIONES?
    Para poder comparar con el BST y demostrar que el árbol es más
    eficiente. Cada vez que preguntamos "¿es este el que busco?" cuenta
    como una comparación.
"""


def buscar_por_codigo_secuencial(catalogo: list, codigo: str) -> tuple:
    """
    Busca un libro por código recorriendo la lista de principio a fin.

    Args:
        catalogo: lista de objetos Libro.
        codigo: código a buscar (ej. "L015").

    Returns:
        Tupla (libro, comparaciones) si lo encuentra.
        Tupla (None, comparaciones) si no lo encuentra.

    Ejemplo:
        >>> libro, comps = buscar_por_codigo_secuencial(catalogo, "L015")
        >>> print(f"Encontrado en {comps} comparaciones")
    """
    comparaciones = 0
    for libro in catalogo:
        comparaciones += 1
        if libro.codigo == codigo:
            return (libro, comparaciones)
    # No se encontró: se recorrió toda la lista
    return (None, comparaciones)


def buscar_por_titulo_secuencial(catalogo: list, titulo: str) -> tuple:
    """
    Busca un libro por título (búsqueda parcial, sin distinguir mayúsculas).

    ¿POR QUÉ PARCIAL Y CASE-INSENSITIVE?
        Porque el usuario no siempre recuerda el título exacto.
        Si busca "cien años", debería encontrar "Cien años de soledad".

    Args:
        catalogo: lista de objetos Libro.
        titulo: texto a buscar dentro del título.

    Returns:
        Tupla (libro, comparaciones) del PRIMER libro cuyo título
        contenga el texto buscado.
        Tupla (None, comparaciones) si no se encuentra.
    """
    comparaciones = 0
    titulo_lower = titulo.lower()
    for libro in catalogo:
        comparaciones += 1
        if titulo_lower in libro.titulo.lower():
            return (libro, comparaciones)
    return (None, comparaciones)


def buscar_por_autor(catalogo: list, autor: str) -> tuple:
    """
    Busca TODOS los libros de un autor (puede haber más de uno).

    ¿POR QUÉ DEVUELVE UNA LISTA?
        Porque un autor puede tener varios libros en el catálogo.
        A diferencia de buscar_por_codigo (que es única), acá necesitamos
        recorrer TODA la lista siempre.

    Args:
        catalogo: lista de objetos Libro.
        autor: nombre (parcial) del autor a buscar.

    Returns:
        Tupla (lista_de_libros, comparaciones).
        Si no se encuentra ninguno, la lista estará vacía.
    """
    comparaciones = 0
    encontrados = []
    autor_lower = autor.lower()
    for libro in catalogo:
        comparaciones += 1
        if autor_lower in libro.autor.lower():
            encontrados.append(libro)
    return (encontrados, comparaciones)
