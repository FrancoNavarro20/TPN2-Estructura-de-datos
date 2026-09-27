# 📚 Biblioteca — TP Estructuras de Datos

## Descripción

Sistema de consola para gestionar un catálogo de libros de una biblioteca.
Desarrollado como Trabajo Práctico de la materia **Estructuras de Datos**
de la Tecnicatura Universitaria.

El programa implementa **desde cero** las siguientes estructuras de datos:
- Árbol General (n-ario) para la jerarquía de categorías
- Árbol Binario de Búsqueda (BST) para búsqueda eficiente por código
- Pila (LIFO) para deshacer operaciones
- Cola (FIFO) para historial de búsquedas

## Integrantes

| Nombre completo       | Legajo  |
| --------------------- | ------- |
| *(completar)*         | *(completar)* |
| *(completar)*         | *(completar)* |
| *(completar)*         | *(completar)* |

## Cómo ejecutar

```bash
# Desde la carpeta biblioteca-tp/
python main.py
```

**Requisitos:**
- Python 3.10 o superior
- matplotlib (solo para el gráfico de comparación)

```bash
pip install matplotlib
```

## Estructura del proyecto

```
biblioteca-tp/
├── modelos/
│   ├── __init__.py
│   └── libro.py                  # Clase Libro (dominio)
├── estructuras/
│   ├── __init__.py
│   ├── arbol_categorias.py       # Árbol general n-ario
│   ├── arbol_bst.py              # Árbol binario de búsqueda
│   ├── pila.py                   # Pila LIFO
│   └── cola.py                   # Cola FIFO
├── servicios/
│   ├── __init__.py
│   ├── busquedas.py              # Búsquedas secuenciales
│   ├── persistencia.py           # Guardar/cargar JSON
│   ├── estadisticas.py           # Estadísticas del catálogo
│   └── comparador.py             # Comparación de eficiencia
├── datos/
│   └── catalogo.json             # 30 libros de prueba
├── ui/
│   ├── __init__.py
│   └── menu.py                   # Menú de consola
├── docs/
│   ├── EXPLICACION.md            # Explicación detallada
│   └── comparacion.png           # Gráfico generado
├── main.py                       # Punto de entrada
├── README.md                     # Este archivo
├── USO-DE-IA.md                  # Declaración de uso de IA
└── .gitignore
```

## Funcionalidades y estructuras usadas

| Funcionalidad                     | Estructura de datos       |
| --------------------------------- | ------------------------- |
| Clasificación jerárquica          | Árbol general (n-ario)    |
| Búsqueda eficiente por código     | Árbol binario de búsqueda |
| Búsqueda secuencial               | Lista (recorrido lineal)  |
| Deshacer última operación         | Pila (LIFO)               |
| Historial de búsquedas recientes  | Cola (FIFO, máx. 5)       |
| Persistencia                      | Archivo JSON               |
| Comparación de eficiencia         | Lista + BST + matplotlib  |
