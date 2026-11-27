"""Consulta de IPC y costo de la canasta básica.

Lee solo data/processed/ (ipc.csv y costo_canasta_mensual.csv).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

def _ruta_processed() -> Path:
    """Busca data/processed subiendo desde este archivo o desde el cwd."""
    for base in (Path(__file__).resolve().parent, Path.cwd()):
        for carpeta in (base, *base.parents):
            candidata = carpeta / "data" / "processed"
            if candidata.is_dir():
                return candidata
    return Path("data") / "processed"


PROCESSED = _ruta_processed()

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre",
    11: "noviembre", 12: "diciembre",
}
GRUPOS = {
    "total": "total",
    "alimentos": "alimentos_y_bebidas_no_alcoholicas",
}
FUENTES = {
    "acodeco": "acodeco_historico",
    "mef": "mef_cbfa",
}

# Variaciones publicadas por el INEC (guia_analisis.md). No se recalculan.
INFLACION_OFICIAL = pd.DataFrame(
    [
        ("2019 (variación anual, Cuadro 5, base 2013=100)", -0.3, 0.3),
        ("2022 (variación anual, Cuadro 5, base 2013=100)", 2.6, 3.9),
        ("Oct 2026 / Oct 2025 (columna notas)", 3.3, 2.6),
    ],
    columns=["momento", "total_%", "alimentos_%"],
)


def cargar_datos(carpeta: Path = PROCESSED):
    """Carga las dos tablas y agrega columnas anio y mes desde `fecha`."""
    ipc = pd.read_csv(carpeta / "ipc.csv", parse_dates=["fecha"])
    costo = pd.read_csv(carpeta / "costo_canasta_mensual.csv", parse_dates=["fecha"])
    # anio y mes ya vienen en los CSV (esquemas.py); se verifica por seguridad.
    for nombre, df in (("ipc", ipc), ("costo_canasta_mensual", costo)):
        faltan = {"anio", "mes", "fecha"} - set(df.columns)
        if faltan:
            raise ValueError(f"{nombre}.csv: faltan columnas {sorted(faltan)}")
    return ipc, costo


def consultar_ipc(ipc: pd.DataFrame, anio: int, mes: int, grupo: str = "total"):
    """Devuelve el índice del mes. Nunca mezcla bases distintas."""
    f = ipc[(ipc["anio"] == anio) & (ipc["mes"] == mes) & (ipc["grupo"] == GRUPOS[grupo])]
    return f[["fecha", "grupo", "base", "geografia", "indice", "notas"]]


def consultar_costo(costo: pd.DataFrame, anio: int, mes: int, fuente: str | None = None):
    """Devuelve el costo_total de la canasta. Cada fuente va por separado."""
    f = costo[(costo["anio"] == anio) & (costo["mes"] == mes)]
    if fuente:
        f = f[f["fuente"] == FUENTES[fuente]]
    return f[["fecha", "fuente", "geografia", "costo_total", "n_productos"]]


def variacion_costo(costo: pd.DataFrame, mes: int, fuente: str, anio_ini: int, anio_fin: int):
    """Variación % del costo entre el mismo mes de dos años (misma fuente)."""
    f = costo[(costo["fuente"] == FUENTES[fuente]) & (costo["mes"] == mes)]
    v = f.set_index("anio")["costo_total"]
    if anio_ini not in v.index or anio_fin not in v.index:
        return None
    return (v[anio_fin] / v[anio_ini] - 1) * 100


# ----------------------------- interfaz de texto -----------------------------

def _pedir_fecha():
    anio = int(input("Año (2019, 2022, 2025, 2026): "))
    mes = int(input("Mes (1-12): "))
    if mes not in MESES:
        raise ValueError("Mes inválido")
    return anio, mes


def _mostrar_ipc(ipc):
    anio, mes = _pedir_fecha()
    g = input("Grupo [total/alimentos]: ").strip().lower() or "total"
    if g not in GRUPOS:
        print("Grupo inválido.")
        return
    r = consultar_ipc(ipc, anio, mes, g)
    if r.empty:
        print(f"Sin datos de IPC para {MESES[mes]} {anio}.")
        return
    for _, fila in r.iterrows():
        print(f"IPC {g} {MESES[mes]} {anio}: {fila['indice']} "
              f"(base {fila['base']}, {fila['geografia']})")
        if pd.notna(fila["notas"]):
            print(f"  Nota INEC: {fila['notas']}")


def _mostrar_costo(costo):
    anio, mes = _pedir_fecha()
    fu = input("Fuente [acodeco/mef/ambas]: ").strip().lower() or "ambas"
    fuente = None if fu == "ambas" else fu
    if fuente and fuente not in FUENTES:
        print("Fuente inválida.")
        return
    r = consultar_costo(costo, anio, mes, fuente)
    if r.empty:
        print(f"Sin costo publicado para {MESES[mes]} {anio} "
              "(ej.: el MEF no publicó agosto de 2022; no se interpola).")
        return
    for _, fila in r.iterrows():
        print(f"{fila['fuente']}: B/. {fila['costo_total']:.2f} "
              f"({fila['n_productos']} productos, {fila['geografia']})")


def _mostrar_variacion(costo):
    mes = int(input("Mes a comparar (1-12): "))
    fu = input("Fuente [acodeco/mef]: ").strip().lower() or "acodeco"
    a0 = int(input("Año inicial: "))
    a1 = int(input("Año final: "))
    if fu not in FUENTES:
        print("Fuente inválida.")
        return
    v = variacion_costo(costo, mes, fu, a0, a1)
    if v is None:
        print("No hay datos de ese mes en uno de los dos años.")
    else:
        print(f"Costo {fu}, {MESES[mes]} {a0} → {a1}: {v:+.1f} %")


def main():
    ipc, costo = cargar_datos()
    acciones = {
        "1": ("Consultar IPC", lambda: _mostrar_ipc(ipc)),
        "2": ("Consultar costo de la canasta", lambda: _mostrar_costo(costo)),
        "3": ("Variación del costo (mismo mes, dos años)", lambda: _mostrar_variacion(costo)),
        "4": ("Inflación oficial INEC (2019, 2022, oct 2026)",
              lambda: print(INFLACION_OFICIAL.to_string(index=False))),
    }
    while True:
        print("\n--- IPC y costo de la canasta ---")
        for k, (txt, _) in acciones.items():
            print(f"{k}. {txt}")
        print("0. Salir")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op in acciones:
            try:
                acciones[op][1]()
            except ValueError as e:
                print(f"Entrada inválida: {e}")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
