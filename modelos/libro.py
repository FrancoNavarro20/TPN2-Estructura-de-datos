"""
modelos/libro.py — Clase Libro (dominio del problema)

Este módulo define la clase principal del sistema: Libro.
Representa un libro físico en la biblioteca, con sus datos básicos
y la cantidad de ejemplares disponibles.

¿POR QUÉ encapsulamiento?
    Usamos atributos privados (_codigo, _titulo, etc.) y @property para
    controlar el acceso. Así nadie puede, por ejemplo, poner una cantidad
    negativa directamente: tiene que pasar por el setter que lo valida.
"""


class Libro:
    """
    Representa un libro del catálogo de la biblioteca.

    Atributos privados:
        _codigo   (str) : identificador único, ej. "L001"
        _titulo   (str) : título del libro
        _autor    (str) : autor principal
        _categoria(str) : categoría hoja del árbol de categorías
        _anio     (int) : año de publicación
        _cantidad (int) : ejemplares disponibles (>= 0)

    Ejemplo de uso:
        >>> libro = Libro("L001", "Cien años de soledad",
        ...               "Gabriel García Márquez", "Ficción", 1967, 3)
        >>> print(libro)
        [L001] Cien años de soledad — Gabriel García Márquez (1967) | Ej: 3
    """

    def __init__(self, codigo: str, titulo: str, autor: str,
                 categoria: str, anio: int, cantidad: int):
        """
        Crea un nuevo Libro validando los datos obligatorios.

        Raises:
            ValueError: si código o título están vacíos,
                        o si cantidad es negativa.
        """
        # --- Validaciones ---
        if not codigo or not codigo.strip():
            raise ValueError("El código del libro no puede estar vacío.")
        if not titulo or not titulo.strip():
            raise ValueError("El título del libro no puede estar vacío.")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        # --- Asignación de atributos privados ---
        self._codigo = codigo.strip()
        self._titulo = titulo.strip()
        self._autor = autor.strip() if autor else "Desconocido"
        self._categoria = categoria.strip() if categoria else "Sin categoría"
        self._anio = anio
        self._cantidad = cantidad

    # ------------------------------------------------------------------ #
    #  Properties: permiten leer los atributos sin modificarlos           #
    # ------------------------------------------------------------------ #

    @property
    def codigo(self) -> str:
        """Devuelve el código identificador del libro."""
        return self._codigo

    @property
    def titulo(self) -> str:
        """Devuelve el título del libro."""
        return self._titulo

    @property
    def autor(self) -> str:
        """Devuelve el autor del libro."""
        return self._autor

    @property
    def categoria(self) -> str:
        """Devuelve la categoría del libro."""
        return self._categoria

    @property
    def anio(self) -> int:
        """Devuelve el año de publicación."""
        return self._anio

    @property
    def cantidad(self) -> int:
        """Devuelve la cantidad de ejemplares disponibles."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        """
        Modifica la cantidad de ejemplares.

        ¿POR QUÉ un setter?
            Porque necesitamos validar que nadie ponga un número negativo.
            Si alguien escribe `libro.cantidad = -5`, Python llama a este
            método y nosotros lanzamos un error antes de que se guarde.

        Raises:
            ValueError: si nueva_cantidad es negativa.
        """
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = nueva_cantidad

    # ------------------------------------------------------------------ #
    #  Métodos de instancia                                               #
    # ------------------------------------------------------------------ #

    def disponible(self) -> bool:
        """
        Indica si hay al menos un ejemplar disponible.

        Returns:
            True si cantidad > 0, False en caso contrario.
        """
        return self._cantidad > 0

    def a_diccionario(self) -> dict:
        """
        Convierte el libro en un diccionario para poder guardarlo en JSON.

        ¿POR QUÉ?
            JSON no sabe serializar objetos Python directamente.
            Necesitamos convertir el objeto a un dict de tipos básicos
            (str, int) para poder escribirlo en un archivo.

        Returns:
            dict con las claves: codigo, titulo, autor, categoria, anio, cantidad.
        """
        return {
            "codigo": self._codigo,
            "titulo": self._titulo,
            "autor": self._autor,
            "categoria": self._categoria,
            "anio": self._anio,
            "cantidad": self._cantidad,
        }

    def __str__(self) -> str:
        """
        Representación legible del libro para mostrar en consola.

        Ejemplo:
            [L001] Cien años de soledad — Gabriel García Márquez (1967) | Ej: 3
        """
        return (f"[{self._codigo}] {self._titulo} — {self._autor} "
                f"({self._anio}) | Ej: {self._cantidad}")

    def __repr__(self) -> str:
        """Representación técnica (útil al depurar)."""
        return (f"Libro('{self._codigo}', '{self._titulo}', '{self._autor}', "
                f"'{self._categoria}', {self._anio}, {self._cantidad})")
