# 📖 EXPLICACIÓN DETALLADA DEL PROYECTO

Este documento explica el proyecto **completo**, archivo por archivo,
para que cualquier estudiante que no haya escrito el código pueda
entenderlo y defenderlo en un examen oral.

---

## 1. Mapa del proyecto

```
biblioteca-tp/
│
├── modelos/              ← Las clases del DOMINIO (qué cosas maneja el sistema)
│   └── libro.py          ← Clase Libro: representa un libro físico
│
├── estructuras/          ← Las ESTRUCTURAS DE DATOS implementadas a mano
│   ├── arbol_categorias.py  ← Árbol general (n hijos) para clasificar libros
│   ├── arbol_bst.py         ← Árbol binario de búsqueda para buscar rápido
│   ├── pila.py              ← Pila (LIFO) para deshacer operaciones
│   └── cola.py              ← Cola (FIFO) para historial de búsquedas
│
├── servicios/            ← La LÓGICA DE NEGOCIO (qué hace el sistema)
│   ├── busquedas.py         ← Búsquedas secuenciales con conteo
│   ├── persistencia.py      ← Guardar y cargar el catálogo en JSON
│   ├── estadisticas.py      ← Cálculos estadísticos
│   └── comparador.py        ← Compara eficiencia lista vs BST
│
├── datos/                ← Los DATOS de prueba
│   └── catalogo.json        ← 30 libros reales en formato JSON
│
├── ui/                   ← La INTERFAZ de usuario (consola)
│   └── menu.py              ← Menú con 13 opciones
│
├── docs/                 ← DOCUMENTACIÓN
│   ├── EXPLICACION.md       ← Este archivo
│   └── comparacion.png      ← Gráfico generado por el comparador
│
├── main.py               ← Punto de entrada: el que ejecutás con python main.py
├── README.md             ← Presentación del proyecto
├── USO-DE-IA.md          ← Declaración de uso de IA
└── .gitignore            ← Archivos que Git debe ignorar
```

**¿Por qué esta organización?**

Separamos el código en capas:
1. **Modelos** → define QUÉ es un libro (datos)
2. **Estructuras** → define CÓMO organizamos los libros (estructuras de datos)
3. **Servicios** → define QUÉ OPERACIONES hacemos con los libros (lógica)
4. **UI** → define CÓMO INTERACTÚA el usuario (presentación)

Esto se llama **separación de responsabilidades** y es una buena práctica
de diseño de software.

---

## 2. Archivo por archivo

### `modelos/libro.py`

**Clase `Libro`**

| Atributo     | Tipo  | Descripción                      |
|-------------|-------|----------------------------------|
| `_codigo`    | str   | Identificador único (ej. "L001") |
| `_titulo`    | str   | Título del libro                 |
| `_autor`     | str   | Autor principal                  |
| `_categoria` | str   | Categoría hoja del árbol         |
| `_anio`      | int   | Año de publicación               |
| `_cantidad`  | int   | Ejemplares disponibles (≥ 0)     |

Los atributos son **privados** (con `_`) y se acceden mediante `@property`.
El setter de `cantidad` valida que no sea negativa.

**Métodos:**
- `disponible()` → True si hay al menos 1 ejemplar
- `a_diccionario()` → convierte a dict para guardar en JSON
- `__str__()` → formato legible para mostrar en consola

---

### `estructuras/arbol_categorias.py`

**Clase `NodoCategoria`** — Un nodo del árbol general (n hijos).

**Métodos:**
- `agregar_subcategoria(nombre)` → agrega un hijo y devuelve el nodo nuevo
- `es_hoja()` → True si no tiene subcategorías
- `mostrar(nivel)` → imprime el árbol con indentación (recorrido preorden)
- `buscar_categoria(nombre)` → busca recursivamente en todo el subárbol
- `contar_elementos()` → cuenta libros propios + de todas las subcategorías
- `altura()` → altura del subárbol
- `listar_todos()` → lista plana de todos los libros del subárbol

**Funciones auxiliares:**
- `construir_arbol_categorias()` → arma la jerarquía completa
- `asignar_libros_a_categorias(raiz, catalogo)` → distribuye libros en las hojas

---

### `estructuras/arbol_bst.py`

**Clase `NodoBST`** — Un nodo del árbol binario de búsqueda.

**Métodos:**
- `insertar(clave, elemento)` → inserción recursiva respetando la regla de orden
- `buscar(clave, comparaciones)` → búsqueda con conteo de comparaciones
- `altura()` → altura del subárbol
- `contar_nodos()` → cantidad de nodos

