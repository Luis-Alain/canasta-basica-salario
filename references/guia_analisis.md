# Guía de análisis con los datos limpios

Esta guía es para los notebooks `01` a `04`.

Leer solo `data/processed/` y guardar las figuras en `outputs/figures/`.

El detalle de las fuentes y de la limpieza está en [`plan_datos.md`](plan_datos.md). El entorno y la pregunta del proyecto están en el [`README`](../README.md).

## Antes de graficar

Desde la raíz del repositorio, con el entorno activado:

```python
from pathlib import Path

import pandas as pd

PROCESSED = Path("data/processed")

ipc = pd.read_csv(PROCESSED / "ipc.csv", parse_dates=["fecha"])
costo = pd.read_csv(PROCESSED / "costo_canasta_mensual.csv", parse_dates=["fecha"])
salario = pd.read_csv(PROCESSED / "salario_minimo.csv", parse_dates=["fecha_inicio"])
precios = pd.read_csv(PROCESSED / "precios_supermercados.csv", parse_dates=["fecha"])
```

Si el notebook está en `notebooks/`, la ruta es `Path("..") / "data" / "processed"`.

Al leer el CSV, `region` llega como número (`1` o `2`), no como texto. `quincena` es `2` en septiembre de 2026 y vacío en los CSV.

Cuatro reglas recorren todos los bloques:

1. Filtren `fuente` antes de usar el costo. `acodeco_historico` y `mef_cbfa` describen canastas distintas y se grafican en paralelo.
2. Grafiquen los niveles del IPC dentro de una sola `base`. 2019 y 2022 son `2013=100`. Diciembre de 2025 y 2026 son `2024=100`.
3. El cruce canasta–salario usa la Región 1. La Región 2 queda en el bloque del salario.
4. Un precio vacío es `NaN`. No lo reemplacen por 0 ni lo sumen como si fuera un precio.

## Qué hay en cada tabla

### `ipc.csv` — 70 filas

Una fila por mes, grupo y base.

| Columna | Valores |
|---|---|
| `grupo` | `total` o `alimentos_y_bebidas_no_alcoholicas` |
| `base` | `2013=100` o `2024=100` |
| `geografia` | `panama_y_san_miguelito` en la base vieja; `provincia_de_panama` en la nueva |
| `indice` | Nivel del INEC. En 2026 conserva los decimales del Excel |
| `notas` | Solo octubre 2026 trae texto: la variación interanual oficial |

Cobertura: los 12 meses de 2019 y de 2022, diciembre de 2025, y enero–octubre de 2026.

La serie vieja la publica el INEC para los distritos de Panamá y San Miguelito. En el relato del proyecto esa área se trata como la provincia. La columna `geografia` conserva el nombre de la publicación, para no mezclarla con la serie de 2026.

### `costo_canasta_mensual.csv` — 63 filas

Una fila por mes y fuente. `n_productos` es 59 en todas.

| `fuente` | Meses | `geografia` |
|---|---|---|
| `acodeco_historico` | 2019 y 2022 completos; 2026 de enero a agosto | `provincia_de_panama` |
| `mef_cbfa` | 2019 completo; 2022 sin agosto; 2026 de enero a agosto | `panama_y_san_miguelito` |

Agosto de 2022 del MEF no está publicado. No lo interpolen. El `costo_total` ya incluye las cantidades de cada canasta: no lo reconstruyan sumando precios unitarios.

### `salario_minimo.csv` — 22 filas

Una fila por año de análisis, región y categoría. El salario no es mensual: dentro de un año de análisis la tasa es la misma.

| `anio_analisis` | Decreto | `fecha_inicio` |
|---|---|---|
| 2019 | `DE 75/2017` | 2018-01-01 |
| 2022 | `DE 74/2021` | 2022-01-16 |
| 2026 | `DE 13/2025` | 2026-01-16 |

`actividad` es `comercio_al_por_menor` o `trabajo_domestico`. `categoria` es `pequena`, `gran_empresa`, `supermercados_5_plus` o `domestico`.

En el comercio, `salario_mensual` ya es `salario_hora * 208`. No lo vuelvan a multiplicar. En el doméstico, `salario_hora` está vacío y `salario_mensual` es el monto del decreto (`es_oficial_mensual` es verdadero). En 2019 no existe la fila de supermercados de 5 o más sucursales.

### `precios_supermercados.csv` — 89,149 filas

Una fila por producto, establecimiento y fecha.

| Origen | `fuente` | Fechas |
|---|---|---|
| CSV | `acodeco_csv` | Marzo–diciembre 2019 y enero–junio 2022. No hay enero ni febrero de 2019 |
| PDF | `acodeco_pdf_sep2026` | 1 de septiembre de 2026, `quincena` 2 |

`producto_estandar` unifica los 59 productos de los tres años. `precio` vacío significa que ese local no reportó el producto. Hay 28,320 precios vacíos y ninguno en cero.

`zona` es `san_miguelito` cuando el nombre del local o el recuadro del PDF lo dice (4,484 filas). El resto es `sin_clasificar`. La tabla no trae una zona `capital`. El contraste disponible es San Miguelito frente al resto.

`cadena` sale del nombre (Super 99, Rey, Xtra, Machetazo, Riba Smith, El Fuerte, minisúper, abarrotería, frutería). Si el nombre no dice la cadena, `cadena` queda vacía.

## Notebook 01 — inflación, canasta y salario

Tres figuras, en este orden:

1. `outputs/figures/inflacion_interanual.png` — variación interanual del IPC, general y alimentos.
2. `outputs/figures/aumento_canasta_salario.png` — incremento porcentual 2019→2022→2026 de la canasta ACODECO y del salario de la Región 1.
3. `outputs/figures/canasta_vs_salario.png` — costo de la canasta en balboas frente a ese salario.

