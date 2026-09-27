"""
estructuras/arbol_bst.py — Árbol Binario de Búsqueda (BST)

¿QUÉ ES UN BST?
    Es un árbol donde cada nodo tiene como máximo 2 hijos (izquierdo y derecho).
    La REGLA DE ORDEN es:
        - Todo lo que está a la IZQUIERDA tiene clave MENOR.
        - Todo lo que está a la DERECHA tiene clave MAYOR.

    Esto permite buscar un elemento en O(log n) en el mejor caso,
    en vez de O(n) como en una lista.

    Ejemplo con códigos de libros:
                    L015
                   /    \\
                L007    L023
               /    \\      \\
            L003   L010    L028

    Para buscar L010:
        L015 → es menor → voy a la izquierda (L007)
        L007 → es mayor → voy a la derecha (L010) → ¡encontrado!
        Solo necesité 3 comparaciones en vez de recorrer todo.

¿POR QUÉ HAY DOS FUNCIONES DE CONSTRUCCIÓN?
    ┌─────────────────────────────────────────────────────────────────┐
    │ PROBLEMA DEL ÁRBOL DEGENERADO                                  │
    │                                                                 │
    │ Si insertamos claves ya ordenadas (L001, L002, L003, ...),     │
    │ cada nodo nuevo va siempre a la derecha. El árbol se convierte │
    │ en una lista enlazada y la búsqueda vuelve a ser O(n):         │
    │                                                                 │
    │     L001                                                        │
    │       \\                                                         │
    │       L002                                                      │
    │         \\                                                       │
    │         L003      ← altura = n-1, igual que una lista           │
    │           \\                                                     │
    │           ...                                                   │
    │                                                                 │
    │ SOLUCIÓN: construir_bst_balanceado() ordena los datos y luego  │
    │ inserta primero el del MEDIO, después recursivamente los       │
    │ medios de cada mitad. Así el árbol queda parejo con altura     │
    │ ~log2(n).                                                       │
    │                                                                 │
    │ DEJAMOS AMBAS FUNCIONES para poder comparar y demostrar        │
    │ la diferencia en el trabajo práctico.                           │
    └─────────────────────────────────────────────────────────────────┘
"""


class NodoBST:
    """
    Un nodo del Árbol Binario de Búsqueda.

    Atributos:
        clave (str): valor por el cual se ordena (ej. código del libro).
        elemento: el objeto Libro asociado a este nodo.
        izquierda (NodoBST | None): hijo izquierdo (claves menores).
        derecha (NodoBST | None): hijo derecho (claves mayores).
    """

    def __init__(self, clave: str, elemento):
        self.clave = clave
        self.elemento = elemento
        self.izquierda = None
        self.derecha = None

    # ------------------------------------------------------------------ #
    #  Inserción recursiva                                                #
    # ------------------------------------------------------------------ #

    def insertar(self, clave: str, elemento) -> "NodoBST":
        """
        Inserta un nuevo elemento respetando la regla de orden del BST.

        ¿CÓMO FUNCIONA?
            1. Si la clave es MENOR que la del nodo actual → va a la izquierda.
            2. Si la clave es MAYOR → va a la derecha.
            3. Si la clave es IGUAL → NO se inserta (claves únicas).

        Args:
            clave: la clave del nuevo elemento.
            elemento: el objeto Libro a insertar.

        Returns:
            Este mismo nodo (para facilitar la recursión).
        """
        if clave < self.clave:
            if self.izquierda is None:
                self.izquierda = NodoBST(clave, elemento)
            else:
                self.izquierda.insertar(clave, elemento)
        elif clave > self.clave:
            if self.derecha is None:
                self.derecha = NodoBST(clave, elemento)
            else:
                self.derecha.insertar(clave, elemento)
        # Si clave == self.clave, no hacemos nada (clave repetida)
        return self

    # ------------------------------------------------------------------ #
    #  Búsqueda con contador de comparaciones                            #
    # ------------------------------------------------------------------ #

    def buscar(self, clave: str, comparaciones: int = 0):
        """
        Busca un elemento por clave, contando las comparaciones realizadas.

        ¿POR QUÉ CONTAMOS COMPARACIONES?
            Para demostrar que el BST balanceado necesita menos pasos
            que la búsqueda secuencial o el BST degenerado.

        Args:
            clave: la clave a buscar.
            comparaciones: acumulador (se incrementa en cada nodo visitado).

        Returns:
            Tupla (elemento, comparaciones) si lo encuentra.
            Tupla (None, comparaciones) si no lo encuentra.
        """
        comparaciones += 1  # cada nodo visitado es una comparación

        if clave == self.clave:
            return (self.elemento, comparaciones)
        elif clave < self.clave:
            if self.izquierda is None:
                return (None, comparaciones)
            return self.izquierda.buscar(clave, comparaciones)
        else:
            if self.derecha is None:
                return (None, comparaciones)
            return self.derecha.buscar(clave, comparaciones)

    # ------------------------------------------------------------------ #
    #  Métricas del árbol                                                 #
    # ------------------------------------------------------------------ #

    def altura(self) -> int:
        """
        Calcula la altura del subárbol desde este nodo.

        Altura de una hoja = 0.
        Altura de un nodo = 1 + max(altura izq, altura der).
        """
        alt_izq = self.izquierda.altura() if self.izquierda else -1
        alt_der = self.derecha.altura() if self.derecha else -1
        return 1 + max(alt_izq, alt_der)

    def contar_nodos(self) -> int:
        """Cuenta el total de nodos en el subárbol."""
        total = 1
        if self.izquierda:
            total += self.izquierda.contar_nodos()
        if self.derecha:
            total += self.derecha.contar_nodos()
        return total