**Funciones de recorrido:**
- `inorden(nodo)` → izquierda → raíz → derecha (devuelve ordenado)
- `preorden(nodo)` → raíz → izquierda → derecha
- `postorden(nodo)` → izquierda → derecha → raíz

**Funciones de construcción:**
- `construir_bst(catalogo, clave)` → inserta en orden (puede degenerar)
- `construir_bst_balanceado(catalogo, clave)` → inserta por el medio (balanceado)

---

### `estructuras/pila.py`

**Clase `Pila`** — Pila LIFO con lista enlazada.

- `apilar(dato)` → agrega al tope
- `desapilar()` → saca del tope
- `ver_tope()` → mira sin sacar
- `esta_vacia()` → ¿está vacía?
- `tamanio()` → cantidad de elementos

---

### `estructuras/cola.py`

**Clase `Cola`** — Cola FIFO con lista enlazada y tamaño máximo.

- `encolar(dato)` → agrega al final (descarta el más viejo si se pasa del máx)
- `desencolar()` → saca del frente
- `esta_vacia()` → ¿está vacía?
- `listar()` → devuelve todos sin sacarlos

---

### `servicios/busquedas.py`

Tres funciones de búsqueda secuencial, todas con conteo de comparaciones:

- `buscar_por_codigo_secuencial(catalogo, codigo)` → búsqueda exacta
- `buscar_por_titulo_secuencial(catalogo, titulo)` → búsqueda parcial, case-insensitive
- `buscar_por_autor(catalogo, autor)` → devuelve todos los del autor

---

### `servicios/persistencia.py`

- `guardar_catalogo(catalogo, archivo)` → convierte a dict y guarda como JSON
- `cargar_catalogo(archivo)` → lee JSON y crea objetos Libro

Usa `encoding="utf-8"` y `ensure_ascii=False` para los acentos.

---

### `servicios/estadisticas.py`

Función `mostrar_estadisticas()` que calcula:
- Total de títulos y ejemplares
- Libros sin stock
- Alturas de los árboles
- Libros por categoría
- Autor con más obras
- Año más antiguo y más reciente

---

### `servicios/comparador.py`

Función `comparar_eficiencia()` que:
1. Busca 4 códigos (primero, medio, último, inexistente) con 3 métodos
2. Imprime una tabla comparativa
3. Genera un gráfico de barras con matplotlib

---

### `ui/menu.py`

**Clase `Menu`** — Controlador del menú de consola con 13 opciones.
Mantiene el estado: catálogo, árboles, pila de deshacer, cola de historial.

---

### `main.py`

Punto de entrada: carga JSON → crea Menu → ejecuta.

---

## 3. ¿Por qué esta estructura y no otra?

| Funcionalidad                    | Estructura usada            | ¿Por qué esa y no otra?                                                                                    |
|----------------------------------|-----------------------------|-------------------------------------------------------------------------------------------------------------|
| Clasificación jerárquica         | Árbol general (n-ario)      | Las categorías tienen relación padre-hijo natural. Una lista plana perdería la jerarquía.                   |
| Búsqueda rápida por código       | BST balanceado              | Busca en O(log n) vs O(n) de la lista. Con 30 libros: ~5 comparaciones vs hasta 30.                        |
| Búsqueda por título/autor        | Lista (secuencial)          | No podemos usar BST porque la clave es el código. Para título necesitamos recorrer todo.                    |
| Deshacer operaciones             | Pila (LIFO)                 | La última operación es la primera que se deshace. Es exactamente el comportamiento LIFO.                    |
| Historial de búsquedas           | Cola (FIFO)                 | Queremos mantener orden cronológico y descartar las más viejas. Es exactamente FIFO.                        |
| Almacenamiento del catálogo      | Lista de Python             | Necesitamos acceso por índice, recorrido secuencial, y es el contenedor más simple para los 30 libros.      |
| Persistencia                     | Archivo JSON                | Formato legible, nativo en Python, no requiere base de datos.                                               |

---

## 4. Explicaciones con dibujos ASCII

### 4.1 El árbol de categorías (cómo se recorre)

```
                         Biblioteca
                        /          \
                 Literatura        Técnicos
                /    |    \       /    |    \
          Ficción  Poesía Cuento Prog. Matem. BD
          /    \
    Ci.Fi  Nov.Hist.
```

**Recorrido PREORDEN** (primero el nodo, después los hijos):
```
Biblioteca → Literatura → Ficción → Ci.Fi → Nov.Hist. → Poesía → Cuento
→ Técnicos → Prog. → Matem. → BD
```

