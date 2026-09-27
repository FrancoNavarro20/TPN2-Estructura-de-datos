"""
servicios/persistencia.py — Guardar y cargar el catálogo en JSON

¿POR QUÉ JSON?
    Porque es un formato de texto plano, legible por humanos, y Python
    tiene soporte nativo con el módulo 'json'. No necesitamos instalar
    nada extra ni usar una base de datos.

¿POR QUÉ encoding='utf-8' y ensure_ascii=False?
    Para que los acentos y caracteres especiales (á, é, ñ, etc.)
    se guarden correctamente en el archivo, en vez de convertirse
    en secuencias raras como \\u00e1.
"""

import json
import os

from modelos.libro import Libro


def guardar_catalogo(catalogo: list, archivo: str = "datos/catalogo.json"):
    """
    Guarda la lista de libros en un archivo JSON.

    Convierte cada objeto Libro a diccionario con a_diccionario()
    y escribe la lista de dicts en formato JSON indentado.

    Args:
        catalogo: lista de objetos Libro.
        archivo: ruta del archivo JSON de salida.
    """
    # Convertir cada Libro a diccionario
    datos = [libro.a_diccionario() for libro in catalogo]

    # Crear el directorio si no existe
    directorio = os.path.dirname(archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

    # Escribir el JSON
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print(f"✅ Catálogo guardado en '{archivo}' ({len(catalogo)} libros).")


def cargar_catalogo(archivo: str = "datos/catalogo.json") -> list:
    """
    Carga la lista de libros desde un archivo JSON.

    Si el archivo no existe, devuelve una lista vacía sin romper.

    ¿POR QUÉ NO ROMPEMOS SI NO EXISTE?
        Porque la primera vez que se ejecuta el programa, el archivo
        podría no existir todavía. Es mejor arrancar con un catálogo
        vacío que mostrar un error feo al usuario.

    Args:
        archivo: ruta del archivo JSON de entrada.

    Returns:
        Lista de objetos Libro.
    """
    if not os.path.exists(archivo):
        print(f"⚠️  Archivo '{archivo}' no encontrado. Se inicia con catálogo vacío.")
        return []

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️  El archivo '{archivo}' tiene formato inválido. "
              "Se inicia con catálogo vacío.")
        return []

    # Convertir cada diccionario a un objeto Libro
    catalogo = []
    for d in datos:
        try:
            libro = Libro(
                codigo=d["codigo"],
                titulo=d["titulo"],
                autor=d["autor"],
                categoria=d["categoria"],
                anio=d["anio"],
                cantidad=d["cantidad"],
            )
            catalogo.append(libro)
        except (KeyError, ValueError) as e:
            print(f"⚠️  Error al cargar libro: {e}. Se omite este registro.")

    print(f"📚 Catálogo cargado: {len(catalogo)} libros desde '{archivo}'.")
    return catalogo
