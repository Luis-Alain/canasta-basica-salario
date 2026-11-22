# Plan de datos: ¿Cuánto del salario mínimo se va en comida?

**Proyecto:** `canasta-vs-salario-panama`  
**Alcance cerrado:** solo **provincia de Panamá**; años **2019** (prepandemia), **2022** (post) y **2026** (actualidad).  
**Público:** equipo SIC, nivel inicial de pandas.  
**Regla:** no inventar cifras ni enlaces. Todo lo que aparece aquí se descargó o se leyó de la fuente oficial el 22 de noviembre de 2026 (hora de Panamá, UTC-5).  
**No se editó** la hoja de Google Sheets del inventario.

Cuatro bloques de análisis:

1. IPC y costo de la canasta (INEC + histórico ACODECO + MEF, Panamá y San Miguelito).
2. Salario mínimo (Región 1 en 2019, 2022 y 2026; Región 1 vs Región 2 solo en este bloque).
3. Poder adquisitivo (cruce de canasta e inflación contra el salario de la Región 1).
4. Supermercados (CSV ACODECO 2019 y 2022 + PDF quincenal de septiembre 2026; opcional capital vs San Miguelito).

Las muestras inspeccionadas están en `sic-canasta/muestras/`.

---

## 1. Lista exacta de datasets

### Cómo usar esta lista

- **Esencial:** hay que bajarlo para hacer el bloque.  
- **Mínimo suficiente:** subconjunto que ya permite el contraste 2019 / 2022 / 2026.  
- **Recomendado (completo):** si hay tiempo, cubre todos los meses disponibles y deja series más limpias para el bloque 3.

### 1.1 Bloque 1 — IPC (INEC)

El INEC **no tiene un solo cuadro** con 2019, 2022 y 2026 en la misma base y la misma geografía. Hay que usar **dos familias de archivos** y tratarlas por separado.

#### A) Serie comparable 2019 vs 2022 (y hasta agosto 2025)

**Geografía:** distritos de **Panamá y San Miguelito**.  
**Base:** **2013 = 100**.  
**Ponderaciones:** Encuesta de Ingresos y Gastos de los Hogares 2007/08 (2,103 hogares).  
**Publicación:** *Índice de Precios al Consumidor (IPC) 2017-2025*, página  
https://www.inec.gob.pa/publicaciones/Default3.aspx?ID_PUBLICACION=1396&ID_CATEGORIA=4&ID_SUBCATEGORIA=82

