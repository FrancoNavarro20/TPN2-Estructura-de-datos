"""
main.py — Punto de entrada del sistema de Biblioteca

Este archivo es el que se ejecuta con `python main.py`.
Su trabajo es simple:
    1. Cargar el catálogo desde el JSON.
    2. Crear el menú con el catálogo cargado.
    3. Ejecutar el bucle del menú.

Toda la lógica pesada está en los otros módulos.
"""

from servicios.persistencia import cargar_catalogo
from ui.menu import Menu


def main():
    """Función principal del programa."""
    # 1. Cargar el catálogo desde el archivo JSON
    catalogo = cargar_catalogo("datos/catalogo.json")

    # 2. Crear el menú con el catálogo
    menu = Menu(catalogo, archivo_json="datos/catalogo.json")

    # 3. Ejecutar el menú interactivo
    menu.ejecutar()


if __name__ == "__main__":
    main()
