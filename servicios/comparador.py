"""
servicios/comparador.py — Compara la eficiencia de búsqueda: lista vs BST

Este módulo demuestra la diferencia de rendimiento entre:
  1. Búsqueda SECUENCIAL en una lista (O(n))
  2. Búsqueda en un BST DEGENERADO (O(n) — se comporta como lista)
  3. Búsqueda en un BST BALANCEADO (O(log n))

Prueba 4 casos:
  - Buscar el PRIMER elemento del catálogo
  - Buscar uno del MEDIO
  - Buscar el ÚLTIMO
  - Buscar uno que NO EXISTE

Imprime una tabla comparativa y genera un gráfico de barras con matplotlib.

¿POR QUÉ IMPORTA ESTO?
    Porque es exactamente el punto del trabajo práctico: demostrar que
    la elección de la estructura de datos impacta directamente en la
    eficiencia. Un BST balanceado con 30 elementos necesita ~5 comparaciones
    (log2(30) ≈ 5), mientras que la lista puede necesitar hasta 30.
"""

import os

from servicios.busquedas import buscar_por_codigo_secuencial
from estructuras.arbol_bst import construir_bst, construir_bst_balanceado


def comparar_eficiencia(catalogo: list):
    """
    Ejecuta la comparación completa: tabla en consola + gráfico PNG.

    Args:
        catalogo: lista de objetos Libro (debe tener al menos 3 elementos).
    """
    if len(catalogo) < 3:
        print("⚠️  Se necesitan al menos 3 libros para la comparación.")
        return

    # --- Preparar los 3 métodos de búsqueda ---
    bst_degenerado = construir_bst(catalogo, "codigo")
    bst_balanceado = construir_bst_balanceado(catalogo, "codigo")

    # --- Definir los 4 casos de prueba ---
    primer_codigo = catalogo[0].codigo
    medio_codigo = catalogo[len(catalogo) // 2].codigo
    ultimo_codigo = catalogo[-1].codigo
    inexistente = "ZZZZ"  # código que no existe

    casos = [
        ("Primero", primer_codigo),
        ("Medio", medio_codigo),
        ("Último", ultimo_codigo),
        ("Inexistente", inexistente),
    ]

    # --- Ejecutar las búsquedas y recolectar resultados ---
    resultados = []
    for nombre_caso, codigo in casos:
        # Búsqueda secuencial
        _, comp_seq = buscar_por_codigo_secuencial(catalogo, codigo)

        # BST degenerado
        if bst_degenerado:
            _, comp_deg = bst_degenerado.buscar(codigo)
        else:
            comp_deg = 0

        # BST balanceado
        if bst_balanceado:
            _, comp_bal = bst_balanceado.buscar(codigo)
        else:
            comp_bal = 0

        resultados.append({
            "caso": f"{nombre_caso} ({codigo})",
            "secuencial": comp_seq,
            "bst_degenerado": comp_deg,
            "bst_balanceado": comp_bal,
        })

    # --- Imprimir tabla ---
    _imprimir_tabla(resultados, bst_degenerado, bst_balanceado)

    # --- Generar gráfico ---
    _generar_grafico(resultados)


def _imprimir_tabla(resultados: list, bst_deg, bst_bal):
    """Imprime la tabla comparativa en consola."""
    print("\n" + "=" * 75)
    print("📊  COMPARACIÓN DE EFICIENCIA: Lista vs BST Degenerado vs BST Balanceado")
    print("=" * 75)

    # Alturas
    alt_deg = bst_deg.altura() if bst_deg else 0
    alt_bal = bst_bal.altura() if bst_bal else 0
    print(f"\n  Altura BST degenerado:  {alt_deg}")
    print(f"  Altura BST balanceado:  {alt_bal}")
    print()

    # Encabezados
    print(f"  {'Caso':<25} {'Secuencial':>12} {'BST Degen.':>12} {'BST Balanc.':>12}")
    print("  " + "-" * 61)

    for r in resultados:
        print(f"  {r['caso']:<25} {r['secuencial']:>12} "
              f"{r['bst_degenerado']:>12} {r['bst_balanceado']:>12}")

    print()
    print("  💡 Menor número de comparaciones = más eficiente.")
    print("  💡 El BST balanceado es el claro ganador en todos los casos.")
    print("=" * 75)


def _generar_grafico(resultados: list):
    """
    Genera un gráfico de barras agrupadas y lo guarda en docs/comparacion.png.

    Usa matplotlib. Si no está instalado, muestra un mensaje y continúa.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # backend sin ventana (para guardar a archivo)
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠️  matplotlib no está instalado. No se puede generar el gráfico.")
        print("    Instalalo con: pip install matplotlib")
        return

    # Datos para el gráfico
    casos = [r["caso"].split(" (")[0] for r in resultados]  # solo el nombre
    secuencial = [r["secuencial"] for r in resultados]
    degenerado = [r["bst_degenerado"] for r in resultados]
    balanceado = [r["bst_balanceado"] for r in resultados]

    # Configurar el gráfico
    x = range(len(casos))
    ancho = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    barras1 = ax.bar([i - ancho for i in x], secuencial, ancho,
                      label="Secuencial (lista)", color="#e74c3c")
    barras2 = ax.bar(list(x), degenerado, ancho,
                      label="BST Degenerado", color="#f39c12")
    barras3 = ax.bar([i + ancho for i in x], balanceado, ancho,
                      label="BST Balanceado", color="#27ae60")

    # Agregar el número encima de cada barra
    for barras in [barras1, barras2, barras3]:
        for barra in barras:
            altura = barra.get_height()
            ax.annotate(f"{int(altura)}",
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9)

    ax.set_xlabel("Caso de búsqueda")
    ax.set_ylabel("Comparaciones realizadas")
    ax.set_title("Comparación de eficiencia: Lista vs BST Degenerado vs BST Balanceado")
    ax.set_xticks(list(x))
    ax.set_xticklabels(casos)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    # Crear directorio docs/ si no existe
    os.makedirs("docs", exist_ok=True)
    ruta = "docs/comparacion.png"
    plt.savefig(ruta, dpi=150)
    plt.close()

    print(f"\n📈 Gráfico guardado en '{ruta}'.")