Es el que usamos para MOSTRAR el árbol con indentación, porque primero
imprime la categoría padre y después baja a las sub.

**Búsqueda en profundidad (DFS):**
Para buscar "Poesía", el algoritmo hace:
1. ¿Es "Biblioteca"? No → baja al primer hijo
2. ¿Es "Literatura"? No → baja al primer hijo
3. ¿Es "Ficción"? No → baja al primer hijo
4. ¿Es "Ciencia ficción"? No → no tiene hijos, vuelve
5. ¿Es "Novela histórica"? No → no tiene hijos, vuelve a Ficción, vuelve a Literatura
6. ¿Es "Poesía"? ¡SÍ! → devuelve este nodo

---

### 4.2 El árbol binario de búsqueda (la regla de orden)

```
                    L015
                   /    \
               L007      L023
              /    \     /    \
          L003    L010 L019   L027
         /    \     \     \      \
       L001  L005  L012  L021   L029
         \     \     \      \      \
        L002  L006  L014   L022   L030
                      \      \
                     L016   L024
                       \      \
                      L017   L025
                        \      \
                       L018   L026
                               \
                              L028
```

**Regla:** todo lo de la IZQUIERDA es MENOR, todo lo de la DERECHA es MAYOR.

Para buscar **L010**:
```
L015 → L010 < L015 → voy a la IZQUIERDA
L007 → L010 > L007 → voy a la DERECHA
L010 → ¡ENCONTRADO! (3 comparaciones)
```

Búsqueda secuencial en la lista: L001, L002, ..., L010 → 10 comparaciones.

---

### 4.3 El problema del árbol degenerado

Si insertamos L001, L002, L003, ... en orden:

```
BST DEGENERADO:              BST BALANCEADO:
                             
L001                              L015
  \                              /    \
  L002                       L007      L023
    \                       /    \    /    \
    L003                 L003   L010 L019  L027
      \                  ...    ...  ...   ...
      L004
        \
        ...              Altura ≈ 5 (log2 30)
          \
          L030

Altura = 29 (igual que una lista)
```

**¿Por qué pasa?**
Porque cada clave nueva es MAYOR que la anterior, así que siempre va
a la derecha. El árbol se convierte en una cadena lineal.

**¿Cómo lo resolvemos?**
Con `construir_bst_balanceado()`: ordenamos, tomamos el del MEDIO
como raíz, y recursivamente el medio de cada mitad.

---

### 4.4 Los recorridos inorden, preorden y postorden

Dado este BST:
```
        L015
       /    \
    L007    L023
   /    \
 L003   L010
```

| Recorrido  | Orden de visita                   | Resultado                           |
|-----------|-----------------------------------|-------------------------------------|
| INORDEN   | izq → raíz → der                  | L003, L007, L010, L015, L023        |
| PREORDEN  | raíz → izq → der                  | L015, L007, L003, L010, L023        |
| POSTORDEN | izq → der → raíz                  | L003, L010, L007, L023, L015        |

**¿Para qué sirve cada uno?**
- **INORDEN** → devuelve los elementos **ordenados** (lo usamos para listar)
- **PREORDEN** → visita la raíz primero (útil para copiar la estructura)
- **POSTORDEN** → visita la raíz al final (útil para eliminar el árbol)

---

## 5. Recorrido de una operación de punta a punta

### "Buscar por código con BST" (opción 2 del menú)

Paso a paso, desde que el usuario elige la opción hasta que ve el resultado:

```
1. El usuario escribe "2" y presiona Enter
   → archivo: ui/menu.py, método: Menu.ejecutar()
   → el if reconoce opcion == "2" y llama a self._buscar_codigo_bst()

2. Se le pide el código al usuario: "Ingresá el código (ej. L015)"
   → archivo: ui/menu.py, método: Menu._buscar_codigo_bst()
   → el usuario escribe "L015"

3. Se busca en el BST balanceado
   → archivo: ui/menu.py llama a self.bst_balanceado.buscar("L015")
   → archivo: estructuras/arbol_bst.py, método: NodoBST.buscar()

4. Dentro del BST, se recorre recursivamente:
   → "L015" == "L015"? SÍ → devuelve (libro, 1 comparación)

5. De vuelta en el menú, se registra la búsqueda en el historial
   → archivo: ui/menu.py → self.historial_busquedas.encolar("Código(BST): L015")
   → archivo: estructuras/cola.py, método: Cola.encolar()

6. Se muestra el resultado al usuario:
   "✅ Encontrado en 1 comparaciones (BST):
    [L015] Rayuela — Julio Cortázar (1963) | Ej: 3"
```

