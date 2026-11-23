import random
import re
import sys
import time
import streamlit as st

#sys.setrecursionlimit(10000)

st.set_page_config(
    page_title="Mini Proyecto",
    page_icon="⚙️",
    layout="wide",
)

st.markdown("""
    <style>
        /* Oculta el botón Deploy y el menú superior */
        header[data-testid="stHeader"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# MERGESORT
# LO RECUPERAMOS DE https://www.geeksforgeeks.org/python/python-program-for-merge-sort/
def merge(arr, l, m, r,pasos=None): #esto es para cuando n<=10
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[l + i]
    for j in range(n2):
        R[j] = arr[m + 1 + j]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
    if pasos is not None:
        pasos.append(f"Mezcla [{l}..{r}] → {arr.copy()}")

def mergeSort(arr, l, r,pasos=None):
    if l < r:
        m = l + (r - l) // 2
        mergeSort(arr, l, m,pasos)
        mergeSort(arr, m + 1, r,pasos)
        merge(arr, l, m, r,pasos)

# QUICKSORT 
# LO RECUPERAMOS DE https://www.geeksforgeeks.org/dsa/python-program-for-quicksort/ 
def partition(arr, low, high,pasos=None):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    if pasos is not None:
        pasos.append(f"Pivote={pivot} en índice {i + 1} (rango [{low}..{high}]) → {arr.copy()}")
    return i + 1

def quick_sort(arr, low, high,pasos=None):
    if low < high:
        p = partition(arr, low, high, pasos)
        quick_sort(arr, low, p - 1, pasos)
        quick_sort(arr, p + 1, high, pasos)

# HEAPSORT
# LO RECUPERAMOS DE https://www.geeksforgeeks.org/dsa/python-program-for-heap-sort/ 
def heapify(arr, n, i):
    largest = i    
    l = 2 * i + 1    
    r = 2 * i + 2  

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapSort(arr, pasos=None):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    if pasos is not None:
        pasos.append(f"Max-Heap inicial → {arr.copy()}")

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
        if pasos is not None:
            pasos.append(f"Extrae máximo {arr[i]} → {arr.copy()}")

#esto es para que se pueda ver directamente en formato cientifico :D
def formato_cientifico(valor, decimales=4):
    base, exp = f"{valor:.{decimales}e}".split("e")
    superindices = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    exp_limpio = str(int(exp)).translate(superindices)
    return f"{base}×10{exp_limpio}"

# --- INTERFAZ ---
st.title("Ordenador de Arreglos")

if "uploader_id" not in st.session_state:
    st.session_state["uploader_id"] = 0

origen = st.radio(
    "¿Cómo deseas ingresar los datos?",
    ["Escribir manualmente", "Subir archivo (.txt / .csv)", "Generar aleatorios"],
    horizontal=True,
    key="origen_datos"
)

arr = []

if origen == "Escribir manualmente":
    entrada = st.text_input(
        "Ingrese los números separados por comas:",
        placeholder="Ej: 12, 11, 13, 5, 6",
        key="entrada_manual"
        
    )
    if entrada.strip():
        tokens = [t.strip() for t in entrada.split(",") if t.strip() != ""]
        try:
            arr = [int(t) for t in tokens]
        except ValueError:
            st.error("Entrada inválida: ingresa únicamente números enteros separados por comas.")
            arr = []

elif origen == "Subir archivo (.txt / .csv)":
    archivo = st.file_uploader(
        "Sube un archivo con números (separados por comas, espacios o saltos de línea):",
        type=["txt", "csv"],
        key=f"cargardatos_{st.session_state['uploader_id']}"
    )
    if archivo is not None:
        contenido = archivo.read().decode("utf-8")
        arr = [int(n) for n in re.findall(r"-?\d+", contenido)]
        st.info(f"Se cargaron **{len(arr)}** números desde `{archivo.name}`.")

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        cantidad = st.number_input("Cantidad de números:", min_value=0, max_value=100000, value=0, step=1)
        key="cant_aleatoria"
    with col2:
        min_val = st.number_input("Valor mínimo:", value=1, step=1)
    with col3:
        max_val = st.number_input("Valor máximo:", value=100, step=1)

    if min_val > max_val:
        st.error("El valor mínimo no puede ser mayor que el valor máximo.")
    else:
        params_actuales = (int(cantidad), int(min_val), int(max_val))
        if (
            st.button("Generar nueva lista")
            or "lista_aleatoria" not in st.session_state
            or st.session_state.get("params_aleatorios") != params_actuales
        ):
            st.session_state.lista_aleatoria = [
                random.randint(int(min_val), int(max_val)) for _ in range(int(cantidad))
            ]
            st.session_state.params_aleatorios = params_actuales

        arr = st.session_state.lista_aleatoria
        with st.expander("Ver lista generada sin ordenar", expanded=True):
            st.code(str(arr), language="python")

nombres_metodos = {
    "MergeSort": "Merge Sort",
    "QuickSort": "Quick Sort",
    "HeapSort": "Heap Sort"
}

metodos_seleccionados = st.multiselect(
    "Elija uno, varios o los tres métodos de ordenamiento:",
    options=["MergeSort", "QuickSort", "HeapSort"],
    default=["MergeSort", "QuickSort", "HeapSort"],
    format_func=lambda x: nombres_metodos[x]
)

if st.button("Ordenar", type="primary"):
    if not arr:
        st.warning("Por favor, ingresa números, sube un archivo o genera una lista válida.")
    elif len(arr) < 2:
        st.warning("Ingresa o carga al menos 2 números válidos para ordenar.")
    elif not metodos_seleccionados:
        st.warning("Selecciona al menos un algoritmo de ordenamiento.")
    else:
        #resultado_final = []
        resultados_por_metodo = {}
        cols_tiempos = st.columns(len(metodos_seleccionados))

        for i, metodo in enumerate(metodos_seleccionados):
            copia_arr = arr.copy()
            inicio = time.perf_counter()

            try:
                match metodo:
                    case "MergeSort":
                        mergeSort(copia_arr, 0, len(copia_arr) - 1)
                    case "QuickSort":
                        quick_sort(copia_arr, 0, len(copia_arr) - 1)
                    case "HeapSort":
                        heapSort(copia_arr)

                tiempo_s = time.perf_counter() - inicio
                resultados_por_metodo[metodo] = copia_arr
                cols_tiempos[i].metric(
                    label=f"Método {nombres_metodos[metodo]}",
                    value=f"{formato_cientifico(tiempo_s)} s"
                )

            except RecursionError:
                cols_tiempos[i].metric(
                    label=f"Método {nombres_metodos[metodo]}",
                    value="RecursionError"
                )
                st.error(
                    f"**{nombres_metodos[metodo]}** superó el límite máximo de recursión de Python con "
                    f"$n={len(arr)}$. Causa: elegir el último elemento como pivote (`arr[high]`) genera "
                    f"particiones totalmente desequilibradas de profundidad $O(n)$."
                )

        listas_ordenadas = list(resultados_por_metodo.values())
        todos_iguales = all(res == listas_ordenadas[0] for res in listas_ordenadas)
        orden_correcto = listas_ordenadas[0] == sorted(arr)
        
        if todos_iguales and orden_correcto:
            st.success(f"Validación exitosa: los {len(listas_ordenadas)} algoritmos produjeron exactamente el mismo arreglo ordenado ({len(listas_ordenadas[0])} elementos).")
        else:
            st.error("Error de consistencia: los algoritmos produjeron resultados distintos.")
        st.write("Resultado:")
        st.code(str(listas_ordenadas[0]), language="python")


        #st.success(f"Arreglo ordenado ({len(resultado_final)} elementos):")
        #st.code(str(resultado_final), language="python")
        if len(arr) <= 10:
                        with st.expander("Ver prueba funcional paso a paso", expanded=False):
                            st.write(f"**Datos iniciales:** `{arr}`")

                            for metodo in metodos_seleccionados:
                                if metodo not in resultados_por_metodo:
                                    continue
                                pasos = []
                                copia_traza = arr.copy()

                                match metodo:
                                    case "MergeSort":
                                        mergeSort(copia_traza, 0, len(copia_traza) - 1, pasos)
                                    case "QuickSort":
                                        quick_sort(copia_traza, 0, len(copia_traza) - 1, pasos)
                                    case "HeapSort":
                                        heapSort(copia_traza, pasos)
                                st.text("")        
                                st.markdown(f"**>>>{nombres_metodos[metodo]}:**")
                                for num_paso, estado in enumerate(pasos, 1):
                                    st.text(f"    >Paso {num_paso}: {estado}")
                                    

        #st.write(f"**Resultado final:** `{listas_ordenadas[0]}`")
       

        st.download_button(
            label="Descargar lista ordenada (.txt)",
            data=", ".join(map(str, listas_ordenadas[0])),
            file_name="arreglo_ordenado.txt",
            mime="text/plain"
        )
st.divider()
if st.button("Finalizar y limpiar datos"):
    nuevo_id = st.session_state.get("uploader_id", 0) + 1
    st.session_state.clear()
    st.session_state["uploader_id"] = nuevo_id
    st.session_state["entrada_manual"] = ""
    st.session_state["cant_aleatoria"] = 0
    st.session_state["origen_datos"] = "Escribir manualmente"
    st.session_state["sesion_finalizada"] = True
    st.rerun()

if st.session_state.pop("sesion_finalizada", False):
    st.info("Sesión finalizada y datos reiniciados. Puedes cerrar esta pestaña o comenzar una nueva prueba.")


