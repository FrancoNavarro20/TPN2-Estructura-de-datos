"""
estructuras/cola.py — Cola (FIFO) implementada a mano

¿QUÉ ES UNA COLA?
    Es una estructura donde el PRIMER elemento que entra es el PRIMERO
    que sale (First In, First Out — FIFO).

    Pensalo como la cola del supermercado: el primero que llegó es
    el primero que atienden.

    Operaciones:
        encolar()     → agrega un elemento al final
        desencolar()  → saca y devuelve el primero
        esta_vacia()  → ¿hay algo?
        listar()      → muestra todos los elementos en orden

¿PARA QUÉ LA USAMOS?
    Para mantener un HISTORIAL de las últimas 5 búsquedas.
    Cuando se llega al máximo, se descarta la más vieja (la primera
    que entró) automáticamente.

¿POR QUÉ TAMAÑO MÁXIMO?
    Porque el historial solo muestra las últimas N búsquedas.
    No tiene sentido guardar miles de búsquedas viejas.
"""


class _NodoCola:
    """
    Nodo interno de la cola.
    Cada nodo apunta al siguiente (el que llegó después).
    """

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Cola:
    """
    Cola (FIFO) con tamaño máximo, implementada como lista enlazada.

    Mantiene un puntero al FRENTE (para desencolar rápido) y otro
    al FINAL (para encolar rápido). Ambas operaciones son O(1).
    """

    def __init__(self, maximo: int = 5):
        """
        Crea una cola vacía con un tamaño máximo.

        Args:
            maximo: cantidad máxima de elementos. Cuando se supera,
                    se descarta el más viejo automáticamente.
        """
        self._frente = None    # primer nodo (el más viejo)
        self._final = None     # último nodo (el más nuevo)
        self._tamanio = 0
        self._maximo = maximo

    def encolar(self, dato):
        """
        Agrega un elemento al final de la cola.

        Si la cola ya tiene el máximo de elementos, DESCARTA el más
        viejo (el del frente) antes de agregar el nuevo.

        Args:
            dato: el elemento a encolar.
        """
        nuevo_nodo = _NodoCola(dato)

        if self.esta_vacia():
            # Primer elemento: frente y final son el mismo
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            # El nodo actual del final apunta al nuevo
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo

        self._tamanio += 1

        # Si nos pasamos del máximo, descartamos el más viejo
        if self._tamanio > self._maximo:
            self.desencolar()

    def desencolar(self):
        """
        Saca y devuelve el elemento del frente (el más viejo).

        Returns:
            El dato del frente.

        Raises:
            IndexError: si la cola está vacía.
        """
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola está vacía.")

        dato = self._frente.dato
        self._frente = self._frente.siguiente  # el frente pasa al siguiente

        # Si la cola quedó vacía, el final también es None
        if self._frente is None:
            self._final = None

        self._tamanio -= 1
        return dato

    def esta_vacia(self) -> bool:
        """Devuelve True si la cola no tiene elementos."""
        return self._frente is None

    def tamanio(self) -> int:
        """Devuelve la cantidad de elementos actuales en la cola."""
        return self._tamanio

    def listar(self) -> list:
        """
        Devuelve todos los elementos de la cola en orden (del más viejo
        al más nuevo) SIN sacarlos.

        Returns:
            Lista con los datos de la cola.
        """
        elementos = []
        actual = self._frente
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __str__(self) -> str:
        """Representación visual de la cola (de frente a final)."""
        elementos = self.listar()
        if not elementos:
            return "(cola vacía)"
        return " → ".join(str(e) for e in elementos)