# ====================================================================== #
#  Recorridos del BST                                                     #
#                                                                          #
#  Son funciones SUELTAS (no métodos) porque operan sobre el árbol         #
#  entero, que puede ser None (árbol vacío).                               #
# ====================================================================== #

def inorden(nodo: NodoBST | None, resultado: list = None) -> list:
    """
    Recorrido INORDEN: izquierda → raíz → derecha.

    ¿POR QUÉ ES ÚTIL?
        En un BST, el recorrido inorden devuelve los elementos
        ORDENADOS de menor a mayor. Es la forma de listar el catálogo
        en orden alfabético por código.

    Args:
        nodo: raíz del subárbol a recorrer.
        resultado: lista acumuladora (se crea nueva si no se pasa).

    Returns:
        Lista con los elementos en orden.
    """
    if resultado is None:
        resultado = []
    if nodo is not None:
        inorden(nodo.izquierda, resultado)
        resultado.append(nodo.elemento)
        inorden(nodo.derecha, resultado)
    return resultado


def preorden(nodo: NodoBST | None, resultado: list = None) -> list:
    """
    Recorrido PREORDEN: raíz → izquierda → derecha.

    ¿PARA QUÉ SIRVE?
        Es útil para copiar o serializar la estructura del árbol,
        porque primero visita la raíz antes de descender.
    """
    if resultado is None:
        resultado = []
    if nodo is not None:
        resultado.append(nodo.elemento)
        preorden(nodo.izquierda, resultado)
        preorden(nodo.derecha, resultado)
    return resultado


def postorden(nodo: NodoBST | None, resultado: list = None) -> list:
    """
    Recorrido POSTORDEN: izquierda → derecha → raíz.

    ¿PARA QUÉ SIRVE?
        Es útil para eliminar un árbol, porque procesa los hijos
        antes que el padre (así no perdemos referencias).
    """
    if resultado is None:
        resultado = []
    if nodo is not None:
        postorden(nodo.izquierda, resultado)
        postorden(nodo.derecha, resultado)
        resultado.append(nodo.elemento)
    return resultado


# ====================================================================== #
#  Funciones de CONSTRUCCIÓN del BST                                       #
# ====================================================================== #

def construir_bst(catalogo: list, clave: str) -> NodoBST | None:
    """
    Construye un BST insertando los elementos EN EL ORDEN en que vienen.

    ⚠️  CUIDADO: si el catálogo ya está ordenado por la clave (ej. L001, L002,
    L003...), el árbol resultante será DEGENERADO (una cadena lineal) y la
    búsqueda será tan lenta como en una lista (O(n)).

    Esta función existe para DEMOSTRAR el problema. En el programa real
    se usa construir_bst_balanceado().

    Args:
        catalogo: lista de objetos Libro.
        clave: nombre del atributo a usar como clave (ej. "codigo").

    Returns:
        La raíz del BST, o None si el catálogo está vacío.
    """
    if not catalogo:
        return None

    # El primer elemento se convierte en la raíz
    raiz = NodoBST(getattr(catalogo[0], clave), catalogo[0])

    # Los demás se insertan uno a uno
    for libro in catalogo[1:]:
        raiz.insertar(getattr(libro, clave), libro)

    return raiz


def construir_bst_balanceado(catalogo: list, clave: str) -> NodoBST | None:
    """
    Construye un BST BALANCEADO a partir de un catálogo.

    ¿CÓMO LO HACE?
        1. Ordena el catálogo por la clave.
        2. Toma el elemento del MEDIO como raíz.
        3. Recursivamente, toma el medio de la mitad izquierda (hijo izq)
           y el medio de la mitad derecha (hijo der).

    ¿POR QUÉ FUNCIONA?
        Al poner siempre el elemento del medio como raíz, cada subárbol
        tiene aproximadamente la misma cantidad de nodos a cada lado.
        Eso garantiza una altura de ~log2(n) en vez de n-1.

    Ejemplo con 7 elementos [1,2,3,4,5,6,7]:
        Medio = 4 (raíz)
        Mitad izq [1,2,3] → medio = 2
        Mitad der [5,6,7] → medio = 6

        Resultado:
                4
               / \\
              2   6
             / \\ / \\
            1  3 5  7
        Altura = 2 (log2(7) ≈ 2.8)

    Args:
        catalogo: lista de objetos Libro.
        clave: nombre del atributo a usar como clave (ej. "codigo").

    Returns:
        La raíz del BST balanceado, o None si el catálogo está vacío.
    """
    if not catalogo:
        return None

    # 1. Ordenar por la clave
    ordenado = sorted(catalogo, key=lambda libro: getattr(libro, clave))

    # 2. Construir recursivamente insertando siempre el del medio
    def _construir_recursivo(lista: list) -> NodoBST | None:
        """Función interna recursiva que arma el BST balanceado."""
        if not lista:
            return None

        medio = len(lista) // 2
        libro_medio = lista[medio]

        nodo = NodoBST(getattr(libro_medio, clave), libro_medio)
        nodo.izquierda = _construir_recursivo(lista[:medio])
        nodo.derecha = _construir_recursivo(lista[medio + 1:])

        return nodo

    return _construir_recursivo(ordenado)