| Archivo | Formato | Qué extraer | URL directa (verificada HTTP 200) |
|---|---|---|---|
| **Cuadro 5.** IPC en los distritos de Panamá y San Miguelito y su variación porcentual, según grupo, subgrupo, clase y subclase: **años 2017-24** | Excel (preferido), también CSV y PDF | Filas **TOTAL** y **ALIMENTOS Y BEBIDAS NO ALCOHÓLICAS**; columnas 2019 y 2022 (índice y variación). El Excel tiene más decimales; los PDF oficiales suelen publicar 1 decimal. | [Excel](https://www.inec.gob.pa/archivos/P053342420260511104741Cuadro%205_%C3%8Dndices%20anuales%20Panam%C3%A1%20y%20SM_2017-24.xlsx) · [CSV](https://www.inec.gob.pa/archivos/P053342420260511104741Cuadro%205_%C3%8Dndices%20anuales%20Panam%C3%A1%20y%20SM_2017-24.csv) · [PDF](https://www.inec.gob.pa/archivos/P053342420260511104741Cuadro%205_%C3%8Dndices%20anuales%20Panam%C3%A1%20y%20SM_2017-24.pdf) |
| **Cuadro 6.** IPC en los distritos de Panamá y San Miguelito, según grupo…: **enero 2017–agosto 2025** | Excel con **una hoja por año** (2017…2025), también CSV y PDF | En las hojas `2019` y `2022`: las 12 columnas mensuales de **TOTAL** y **ALIMENTOS Y BEBIDAS NO ALCOHÓLICAS**. La hoja `2025` solo llega a **agosto** (último mes de esta base y geografía). | [Excel](https://www.inec.gob.pa/archivos/P0289562520260511104807Cuadro%206_%C3%8Dndices%20mensuales%20Panam%C3%A1%20y%20SM_2017-25.xlsx) · [CSV](https://www.inec.gob.pa/archivos/P0289562520260511104807Cuadro%206_%C3%8Dndices%20mensuales%20Panam%C3%A1%20y%20SM_2017-25.csv) · [PDF](https://www.inec.gob.pa/archivos/P0289562520260511104807Cuadro%206_%C3%8Dndices%20mensuales%20Panam%C3%A1%20y%20SM_2017-25.pdf) |

**Cifras anuales verificadas en el Cuadro 5 (Excel; en los PDF se redondean a 1 decimal):**

| Año | TOTAL (general) | Alimentos y bebidas no alcohólicas | Variación TOTAL | Variación alimentos |
|---|---|---|---|---|
| 2019 | 104.2 | 101.8 | −0.3 % | +0.3 % |
| 2022 | 106.9 | 106.3 | +2.6 % | +3.9 % |

Estas anuales coinciden con el **Cuadro 10** (TOTAL, años 2013-24: 2019 = 104.2, 2022 = 106.9) y con el **Cuadro 17** de 2018-19 / 2019-20 (alimentos 2019 = 101.8). El Cuadro 5 es el archivo único que trae **los dos grupos y los dos años**.

**Muestra mensual verificada en el Cuadro 6 (1 decimal, como en los boletines):**

| Mes | TOTAL 2019 | Alimentos 2019 | TOTAL 2022 | Alimentos 2022 |
|---|---|---|---|---|
| Enero | 103.8 | 102.1 | 105.1 | 103.6 |
| Junio | 104.3 | 101.8 | 109.1 | 106.3 |
| Diciembre | 104.0 | 101.6 | 106.8 | 109.0 |

Último mes de la serie vieja, agosto 2025, Panamá y San Miguelito, base 2013=100: TOTAL **108.9**, alimentos **111.5**.

**Estructura observada (Excel Cuadro 5 y 6):** título en las primeras filas; jerarquía de grupos en las columnas A–E (celdas combinadas, muchas vacías); los índices empiezan en la columna O (índice 14). El CSV usa **punto y coma** y codificación **latin-1** (no UTF-8). Conviene leer el Excel con `header=None` y ubicar las filas por el texto `TOTAL` y `ALIMENTOS Y BEBIDAS NO ALCOHÓLICAS`.

Apoyo opcional (misma serie, menos completo): Cuadro 10 TOTAL 2013-24, https://www.inec.gob.pa/archivos/A053342420250115131948Cuadro10.xlsx

#### B) Actualidad 2026 (nueva base)

A partir de **septiembre de 2025** el INEC publica el IPC con **base 2024 = 100**. En los boletines de 2026 la geografía ya no se llama “distritos de Panamá y San Miguelito”, sino **“provincia de Panamá”**. Cambian también las ponderaciones (EIGH 2017/18, 1,896 hogares urbanos) y la clasificación (CCIF 2018, 13 divisiones).

Fuente de la nota:  
https://www.inec.gob.pa/archivos/A0705547520251015154615NOTA%20T%C3%89CNICA%20IPC%202025.pdf  
Portal de cuadros vigentes:  
https://www.inec.gob.pa/avance/Default2.aspx?ID_CATEGORIA=2&ID_CIFRAS=10&ID_IDIOMA=1

| Archivo | Formato | Qué extraer | URL (HTTP 200) |
|---|---|---|---|
| **Cuadro 8.** IPC en la **provincia de Panamá**: diciembre 2025 y **enero–octubre 2026** | Excel / CSV / PDF | Columnas **Total** y **Alimentos y bebidas no alcohólicas**, todos los meses disponibles de 2026 (el año todavía no cierra). | [Excel](https://www.inec.gob.pa/archivos/A053342420261117083812Cuadro%208.xlsx) · [PDF](https://www.inec.gob.pa/archivos/A053342420261117083812Cuadro%208.pdf) |
| **Cuadro 7.** IPC en la provincia de Panamá por división: octubre 2025 y septiembre–octubre 2026 | Excel / PDF | Niveles y variación **interanual** octubre 2026 / octubre 2025 de TOTAL y de alimentos (misma base 2024=100). | [Excel](https://www.inec.gob.pa/archivos/A0705547520261117083707Cuadro%207.xlsx) · [PDF](https://www.inec.gob.pa/archivos/A0705547520261117083707Cuadro%207.pdf) |
| Informe completo IPC octubre 2026 | PDF | Contexto y definiciones. | https://www.inec.gob.pa/archivos/A0705547520261117082213IPC%20Octubre%202026.pdf |

**Cifras verificadas, provincia de Panamá, base 2024=100:**

| Mes | TOTAL | Alimentos y bebidas no alcohólicas |
|---|---|---|
| Diciembre 2025 | 99.9 | 101.1 |
| Enero 2026 | 100.4 | 101.3 |
| Junio 2026 | 102.0 | 101.6 |
| Agosto 2026 | 102.0 | 101.6 |
| Octubre 2026 | 102.9 | 102.4 |

Variación interanual octubre 2026 vs octubre 2025 (Cuadro 7): TOTAL **+3.3 %**; alimentos **+2.6 %**.

#### Cambio de base y cómo (no) empalmar

El **Anexo 3** compara bases 2013=100 y 2024=100, **solo IPC Nacional Urbano, solo el TOTAL, meses de 2024 y 2025**:  
[Excel](https://www.inec.gob.pa/archivos/A0705547520260313094310ANEXO_3.xlsx) · [PDF](https://www.inec.gob.pa/archivos/A0705547520260313094310ANEXO_3.pdf)

El propio anexo dice: *“A partir de septiembre de 2025 el Índice de Precios al Consumidor se publica con año base 2024 = 100. Para mantener la comparabilidad de la serie histórica, los valores anteriores fueron empalmados mediante un factor de enlace. Debido a este procedimiento, las variaciones calculadas en el mes de transición pueden presentar ligeras diferencias respecto a las variaciones obtenidas con la serie original en base 2013.”*

En el Excel del Anexo 3, el **promedio anual 2024** es 110.2762 en base 2013 y **100.0** en base 2024. El factor de enlace del TOTAL nacional es, por tanto:

```text
factor = 100 / 110.2762  ≈  0.9068
indice_2024base = indice_2013base * factor
```

**Reglas para el equipo (no saltárselas):**

1. Ese factor es **oficial solo para el TOTAL del IPC Nacional Urbano**. No se encontró un anexo equivalente para “Panamá y San Miguelito”, ni para “provincia de Panamá”, ni para el grupo de alimentos.
2. **No apliquen** el factor nacional a la serie de Panamá y San Miguelito, ni a los alimentos.
3. **No pongan en el mismo eje** un índice 2019 = 104.2 (base 2013) y un índice 2026 = 102.9 (base 2024): no son comparables.
4. Forma correcta de usar 2026 en este proyecto:
   - **2019 vs 2022:** comparar **niveles** en base 2013=100 (Cuadros 5 y 6).
   - **2026 (actualidad):** reportar niveles en base 2024=100 y, sobre todo, la **variación interanual** ya calculada por el INEC (Cuadro 7), más el costo de la canasta ACODECO/MEF, que sí está en balboas en los tres años.
5. El Anexo 4 (nacional urbano, enero 2024–octubre 2026, ya en 2024=100) solo sirve como contexto nacional, no como serie del proyecto:  
   https://www.inec.gob.pa/archivos/A0705547520261117084308Anexo%204.xlsx

### 1.2 Bloque 1 — Costo de la canasta ACODECO (histórico)

| Archivo | Formato | Bloque | Qué extraer | URL (HTTP 200) |
|---|---|---|---|---|
| HistoricoCBFA_2015-2026.pdf | PDF, 12 páginas, generado desde Excel (no es un escaneo) | 1 y 3 | Precio promedio de los 59 productos y el **COSTO TOTAL** mensual, **provincia de Panamá**, supermercados. Usar 2019 (12 meses), 2022 (12 meses) y 2026 (enero–agosto). | https://www.acodeco.gob.pa/wp-content/uploads/2026/10/HistoricoCBFA_2015-2026.pdf |

`pdftotext -layout` extrae la tabla (se comprobó). Cuidado: en algunos años los últimos meses del **COSTO TOTAL** se cortan o saltan de renglón; hay que verificar a mano contra el PDF. No sumar los 59 precios unitarios: el costo total ya aplica las cantidades de la canasta.

**COSTO TOTAL verificado (B/.):**

| Mes | 2019 | 2022 | 2026 |
|---|---|---|---|
| Enero | 262.93 | 278.87 | 304.40 |
| Junio | 260.64 | 285.92 | 303.45 |
| Agosto | 263.09 | 285.06 | 304.85 |
| Diciembre | 263.52 | 287.41 | (el PDF llega a agosto) |

Serie 2019 completa: 262.93, 262.51, 261.19, 262.19, 264.89, 260.64, 261.90, 263.09, 263.90, 265.44, 263.13, 263.52.  
Serie 2022 completa: 278.87, 274.00, 275.65, 275.66, 280.71, 285.92, 292.52, 285.06, 283.91, 283.92, 286.51, 287.41.  
Serie 2026 (ene–ago): 304.40, 303.04, 302.79, 303.53, 305.13, 303.45, 303.67, 304.85.

### 1.3 Bloque 1 — Costo calórico MEF (Panamá y San Miguelito)

Catálogo: https://www.mef.gob.pa/canasta-basica/  
Metodología constante y declarada en los informes: **59 productos**, 3.5 personas, 2,338.6 kcal/día, precios del INEC. (El Resto Urbano, 50 productos, **queda fuera del alcance**: el proyecto se quedó en la provincia de Panamá / Panamá y San Miguelito.)

El catálogo, en la sección 2019, **solo lista febrero, marzo y abril**, pero existen los 12 meses en PDF numerados (todos se descargaron, HTTP 200, y se leyeron). En 2022 **falta agosto** en el catálogo. En 2026 hay informes hasta **agosto**; enero y febrero vienen en un solo PDF.

**Recomendación:** bajar **todos los meses disponibles** de 2019, 2022 y 2026 (son un dato por informe y alimentan mejor el bloque 3).  
**Mínimo suficiente** si hay que recortar: enero, junio y diciembre de 2019 y 2022, más enero, junio y agosto de 2026.

#### 2019 (costo PySM verificado en cada PDF)

| Mes | Costo PySM (B/.) | URL |
|---|---|---|
| Enero | 306.08 | https://www.mef.gob.pa/wp-content/uploads/2020/12/1-MEF_DAES_Canasta-Basica-de-Alimentos-Enero-2019.pdf |
| Febrero | 304.59 | https://www.mef.gob.pa/wp-content/uploads/2020/12/2-MEF_DAES_Canasta-Basica-de-Alimentos-Febrero-2019.pdf |
| Marzo | 304.61 | https://www.mef.gob.pa/wp-content/uploads/2020/12/3-MEF_DAES_Canasta-Basica-de-Alimentos-Marzo-2019.pdf |
| Abril | 306.76 | https://www.mef.gob.pa/wp-content/uploads/2020/12/MEF-DAES-Informe-de-la-Canasta-Basica-Familiar-de-Alimento-Abril-2019.pdf |
| Mayo | 308.21 | https://www.mef.gob.pa/wp-content/uploads/2020/12/5-MEF_DAES_Canasta-Basica-de-Alimentos-Mayo-2019.pdf |
| Junio | 308.99 | https://www.mef.gob.pa/wp-content/uploads/2020/12/6-MEF_DAES_Canasta-Basica-de-Alimentos-Junio-2019.pdf |
| Julio | 310.38 | https://www.mef.gob.pa/wp-content/uploads/2020/12/7-MEF_DAES_Canasta-Basica-de-Alimentos-Julio-2019.pdf |
| Agosto | 308.25 | https://www.mef.gob.pa/wp-content/uploads/2020/12/8-MEF_DAES_Canasta-Basica-de-Alimentos-Agosto-2019.pdf |
| Septiembre | 310.04 | https://www.mef.gob.pa/wp-content/uploads/2020/12/9-MEF_DAES_Canasta-Basica-de-Alimentos-Septiembre-2019.pdf |
| Octubre | 310.06 | https://www.mef.gob.pa/wp-content/uploads/2020/12/10-MEF_DAES_Canasta-Basica-de-Alimentos-Octubre-2019.pdf |
| Noviembre | 306.42 | https://www.mef.gob.pa/wp-content/uploads/2020/12/11-MEF_DAES_Canasta-Basica-de-Alimentos-Noviembre-2019.pdf |
| Diciembre | 306.68 | https://www.mef.gob.pa/wp-content/uploads/2020/12/12-MEF_DAES_Canasta-Basica-de-Alimentos-Diciembre-2019.pdf |

De cada informe extraer el **costo calórico de los distritos de Panamá y San Miguelito** (la cifra que aparece en la introducción, no la de “sin control de precios”).

#### 2022 (enlaces del catálogo oficial; agosto no está)

| Mes | Costo PySM ya verificado | URL del catálogo |
|---|---|---|
| Enero | 318.12 | https://www.mef.gob.pa/wp-content/uploads/2022/06/MEF-DAES-_Canasta-Basica-de-Alimentos-Enero-2022.pdf |
| Febrero | — (extraer del PDF) | https://www.mef.gob.pa/wp-content/uploads/2022/07/MEF-DAES-_Canasta-Basica-de-Alimentos-Febrero-2022.pdf |
| Marzo | — | https://www.mef.gob.pa/wp-content/uploads/2022/07/MEF-DAES-_Canasta-Basica-de-Alimentos-Marzo-2022.pdf |
| Abril | — | https://www.mef.gob.pa/wp-content/uploads/2022/07/MEF-DAES-_Canasta-Basica-de-Alimentos-Abril-2022.pdf |
| Mayo | — | https://www.mef.gob.pa/wp-content/uploads/2022/07/MEF-DAES-_Canasta-Basica-de-Alimentos-Mayo-2022.pdf |
| Junio | 330.40 | https://www.mef.gob.pa/wp-content/uploads/2022/08/MEF-DAES-_Canasta-Basica-de-Alimentos-Junio-2022.pdf |
| Julio | — | https://www.mef.gob.pa/wp-content/uploads/2022/10/MEF-DAES-_Canasta-Basica-de-Alimentos-Julio-2022.pdf |
| Septiembre | — | https://www.mef.gob.pa/wp-content/uploads/2023/01/MEF-DAES-_Canasta-Basica-de-Alimentos-Septiembre-2022.pdf |
| Octubre | — | https://www.mef.gob.pa/wp-content/uploads/2023/03/MEF-DAES-_Canasta-Basica-de-Alimentos-Octubre-2022.pdf |
| Noviembre | — | https://www.mef.gob.pa/wp-content/uploads/2023/03/MEF-DAES-Canasta-Basica-Familiar-de-Alimentos-Noviembre-2022-.pdf |
| Diciembre | — | https://www.mef.gob.pa/wp-content/uploads/2023/04/MEF-DAES-_Canasta-Basica-de-Alimentos-Diciembre-2022.pdf |

#### 2026 (hasta agosto; enero y febrero en un PDF)

| Mes | Costo PySM ya verificado | URL del catálogo |
|---|---|---|
| Enero y febrero (un informe) | — (extraer ambos meses) | https://www.mef.gob.pa/wp-content/uploads/2026/05/MEF-DAES.Canasta-Basica-Familiar-de-Alimentos-ENERO-Y-FEBRERO-2026.pdf |
| Marzo | — | https://www.mef.gob.pa/wp-content/uploads/2026/06/MEF-DAES-Canasta-Basica-Familiar-de-Alimentos-MARZO-2026.pdf |
| Abril | — | Enlace del catálogo (el nombre del archivo lleva tilde en “Básica”; bajarlo desde https://www.mef.gob.pa/canasta-basica/ si el copiado falla): `…/2026/07/MEF-DAES-Canasta-Básica-Familiar-de-Alimentos-ABRIL-2026.pdf` |
| Mayo | — | https://www.mef.gob.pa/wp-content/uploads/2026/08/MEF-DAES-Canasta-Basica-Familiar-de-Alimentos-MAYO-2026.pdf |
| Junio | — | https://www.mef.gob.pa/wp-content/uploads/2026/08/MEF-DAES-Canasta-Basica-Familiar-de-Alimentos-JUNIO-2026.pdf |
| Julio | — | https://www.mef.gob.pa/wp-content/uploads/2026/10/MEF-DAES-Canasta-Basica-Familiar-de-Alimentos-JULIO-2026.pdf |
| Agosto | **369.21** (mes previo 368.24) | https://www.mef.gob.pa/wp-content/uploads/2026/11/MEF-DAES-Canasta-Basica-Familiar-de-Alimentos-AGOSTO-2026.pdf |

**Caveat:** el costo MEF y el COSTO TOTAL de ACODECO **no son intercambiables**. El MEF es un costo calórico familiar (cantidades INCAP, precios INEC). ACODECO es el costo de su canasta de 59 productos a precios promedio de supermercados de la provincia. Usar ambas series en paralelo, no mezclarlas en una sola línea.

### 1.4 Bloque 2 — Salario mínimo (MITRADEL / Gaceta Oficial)

Las gacetas están escaneadas (`pdftotext` sale vacío). Hay que usar OCR o transcribir de la imagen. Pedir el PDF con un `User-Agent` de navegador; sin eso, el sitio a veces devuelve un HTML de Incapsula de 212 bytes.

| Decreto | Vigencia para este proyecto | Qué extraer | URL (HTTP 200) |
|---|---|---|---|
| **Decreto Ejecutivo 75 de 26 de diciembre de 2017**, Gaceta 28433-A | **2019** (vigente 1 ene 2018–31 dic 2019). El Decreto 424 de 31 dic 2019 es el *siguiente* periodo, no el de 2019. | Comercio al por menor, **Región 1 y Región 2**: pequeña y gran empresa. En 2017 **no existe** la fila “supermercados 5 o más sucursales”. También el doméstico (mensual oficial) y la lista de distritos de la Región 1. | Gaceta completa: https://www.gacetaoficial.gob.pa/storage/gacetas/2017/12/28433_A/GacetaNo_28433a_20171227.pdf · Extracto del decreto: https://www.gacetaoficial.gob.pa/pdfTemp/28433_A/65233.pdf |
| **Decreto Ejecutivo 74 de 31 de diciembre de 2021**, Gaceta 29446-C | **2022** (desde el 16 de enero de 2022) | Comercio al por menor R1 y R2: pequeña, gran empresa y **supermercados 5+**. Doméstico mensual. Lista de distritos R1. | https://www.gacetaoficial.gob.pa/storage/gacetas/2021/12/29446_C/GacetaNo_29446c_20211231.pdf |
| **Decreto Ejecutivo 13 de 31 de diciembre de 2025**, Gaceta 30438 | **2026** (desde el 16 de enero de 2026) | Igual que 2022: pequeña, gran, supermercados 5+, doméstico, distritos. | https://www.gacetaoficial.gob.pa/storage/gacetas/2026/01/30438/GacetaNo_30438_20260106.pdf |

**Tasas horarias verificadas, comercio al por menor (B/.):**

| Decreto (año) | R1 pequeña | R1 gran empresa | R1 súper 5+ | R2 pequeña | R2 gran | R2 súper 5+ |
|---|---|---|---|---|---|---|
| DE 75 (2019) | **2.20** | **2.72** | no existe | **1.84** | **2.23** | no existe |
| DE 74 (2022) | **2.27** | **2.81** | **2.88** | **1.90** | **2.30** | **2.36** |
| DE 13 (2026) | **2.37** | **3.02** | **3.09** | **1.99** | **2.48** | **2.54** |

Doméstico mensual oficial: 2019 R1 275 / R2 250; 2022 R1 315 / R2 290; 2026 R1 350 / R2 320.

Equivalente mensual de las tasas horarias (no es un salario legal impreso): **hora × 208** (48 h × 52 / 12). Ejemplo 2022 R1 gran empresa: 2.81 × 208 = 584.48.

**Región 1 vs Región 2:** la Región 1 incluye, entre otros, Panamá, Colón, San Miguelito, David, Santiago, Chitré, La Chorrera, Arraiján, etc. La Región 2 es “el resto de los distritos”. En el decreto de 2017 la lista de la Región 1 es un poco más corta (aún no aparecen Almirante, Tierras Altas ni Omar Torrijos Herrera). Este contraste salarial **solo va en el bloque 2**; el cruce con la canasta (bloque 3) usa **Región 1**, que es la que corresponde a la provincia de Panamá / Ciudad de Panamá.

### 1.5 Bloque 4 — Precios por supermercado (CSV 2019 y 2022 + PDF 2026)

Conjuntos en datos abiertos (59 productos, supermercados de la **Ciudad de Panamá**; algunos establecimientos de San Miguelito van en los mismos archivos):

- 2019 (marzo–diciembre; **no hay enero ni febrero**): https://www.datosabiertos.gob.pa/dataset/precios-de-productos-de-cba-2019  
  id CKAN: `653d6c37-cb33-40a9-9728-733f0cc90acc`
- 2022 (enero–junio): https://www.datosabiertos.gob.pa/dataset/acodeco-precios-de-productos-de-cba-2022  
  id CKAN: `804a1e66-64a7-4720-aa11-bb92c976b17d`

**CSV 2019, URLs directas (todas HTTP 200 el 22 nov 2026):**

| Mes | URL |
|---|---|
| Marzo | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/3d169448-7ca3-446d-aa51-5fa2c28e26bc/download/cba_marzo2019.csv |
| Abril | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/097af175-7be2-4ab2-9c76-50e8ef0bef6c/download/cba_abril2019.csv |
| Mayo | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/9a6f90fc-513a-4fc1-b265-48cca3021113/download/cba_may2019.csv |
| Junio | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/4d2deef4-44a9-485f-890b-d58a2cdd71c5/download/cba_jun2019.csv |
| Julio | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/06134a64-803c-4722-870b-cd306341ee1f/download/cba_jul2019.csv |
| Agosto | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/204f1644-f61a-4078-9ceb-063a1f402f84/download/cba_ago2019.csv |
| Septiembre | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/1ba897ea-afab-4dff-8601-f25295ad10e9/download/cba_sep2019.csv |
| Octubre | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/7722f1a0-a36d-4541-ab50-c881e3729e00/download/cba_oct2019.csv |
| Noviembre | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/4a4eba2e-66f0-4e40-9438-75efafb26fa7/download/cba_nov2019.csv |
| Diciembre | https://www.datosabiertos.gob.pa/dataset/653d6c37-cb33-40a9-9728-733f0cc90acc/resource/0568c9da-46d2-4ae4-afe4-71f13c375625/download/cba_dic2019.csv |

**CSV 2022, URLs directas (ya usadas, HTTP 200):**

| Mes | URL |
|---|---|
| Enero | https://www.datosabiertos.gob.pa/dataset/804a1e66-64a7-4720-aa11-bb92c976b17d/resource/69b29e97-1ca4-4d2b-b02c-ba87f888a562/download/cba_ene2022.csv |
| Febrero | https://www.datosabiertos.gob.pa/dataset/804a1e66-64a7-4720-aa11-bb92c976b17d/resource/f18e85fb-2df4-4eec-b432-89ce7373dfc7/download/cba_feb2022.csv |
| Marzo | https://www.datosabiertos.gob.pa/dataset/804a1e66-64a7-4720-aa11-bb92c976b17d/resource/f4a9ff0e-51b4-410e-b11f-5395bfbf2258/download/cba_marzo2022csv.csv |
| Abril | https://www.datosabiertos.gob.pa/dataset/804a1e66-64a7-4720-aa11-bb92c976b17d/resource/8218c25d-5b13-446b-a711-7cb7abf00ab4/download/cba_abril2022_csv.csv |
| Mayo | https://www.datosabiertos.gob.pa/dataset/804a1e66-64a7-4720-aa11-bb92c976b17d/resource/f9f97559-62b1-4348-b312-667e96f79901/download/cbamayo2022.csv |
| Junio | https://www.datosabiertos.gob.pa/dataset/804a1e66-64a7-4720-aa11-bb92c976b17d/resource/27162758-05d6-44a1-b7c3-4012cec61957/download/cba_junio2022.csv |

De cada CSV extraer, después de limpiar, el precio de cada producto en cada establecimiento (formato largo). Hay también XLS y PDF del mismo mes en el mismo conjunto, útiles para cruzar si un CSV viene raro.

**PDF quincenal, 2.ª quincena de septiembre 2026** (actualidad del bloque 4):  
https://www.acodeco.gob.pa/wp-content/uploads/2026/10/CBA_PreciosSupermercadosXRutas_2daSeptiembre2026.pdf  
HTTP 200, 5 páginas apaisadas, generado desde Excel. `pdftotext -layout` sí extrae las tablas (se comprobó). Páginas 1–3: supermercados por zona (Bella Vista, Bethania, Juan Díaz, Parque Lefevre, Pueblo Nuevo, San Francisco, **San Miguelito**, Villa Zaita, Santa Ana, Tocumen, etc.). Páginas 4–5: “en Rutas” (minisúper / abarroterías), también con un recuadro San Miguelito. Extraer producto, medida, establecimiento, zona/ruta y precio. La cabecera ocupa 2–3 renglones: habrá que alinear columnas y **verificar a mano** una muestra.

No hay CSV abiertos de ACODECO para 2026 ni para otras provincias.

---

## 2. Estructura base del repositorio

Nombre: `canasta-vs-salario-panama`

```text
canasta-vs-salario-panama/
├── README.md                          # Objetivo, alcance (provincia de Panamá, 2019/2022/2026), fuentes y cómo reproducir
├── requirements.txt                   # pandas, openpyxl, xlrd, pdfplumber, matplotlib, jupyter, requests, lxml
├── data/
│   ├── raw/                           # Archivos tal cual salen de la fuente; no se editan
│   │   ├── acodeco/
│   │   │   ├── csv_2019/              # Los 10 CSV marzo–diciembre 2019
│   │   │   ├── csv_2022/              # Los 6 CSV enero–junio 2022
│   │   │   ├── HistoricoCBFA_2015-2026.pdf
│   │   │   └── CBA_PreciosSupermercadosXRutas_2daSeptiembre2026.pdf
│   │   ├── mef/                       # PDF mensuales 2019, 2022 y 2026 (solo PySM se va a usar)
│   │   ├── inec/
│   │   │   ├── Cuadro5_anual_PySM_2017-24.xlsx
│   │   │   ├── Cuadro6_mensual_PySM_2017-25.xlsx
│   │   │   ├── Cuadro7_provincia_oct2026.xlsx
│   │   │   ├── Cuadro8_provincia_mensual_2026.xlsx
│   │   │   ├── Anexo3_enlace_nacional.xlsx
│   │   │   └── Nota_tecnica_IPC_2024.pdf
│   │   └── mitradel/                  # Las 3 gacetas (DE 75, DE 74, DE 13)
│   ├── interim/                       # Salidas a medio limpiar (un mes, un PDF), todavía no para el análisis
│   └── processed/                     # Tablas tidy finales (csv o parquet): ipc, costo_canasta_mensual, salario_minimo, precios_supermercados
├── notebooks/
│   ├── 00_importacion_y_limpieza.ipynb  # Llama a src/, muestra controles de calidad, guarda processed/
│   ├── 01_ipc_y_costo_canasta.ipynb     # Bloque 1
│   ├── 02_salario_minimo.ipynb          # Bloque 2 (incluye R1 vs R2)
│   ├── 03_poder_adquisitivo.ipynb       # Bloque 3
│   └── 04_supermercados.ipynb           # Bloque 4
├── src/
│   ├── __init__.py
│   ├── io_acodeco.py                  # Lectura robusta de CSV 2019/2022 y extracción de los dos PDF
│   ├── io_inec.py                     # Lectura de los Excel del IPC y armado de la tabla ipc
│   ├── io_mef.py                      # Extracción del costo PySM desde cada PDF del MEF
│   ├── io_salarios.py                 # Tabla de salarios a partir de la transcripción verificada de los decretos
│   ├── limpieza.py                    # Nombres de producto y de tienda, zonas, fechas, asteriskos
│   └── esquemas.py                    # Columnas canónicas y validaciones simples
├── outputs/
│   └── figures/                       # Gráficos de los cuatro bloques
└── referencias/                       # Este plan y, si se quiere, un diccionario de tiendas/zonas en CSV
```

Un propósito por pieza: los CSV crudos no se tocan; toda la lógica de rarezas (separador, columnas de más, pie de página) vive en `src/`; los notebooks de análisis solo leen `data/processed/`.

---

## 3. Importación, limpieza y ordenamiento

### 3.1 Tablas tidy de destino

**`ipc`** — una fila por mes, geografía y grupo.

| Columna | Contenido |
|---|---|
| fecha | Primer día del mes (`2019-06-01`) |
| anio, mes | 2019, 6 |
| geografia | `panama_y_san_miguelito` o `provincia_de_panama` |
| grupo | `total` o `alimentos_y_bebidas_no_alcoholicas` |
| indice | Número del INEC |
| base | `2013=100` o `2024=100` |
| fuente | Nombre del cuadro (ej. `INEC Cuadro 6 2017-25`) |

No mezclar bases en cálculos de variación de largo plazo. Filtrar por `base` y `geografia` antes de graficar niveles.

**`costo_canasta_mensual`** — una fila por mes y fuente.

| Columna | Contenido |
|---|---|
| fecha, anio, mes | Igual que arriba |
| fuente | `acodeco_historico` o `mef_cbfa` |
| geografia | `provincia_de_panama` (ACODECO) o `panama_y_san_miguelito` (MEF) |
| n_productos | 59 |
| costo_total | Balboas del mes |
| notas | Ej. “MEF: costo calórico familiar; no comparable 1:1 con ACODECO” |

**`salario_minimo`**

| Columna | Contenido |
|---|---|
| fecha_inicio | 2018-01-01, 2022-01-16, 2026-01-16 |
| anio_analisis | 2019, 2022 o 2026 |
| decreto | `DE 75/2017`, `DE 74/2021`, `DE 13/2025` |
| region | `1` o `2` |
| actividad | `comercio_al_por_menor` o `trabajo_domestico` |
| categoria | `pequena`, `gran_empresa`, `supermercados_5_plus`, `domestico` |
| salario_hora | Numérico o NA si es doméstico |
| salario_mensual | `salario_hora * 208` (fórmula) o el mensual oficial del doméstico |
| es_oficial_mensual | True solo en doméstico |
| categoria_existia | False para supermercados 5+ en 2019 |

**`precios_supermercados`**

| Columna | Contenido |
|---|---|
| fecha, anio, mes | En 2026, además `quincena` (2 = segunda de septiembre) |
| producto | Nombre original |
| producto_estandar | Nombre limpio y unificado 2019/2022/2026 |
| medida | Ej. `1 Kilogramos` |
| establecimiento | Nombre original de la columna |
| establecimiento_estandar | Nombre limpio (tildes, espacios, typo `VÖA` → `VIA`) |
| cadena | Super 99, Rey, Xtra, Machetazo, Riba Smith, El Fuerte, minisúper, etc. |
| zona | `capital`, `san_miguelito` o `sin_clasificar` (diccionario revisado a mano; no adivinar) |
| precio | `float`; los vacíos quedan en **NaN, nunca en 0** |
| control_precio | True si el nombre del producto traía `*` |
| fuente | `acodeco_csv` o `acodeco_pdf_sep2026` |

### 3.2 ACODECO CSV — rarezas reales (inspeccionadas)

Todos los archivos son **latin-1** (o cp1252). UTF-8 falla. El carácter `Ñ` a veces ya viene roto en el origen (`ESPA¥A`). Hay unos 89–90 establecimientos.

| Archivo | Separador | Cabecera | Columnas extra al inicio | Otras rarezas |
|---|---|---|---|---|
| 2019 abr, may, jun, sep | coma | Fila 0 | No | — |
| 2019 jul | coma | Fila 1 (fila 0 vacía de comas) | No | — |
| 2019 mar, ago, oct | coma | Fila 1 o 2 | Sí: código de grupo y número de producto (`14,1,Babilla…`) | — |
| 2019 nov | **punto y coma** | Fila 1 | Sí, dos columnas | — |
| 2019 dic | **punto y coma** | Fila 2 (dos filas vacías) | Sí, dos columnas | Fila final **Costo Total** por tienda: **borrarla**, no es un producto |
| 2022 ene | coma | Fila 0 | No | Última fila `FUENTE: ACODECO` |
| 2022 feb | coma | Fila 1 (fila 0 vacía) | No | Última fila `FUENTE: ACODECO` |
| 2022 mar, abr, may, jun | coma | Fila 0 | No | Sin pie `FUENTE` (no borrar tiendas cuyo nombre contiene “FUENTE”, ej. Minisuper Fuente de Oro) |

El asterisco al final del producto (`Babilla (Carne de res de Primera) *`) marca **control de precios**. Quitar el `*` del nombre y dejar `control_precio=True`.

Pasos, para cada mes:

1. Leer en binario y decodificar `latin-1`.
2. Detectar separador (si hay más `;` que `,` en las primeras líneas).
3. Saltar filas vacías hasta encontrar la que contiene `Producto` y `Medida`.
4. Si las dos primeras columnas no se llaman Producto/Medida, eliminarlas.
5. Tirar filas de `Costo Total` y de `FUENTE:` (coincidencia al *inicio* de la fila, no en cualquier parte).
6. `melt` de ancho a largo.
7. Precios a número; vacío → `NaN`.
8. Añadir `anio`, `mes`, `fecha` según el nombre del archivo (no fiarse de una fecha interna; no la hay).
9. Estandarizar producto, medida, establecimiento; asignar `cadena` y `zona`.
10. `pd.concat` de todos los meses.

Snippet de lectura y melt:

```python
from pathlib import Path
import pandas as pd

def leer_cba_csv(path, anio, mes):
    raw = Path(path).read_bytes()
    texto = raw.decode("latin-1")
    muestra = "\n".join(texto.splitlines()[:5])
    sep = ";" if muestra.count(";") > muestra.count(",") else ","
    df = pd.read_csv(path, encoding="latin-1", sep=sep, header=None, dtype=str)
    # buscar fila de cabecera
    mask = df.apply(lambda r: r.astype(str).str.contains("Producto", na=False).any(), axis=1)
    i = int(mask.idxmax())
    df.columns = df.iloc[i].fillna("").astype(str).str.strip()
    df = df.iloc[i + 1 :].copy()
    # columnas índice sobrantes
    cols = list(df.columns)
    if cols[0] not in {"Producto", "Medida"} and "Producto" in cols:
        df = df.drop(columns=[c for c in cols[:2] if c not in {"Producto", "Medida"}])
    primer = df.iloc[:, 0].astype(str)
    df = df[~primer.str.contains(r"^(Costo Total|FUENTE)", case=False, na=False)]
    df = df[df["Producto"].notna() & (df["Producto"].str.strip() != "")]
    id_vars = ["Producto", "Medida"]
    value_vars = [c for c in df.columns if c not in id_vars and c.strip() != ""]
    largo = df.melt(id_vars=id_vars, value_vars=value_vars,
                    var_name="establecimiento", value_name="precio")
    largo["control_precio"] = largo["Producto"].str.contains(r"\*", regex=True, na=False)
    largo["producto"] = largo["Producto"].str.replace(r"\s*\*\s*$", "", regex=True).str.strip()
    largo["precio"] = pd.to_numeric(
        largo["precio"].str.replace(",", ".", regex=False), errors="coerce"
    )  # NaN, nunca 0
    largo["anio"], largo["mes"] = anio, mes
    largo["fecha"] = pd.Timestamp(anio, mes, 1)
    return largo

# concatenar todos los meses
# precios = pd.concat([leer_cba_csv(p, a, m) for p, a, m in lista], ignore_index=True)
```

Diccionario mínimo de zona: partir de los establecimientos cuyo nombre trae “SAN MIGUELITO” (El Fuerte San Miguelito, El Machetazo San Miguelito, abarroterías León y Denia, etc.) y, para 2026, de los recuadros titulados **SAN MIGUELITO** en el PDF. El resto de tiendas (Villa Lucre, Los Andes, Brisas del Golf, etc.) solo se clasifican si el equipo las confirma en ese recuadro o en una fuente oficial; si no, `sin_clasificar`. No inventar corregimientos.

Estandarizar nombres de producto entre 2019, 2022 y 2026: minúsculas, sin `*`, espacios simples, tildes unificadas, un `mapa_productos.csv` revisado a mano para las 59 filas. Lo mismo para cadenas (`SUPER 99`, `Super 99`, `Súper 99` → `Super 99`).

### 3.3 PDF de ACODECO (histórico y septiembre 2026)

Los dos PDF salieron de **Microsoft Excel 2013**, no están escaneados. `pdftotext -layout` funciona. `pdfplumber` o `tabula`/`camelot` deberían funcionar igual; igual hay que **verificar a mano** el COSTO TOTAL y una muestra de precios.

Histórico (12 páginas, un año por hoja en la práctica): extraer la fila `COSTO TOTAL` de 2019, 2022 y 2026, y si se quiere los precios promedio por producto. Si una fila se parte en dos líneas, no rellenar con ceros; comparar con las cifras ya verificadas de la sección 1.2.

Septiembre 2026 (5 páginas apaisadas): cabecera multilínea (zona en un renglón, nombre de tienda en dos). Extraer página por página, asignar la zona del encabezado (`SAN MIGUELITO`, `BELLA VISTA`, …) a las columnas de esa página, y revisar al menos 5 celdas por página contra el PDF.

```python
import pdfplumber
import pdfplumber  # o: pdftotext -layout archivo.pdf - > archivo.txt

with pdfplumber.open("data/raw/acodeco/HistoricoCBFA_2015-2026.pdf") as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        tablas = page.extract_tables()  # revisar; si sale pobre, usar page.extract_text()
```

Las gacetas del salario **sí** están escaneadas: ahí sí hace falta OCR (`tesseract -l spa`) o transcripción, y luego una tabla en `src/io_salarios.py` con las cifras ya verificadas de la sección 1.4 (no recalcular tasas desde un OCR sucio en el análisis).

### 3.4 INEC IPC

1. Leer el Excel con `pd.read_excel(..., header=None)`.
2. En Cuadro 5, los años están en la fila de encabezado (columna O en adelante: 2017…2024); tomar 2019 y 2022 de las filas TOTAL y ALIMENTOS Y BEBIDAS NO ALCOHÓLICAS.
3. En Cuadro 6, iterar las hojas `2019` y `2022` (y 2025 solo como contexto del corte de serie). Meses en la fila de encabezado, mismas dos filas de grupos, valores desde la columna O.
4. Cuadros 7 y 8 (2026): geografía `provincia_de_panama`, base `2024=100`.
5. Guardar todo en `ipc` con las columnas de la sección 3.1. Redondear para tablas publicadas a 1 decimal, pero guardar el valor del Excel.
6. El CSV oficial del Cuadro 5/6 es latin-1 y punto y coma, y hereda las celdas combinadas: **preferir el Excel**.

```python
df = pd.read_excel(path, sheet_name="2019", header=None)
meses = df.iloc[4, 14:].tolist()          # Enero … Diciembre
fila_total = df[df[0].eq("TOTAL")].iloc[0, 14:]
fila_alim = df[df[0].astype(str).str.contains("ALIMENTOS Y BEBIDAS", na=False)].iloc[0, 14:]
```

### 3.5 MEF

Por cada PDF: `pdftotext -layout` o pdfplumber; buscar en la introducción la oración del tipo “distritos de Panamá y San Miguelito … B/.306.08”. No usar la cifra “sin la medida de control de precios” ni el dato del Resto Urbano. Validar enero, junio y diciembre 2019 y enero/junio 2022 y agosto 2026 contra las cifras de la sección 1.3. El informe ene–feb 2026 trae **dos** meses.

### 3.6 Antes de analizar (controles)

- 59 productos por mes en los CSV (después de quitar Costo Total / FUENTE).
- Ningún precio faltante convertido a 0.
- Series ACODECO histórico: 12 + 12 + 8 meses.
- `ipc` con `base` y `geografia` siempre llenos; ningún gráfico de niveles mezcla 2013=100 con 2024=100.
- Salarios 2019 sin fila de supermercados 5+.
- Bloque 3: canasta solo contra **Región 1**; el equivalente mensual es hora × 208, salvo el doméstico.

Fórmulas del bloque 3 (cuando las tablas ya están tidy):

```text
pct_salario_en_comida = costo_canasta / salario_mensual_R1 * 100
horas_para_pagar      = costo_canasta / salario_hora_R1
var_canasta           = costo_t / costo_2019 - 1
var_salario           = salario_t / salario_2019 - 1
```

Elegir y declarar una sola categoría de salario para el cruce principal (por ejemplo, comercio al por menor, gran empresa, Región 1) y mostrar las otras como sensibilidad.

---

## 4. División de trabajo (4 personas)

| Persona | Encargo | Entrega |
|---|---|---|
| **A** | Estructura del repo, `requirements.txt`, README, descarga de *todos* los raw, y `src/io_inec.py` + tabla `ipc` (incluido el tratamiento del cambio de base). | `data/raw/` completo, `data/processed/ipc.csv`, nota metodológica del IPC en el README |
| **B** | `src/io_acodeco.py` y `limpieza.py`: CSV 2019/2022, histórico PDF, PDF de septiembre 2026, diccionario de productos, cadenas y zonas. | `precios_supermercados.csv`, `costo_canasta_mensual` (parte ACODECO) |
| **C** | `src/io_mef.py` (costo PySM de todos los meses acordados) y `src/io_salarios.py` (transcripción verificada de los tres decretos, R1 y R2). | `costo_canasta_mensual` (parte MEF), `salario_minimo.csv` |
| **D** | Notebooks 01–04: gráficos y resultados; bloque 3 con el cruce ya limpio; revisión de que nadie mezcle bases del IPC ni sume NaN como cero. | `notebooks/01`–`04`, `outputs/figures/` |

El notebook `00` lo pueden armar A y B juntos el primer día, para que C y D no analicen crudos. Reunión corta de control cuando existan las cuatro tablas de `data/processed/`.

---

## 5. Recordatorios finales

- Alcance: provincia de Panamá, años 2019, 2022 y 2026. No hay CSV provinciales de ACODECO para el interior.
- ACODECO y MEF se muestran en paralelo, no se fusionan en una sola “canasta”.
- El salario de la Región 2 no se cruza con la canasta de la capital; solo ilustra la brecha del país en el bloque 2.
- El IPC de 2026 no se “empalma” con 2019/2022 salvo con un factor oficial que, hoy, **no existe** para Panamá y San Miguelito ni para alimentos.
- Este archivo es la guía de datos. La hoja de Google Sheets del inventario no se modificó.
