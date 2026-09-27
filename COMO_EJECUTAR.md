# 🚀 Cómo ejecutar el programa

## Requisitos previos

1. **Python 3.10 o superior** instalado
   - Verificá con: `python --version`
2. **matplotlib** (solo para el gráfico de comparación)

## Instalación paso a paso

```bash
# 1. Cloná el repositorio
git clone https://github.com/FrancoNavarro20/TPN2-Estructura-de-datos.git

# 2. Entrá a la carpeta del proyecto
cd TPN2-Estructura-de-datos/biblioteca-tp

# 3. Instalá matplotlib (única dependencia externa)
pip install matplotlib
```

## Ejecutar el programa

```bash
# Desde la carpeta biblioteca-tp/
python main.py
```

> **Nota para Windows:** si los emojis no se ven bien en la terminal,
> ejecutá con esta variante:
> ```bash
> set PYTHONIOENCODING=utf-8
> python main.py
> ```
> O en PowerShell:
> ```powershell
> $env:PYTHONIOENCODING="utf-8"; python main.py
> ```

## ¿Qué vas a ver?

Al ejecutar `python main.py` aparece el menú principal:

```
╔══════════════════════════════════════════════════════╗
║         📚  SISTEMA DE BIBLIOTECA  📚               ║
║         Catálogo de Libros — TP Estructuras          ║
╚══════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────┐
│                   MENÚ PRINCIPAL                     │
├──────────────────────────────────────────────────────┤
│  1. Buscar por código (lista — secuencial)           │
│  2. Buscar por código (árbol BST)                    │
│  3. Buscar por título                                │
│  4. Explorar por categorías                          │
│  5. Listar catálogo ordenado (inorden BST)           │
│  6. Insertar libro                                   │
│  7. Eliminar libro                                   │
│  8. Deshacer última operación                        │
│  9. Ver historial de búsquedas                       │
│ 10. Estadísticas                                     │
│ 11. Comparar eficiencia (tabla + gráfico)            │
│ 12. Guardar catálogo                                 │
│  0. Salir (guarda antes de cerrar)                   │
└──────────────────────────────────────────────────────┘
```

Ingresá el número de la opción y presioná **Enter**.

## Pruebas rápidas sugeridas

Probá estas opciones en orden para verificar que todo funciona:

| Paso | Opción | Qué hacer                              | Qué esperar                                  |
|------|--------|----------------------------------------|----------------------------------------------|
| 1    | `1`    | Buscar código `L015`                   | Encuentra "Rayuela" en ~15 comparaciones     |
| 2    | `2`    | Buscar código `L015`                   | Encuentra "Rayuela" en ~5 comparaciones (BST)|
| 3    | `3`    | Buscar título `cien años`              | Encuentra "Cien años de soledad"             |
| 4    | `4`    | Explorar categorías, escribir `Poesía` | Muestra los 4 libros de poesía               |
| 5    | `5`    | Listar catálogo ordenado               | 30 libros de L001 a L030 en orden            |
| 6    | `10`   | Ver estadísticas                       | Resumen completo del catálogo                |
| 7    | `11`   | Comparar eficiencia                    | Tabla + gráfico en `docs/comparacion.png`    |
| 8    | `0`    | Salir                                  | Guarda y cierra                              |

## Estructura del proyecto

```
biblioteca-tp/
├── main.py                  ← EJECUTAR ESTE ARCHIVO
├── modelos/libro.py         ← Clase Libro
├── estructuras/
│   ├── arbol_categorias.py  ← Árbol general n-ario
│   ├── arbol_bst.py         ← Árbol binario de búsqueda
│   ├── pila.py              ← Pila LIFO (deshacer)
│   └── cola.py              ← Cola FIFO (historial)
├── servicios/
│   ├── busquedas.py         ← Búsquedas secuenciales
│   ├── persistencia.py      ← Guardar/cargar JSON
│   ├── estadisticas.py      ← Estadísticas
│   └── comparador.py        ← Comparación + gráfico
├── datos/catalogo.json      ← 30 libros de prueba
├── ui/menu.py               ← Menú de consola
└── docs/EXPLICACION.md      ← Explicación para defensa
```

## Solución de problemas

| Problema                          | Solución                                           |
|-----------------------------------|----------------------------------------------------|
| `ModuleNotFoundError`             | Asegurate de estar EN la carpeta `biblioteca-tp/`  |
| Emojis se ven como `?` o `□`     | Usá `$env:PYTHONIOENCODING="utf-8"` antes          |
| `matplotlib not installed`        | Ejecutá `pip install matplotlib`                    |
| El JSON no se encuentra           | Verificá que existe `datos/catalogo.json`           |
