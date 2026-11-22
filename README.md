# Canasta básica y salario mínimo en Panamá

¿Cuánto del salario mínimo se va en comida en la provincia de Panamá? Este repositorio compara el costo de la canasta básica de alimentos con el salario mínimo en tres momentos: **2019** (antes de la pandemia), **2022** (después) y **2026** (el año en curso). El público es el equipo SIC, con un nivel inicial de pandas.

El análisis no inventa cifras. Cada número sale de una fuente oficial (INEC, ACODECO, MEF o Gaceta Oficial). El inventario de archivos, las URLs y las reglas de limpieza están en [`references/plan_datos.md`](references/plan_datos.md).

## Qué se analiza

Cuatro bloques, siempre dentro de la provincia de Panamá (en las series viejas, los distritos de Panamá y San Miguelito):

1. **IPC y costo de la canasta.** Índice de precios del INEC y costo mensual de la canasta de ACODECO y del MEF.
2. **Salario mínimo.** Tasas de la Región 1 y de la Región 2 (comercio al por menor y trabajo doméstico) según los decretos vigentes en cada año.
3. **Poder adquisitivo.** Qué parte del salario de la Región 1 alcanza para pagar la canasta, y si la comida subió más que el salario.
4. **Supermercados.** Precio de los 59 productos por establecimiento (CSV de ACODECO en 2019 y 2022, y el PDF quincenal de septiembre de 2026).

Tres reglas que el análisis no puede saltarse:

- **ACODECO y MEF no se mezclan.** ACODECO es el costo de su canasta de 59 productos a precios de supermercado. El MEF es un costo calórico familiar (cantidades INCAP, precios del INEC). Van en paralelo.
- **El IPC de 2026 no se empalma con 2019 y 2022.** Hasta agosto de 2025 la serie de Panamá y San Miguelito usa base 2013 = 100. Desde septiembre de 2025 el INEC publica base 2024 = 100 y la geografía pasa a llamarse provincia de Panamá. No hay un factor oficial de enlace para esta geografía ni para el grupo de alimentos. En 2019 y 2022 se comparan niveles; en 2026 se reportan niveles de la base nueva y la variación interanual que ya publica el INEC. El costo de la canasta, en balboas, sí se puede comparar en los tres años.
- **La canasta solo se cruza con la Región 1.** La Región 2 aparece únicamente en el bloque del salario, para mostrar la brecha entre regiones. El equivalente mensual de una tasa horaria es hora × 208 (48 h × 52 / 12). El doméstico usa el mensual que trae el decreto. En 2019 no existe la categoría “supermercados de 5 o más sucursales”.

## Estructura

```text
canasta-basica-salario/
├── README.md
├── requirements.txt
├── references/
│   └── plan_datos.md          # fuentes, cifras de control y reglas de limpieza
├── data/
│   ├── raw/                   # archivos tal cual salen de la fuente; no se editan
│   │   ├── acodeco/           # CSV 2019 y 2022, histórico y PDF de septiembre 2026
│   │   ├── inec/              # cuadros del IPC
│   │   ├── mef/               # informes mensuales 2019, 2022 y 2026
│   │   └── mitradel/          # gacetas de los tres decretos de salario
│   ├── interim/               # limpiezas a medias, todavía no para el análisis
│   └── processed/             # tablas tidy: ipc, costo_canasta_mensual, salario_minimo, precios_supermercados
├── notebooks/                 # 00 limpieza; 01–04 un notebook por bloque
├── src/                       # lectura y limpieza; los notebooks no parsean crudos
└── outputs/
    └── figures/
```

Los CSV y PDF de `data/raw/` ya están descargados. `src/`, `notebooks/` y `data/processed/` están listos para el código de limpieza y los cuatro bloques.

## Configuración

Hace falta Python 3.12 o superior. En esta máquina el entorno del proyecto usa Python 3.14.

```bash
cd canasta-basica-salario
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

En Windows, el activate es `.venv\Scripts\activate`.

Para abrir los notebooks con este entorno:

```bash
python -m ipykernel install --user --name canasta-vs-salario --display-name "Canasta vs salario"
jupyter lab
```

En Jupyter o en Cursor, elige el kernel **Canasta vs salario**.

Dependencias: `pandas`, `openpyxl` y `xlrd` (Excel del INEC), `pdfplumber` (PDF de ACODECO y del MEF), `matplotlib`, `jupyter`, `requests` y `lxml`.

Las gacetas del salario están escaneadas. `pdfplumber` no extrae el texto. Hay que transcribir las tasas ya verificadas en `references/plan_datos.md` (o usar OCR con `tesseract -l spa`, que no forma parte de `requirements.txt`) y dejarlas en `src/`, sin recalcularlas desde un OCR sucio.

## Cómo trabajar

1. No editar nada dentro de `data/raw/`.
2. La lectura de cada fuente vive en `src/` (`io_inec.py`, `io_acodeco.py`, `io_mef.py`, `io_salarios.py`, más `limpieza.py`).
3. El notebook `00` llama a ese código, corre los controles de calidad y escribe `data/processed/`.
4. Los notebooks `01` a `04` solo leen `data/processed/` y guardan figuras en `outputs/figures/`.

Controles mínimos antes de graficar: 59 productos por mes en los CSV, precios faltantes en `NaN` (nunca en 0), series de costo con los meses que realmente trae cada fuente, y ningún gráfico de niveles del IPC que mezcle base 2013 = 100 con base 2024 = 100.

Los CSV de ACODECO vienen en **latin-1**, no en UTF-8. El separador cambia entre coma y punto y coma, y algunos meses traen filas de cabecera vacías, columnas de índice o un pie (`Costo Total`, `FUENTE:`). El detalle, archivo por archivo, está en la sección 3 de [`references/plan_datos.md`](references/plan_datos.md).

## Fuentes

| Bloque | Institución | Qué aporta |
|---|---|---|
| IPC | [INEC](https://www.inec.gob.pa/) | Índices de Panamá y San Miguelito (base 2013) y de la provincia de Panamá (base 2024) |
| Canasta en supermercados | [ACODECO](https://www.acodeco.gob.pa/) y [datos abiertos](https://www.datosabiertos.gob.pa/) | Costo total histórico y precios por establecimiento |
| Costo calórico | [MEF, canasta básica](https://www.mef.gob.pa/canasta-basica/) | Costo familiar en Panamá y San Miguelito |
| Salario mínimo | [Gaceta Oficial](https://www.gacetaoficial.gob.pa/) | Decreto Ejecutivo 75 de 2017, 74 de 2021 y 13 de 2025 |