### Diagrama del flujo:

```
[Usuario: "2"]
       ↓
[ui/menu.py: ejecutar()]
       ↓
[ui/menu.py: _buscar_codigo_bst()]
       ↓
[Usuario: "L015"]
       ↓
[estructuras/arbol_bst.py: NodoBST.buscar("L015")]
       ↓
[Recorrido recursivo del BST: L015 encontrado]
       ↓
[estructuras/cola.py: Cola.encolar() — registra en historial]
       ↓
[ui/menu.py: imprime resultado al usuario]
```

---

## 6. Preguntas que te pueden hacer en la defensa

### P1: ¿Qué es un árbol binario de búsqueda y cuál es su regla?
**R:** Es un árbol donde cada nodo tiene como máximo 2 hijos. La regla
de orden es: todo lo que está a la izquierda tiene clave menor, y todo
lo de la derecha tiene clave mayor. Esto permite buscar en O(log n)
porque en cada paso descartamos la mitad de los datos.

### P2: ¿Qué pasa si insertás los elementos en orden en un BST?
**R:** Se genera un árbol degenerado: todos los nodos van hacia un solo
lado (como una lista enlazada). La altura pasa a ser n-1 y la búsqueda
vuelve a ser O(n), perdiendo toda la ventaja del BST.

### P3: ¿Cómo resolviste el problema del árbol degenerado?
**R:** Con la función `construir_bst_balanceado()`. Primero ordena los
datos por la clave, después inserta el elemento del MEDIO como raíz,
y recursivamente el medio de cada mitad. Así el árbol queda parejo
con altura ~log2(n).

### P4: ¿Qué diferencia hay entre el árbol de categorías y el BST?
**R:** El árbol de categorías es un árbol GENERAL: cada nodo puede tener
cualquier cantidad de hijos y se usa para representar jerarquías. El BST
es un árbol BINARIO: cada nodo tiene exactamente 0, 1 o 2 hijos, y
tiene una regla de orden para buscar eficientemente.

### P5: ¿Por qué usaste una pila para deshacer y no una lista?
**R:** Porque "deshacer" siempre deshace la ÚLTIMA operación, que es
exactamente el comportamiento LIFO de una pila. Podríamos usar una
lista, pero la pila nos obliga a usar la semántica correcta (solo
apilar y desapilar), lo que hace el código más claro y menos propenso
a errores.

### P6: ¿Por qué la cola tiene tamaño máximo?
**R:** Porque solo queremos mostrar las últimas 5 búsquedas. Sin límite,
la cola crecería indefinidamente y guardaría miles de búsquedas viejas
que nadie va a consultar. Cuando se llega al máximo, automáticamente
descarta la más antigua.

### P7: ¿Qué recorrido del BST devuelve los elementos ordenados?
**R:** El recorrido INORDEN (izquierda → raíz → derecha). Es una
propiedad fundamental del BST: como todo lo menor está a la izquierda,
al visitar primero la izquierda, después el nodo, y después la derecha,
los elementos salen en orden ascendente.

### P8: ¿Por qué contás las comparaciones en las búsquedas?
**R:** Para demostrar empíricamente la diferencia de eficiencia. Con
30 libros, la búsqueda secuencial puede hacer hasta 30 comparaciones,
el BST degenerado también hasta 30, pero el BST balanceado no más
de 5 o 6 (~log2(30)). Esa es la razón de ser de las estructuras
de datos: elegir la correcta hace que el programa sea más rápido.

### P9: ¿Qué es el encapsulamiento y dónde lo usás?
**R:** Es ocultar los datos internos de una clase para controlar cómo
se acceden y modifican. En `Libro`, los atributos son privados (con `_`)
y se acceden mediante `@property`. El setter de `cantidad` valida que
no sea negativa. Así nadie puede poner un valor inválido por accidente.

### P10: ¿Por qué guardás en JSON y no en una base de datos?
**R:** Porque el trabajo pide Python puro sin librerías externas (salvo
matplotlib). JSON es un formato de texto plano que Python puede leer
y escribir con el módulo `json` incluido en la biblioteca estándar.
Es legible por humanos, fácil de depurar, y suficiente para 30 libros.
Una base de datos sería excesiva para este caso.

---

*Documento generado para el TP de Estructuras de Datos.*
*Revisado y aprobado por los integrantes del grupo.*
