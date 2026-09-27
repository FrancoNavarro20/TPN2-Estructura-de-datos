"""
estructuras/pila.py — Pila (LIFO) implementada a mano

¿QUÉ ES UNA PILA?
    Es una estructura de datos donde el ÚLTIMO elemento que entra
    es el PRIMERO que sale (Last In, First Out — LIFO).

    Pensalo como una pila de platos: solo podés poner y sacar del TOPE.

    Operaciones:
        apilar()      → pone un elemento arriba de todo
        desapilar()   → saca y devuelve el de arriba
        ver_tope()    → mira el de arriba sin sacarlo
        esta_vacia()  → ¿hay algo?
        tamanio()     → ¿cuántos hay?

¿PARA QUÉ LA USAMOS?
    Para implementar DESHACER (undo). Cada vez que el usuario agrega o
    elimina un libro, apilamos la operación inversa. Si el usuario
    pide "deshacer", desapilamos y ejecutamos esa operación inversa.

¿POR QUÉ NO USAMOS collections.deque O una lista de Python directamente?
    Porque el trabajo práctico pide implementar la estructura A MANO
    para entender cómo funciona internamente.
"""


class _NodoPila:
    """
    Nodo interno de la pila (no se expone al usuario de la estructura).

    Cada nodo apunta al siguiente nodo de abajo en la pila.
    """

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Pila:
    """
    Pila (LIFO) implementada como lista enlazada.

    ¿POR QUÉ lista enlazada y no un array?
        Porque apilar y desapilar son O(1) sin importar el tamaño.
        No necesitamos redimensionar ni mover elementos.
    """

    def __init__(self):
        """Crea una pila vacía."""
        self._tope = None     # referencia al nodo del tope
        self._tamanio = 0     # cantidad de elementos

    def apilar(self, dato):
        """
        Agrega un elemento al tope de la pila.

        El nuevo nodo apunta al anterior tope, y se convierte
        en el nuevo tope.

        Args:
            dato: el elemento a apilar (puede ser cualquier cosa).
        """
        nuevo_nodo = _NodoPila(dato, self._tope)
        self._tope = nuevo_nodo
        self._tamanio += 1

    def desapilar(self):
        """
        Saca y devuelve el elemento del tope.

        Returns:
            El dato que estaba en el tope.

        Raises:
            IndexError: si la pila está vacía.
        """
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía.")

        dato = self._tope.dato
        self._tope = self._tope.siguiente  # el tope pasa a ser el de abajo
        self._tamanio -= 1
        return dato

    def ver_tope(self):
        """
        Devuelve el elemento del tope SIN sacarlo.

        Returns:
            El dato del tope.

        Raises:
            IndexError: si la pila está vacía.
        """
        if self.esta_vacia():
            raise IndexError("No se puede ver el tope: la pila está vacía.")
        return self._tope.dato

    def esta_vacia(self) -> bool:
        """Devuelve True si la pila no tiene elementos."""
        return self._tope is None

    def tamanio(self) -> int:
        """Devuelve la cantidad de elementos en la pila."""
        return self._tamanio

    def __str__(self) -> str:
        """Representación visual de la pila (de tope a base)."""
        elementos = []
        actual = self._tope
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return " → ".join(elementos) if elementos else "(pila vacía)"