`ipc.csv` guarda los años del proyecto, no el año anterior de cada mes. Con estas filas no se puede armar la variación interanual mensual de 2019 ni la de 2022, porque faltan 2018 y 2021. Tampoco se puede restar el índice de 2026 al de 2019: son bases distintas, y los tres años no son consecutivos.

Usen las variaciones que el INEC ya publicó:

| Momento | Total | Alimentos |
|---|---|---|
| 2019, variación anual del Cuadro 5 (base 2013=100) | −0.3 % | +0.3 % |
| 2022, variación anual del Cuadro 5 (base 2013=100) | +2.6 % | +3.9 % |
| Octubre 2026 / octubre 2025, columna `notas` | +3.3 % | +2.6 % |

`src/consulta_ipc_canasta.py` escribe `inflacion_interanual.png` con esas tres parejas. No recalcula una interanual cruzando bases ni pide datos por consola.

Las dos primeras no están en el CSV: citen el Cuadro 5 y no las recalculen promediando los meses. La de octubre 2026 sí está en `notas` de las dos filas de ese mes. Esas tres parejas son las que pueden ir en la misma gráfica de inflación, porque ya vienen en porcentaje.

Los niveles del índice sí se pueden graficar, en dos paneles: uno con `base == "2013=100"` (2019 y 2022, los dos grupos) y otro con `base == "2024=100"` (diciembre 2025–octubre 2026).

La canasta y el salario sí se comparan en balboas entre los tres años. Para el incremento 2019→2022→2026 usen el mismo mes en los tres años. Junio está en ACODECO y en el MEF. Agosto de 2022 no existe en el MEF, así que un corte en agosto deja esa serie incompleta.

```python
r1 = salario.loc[
    (salario["region"] == 1)
    & (salario["actividad"] == "comercio_al_por_menor")
    & (salario["categoria"] == "gran_empresa"),
    ["anio_analisis", "salario_hora", "salario_mensual"],
]

junio = costo.loc[
    (costo["fuente"] == "acodeco_historico") & (costo["mes"] == 6),
    ["anio", "costo_total"],
]
```

Declaren en el notebook la categoría del cruce principal: **comercio al por menor, gran empresa, Región 1**. Las otras categorías van como sensibilidad, en el notebook 02 o en una tabla aparte, sin cambiar la figura principal.

El costo del MEF se reporta al lado, con su propia línea. No se promedia con ACODECO.

Comprobación, junio y gran empresa de la Región 1: la canasta ACODECO es 260.64, 285.92 y 303.45 balboas. El salario mensual es 565.76, 584.48 y 628.16. La comida representa cerca del 46 %, 49 % y 48 % de ese salario. Si el resultado se aleja de eso, el filtro de mes, fuente o categoría no es el de arriba.

## Notebook 02 — salario mínimo

Comparen Región 1 y Región 2 en las categorías que existen en los tres años: pequeña, gran empresa y doméstico. Supermercados de 5 o más sucursales solo entra en 2022 y 2026.

La brecha se puede mostrar como diferencia de la tasa horaria o del mensual. Para el doméstico usen solo `salario_mensual`.

Este notebook no cruza la Región 2 con la canasta.

## Notebook 03 — poder adquisitivo

La categoría principal es la misma del notebook 01. El costo puede ser el de ACODECO o el del MEF, cada uno por su lado.

```text
pct_salario_en_comida = costo_total / salario_mensual * 100
horas_para_pagar      = costo_total / salario_hora
var_canasta           = costo_total / costo_2019 - 1
var_salario           = salario_mensual / salario_2019 - 1
```

`horas_para_pagar` usa la tasa horaria. En el doméstico esa columna está vacía: ahí el porcentaje sale del mensual oficial y las horas no se calculan.

`costo_2019` y `salario_2019` son el mismo mes y la misma categoría. Una variación de junio de 2026 contra enero de 2019 mezcla estacionalidad con el cambio de fondo. Si muestran la serie mensual, cada mes se compara con el mismo mes de 2019.

2026 llega hasta agosto en el costo. Septiembre y octubre no tienen `costo_total` en esta tabla.

## Notebook 04 — supermercados

Agrupen por `producto_estandar`, no por `producto`: el nombre original cambia de ortografía entre archivos.

Para un precio medio por producto y mes:

```python
medio = (
    precios.dropna(subset=["precio"])
    .groupby(["anio", "mes", "producto_estandar"], as_index=False)["precio"]
    .mean()
)
```

`dropna` quita los locales que no reportaron. No rellenen ese hueco con 0: bajaría el promedio. Conviene contar cuántos establecimientos entran en cada promedio.

El PDF de septiembre 2026 es una quincena, no un mes comparable con el promedio de un CSV. Grafíquenlo como un corte aparte, o junto a un mes de 2019 y otro de 2022 dejando claro que la fecha no es la misma.

`control_precio` es verdadero cuando el nombre del producto traía un asterisco en la fuente. Sirve para marcar esos productos; no es un precio.

San Miguelito contra el resto:

```python
precios = precios.copy()
precios["zona_analisis"] = precios["zona"].where(
    precios["zona"].eq("san_miguelito"), "resto"
)
```

## Qué no rehacer

El notebook `00_importacion_y_limpieza.ipynb` ya escribió estas tablas y pasó los controles. Vuelvan a correrlo solo si cambian `src/` o si `data/processed/` no está. Los notebooks de análisis no importan `src/` ni leen `data/raw/`.
