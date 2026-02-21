# -*- coding: utf-8 -*-
"""
Fusiona el dataset manual (generar_dataset.py) con el recolectado por API
(recolector_mejorado.py) y genera dataset_anime_final.csv listo para entrenar.
"""
import pandas as pd
import os

# Archivos de entrada (manual = curado a mano; recolectado = API Jikan)
MANUAL_CSV = "dataset_manual.csv"
RECOLECTADO_CSV = "dataset_recolectado_api.csv"
# Si no existe dataset_manual.csv, se usa dataset_anime_final.csv como base (solo primera vez)
FALLBACK_MANUAL_CSV = "dataset_anime_final.csv"

SALIDA = "dataset_anime_final.csv"

# Columnas esperadas (mismo orden que entrenar.py / app)
COLUMNAS = ["Nombre", "Caps_Manga", "Caps_Anime", "Year", "Studio", "Genero"]


def cargar_csv(ruta):
    if not os.path.isfile(ruta):
        return None
    df = pd.read_csv(ruta)
    for c in COLUMNAS:
        if c not in df.columns:
            return None
    return df[COLUMNAS]


def fusionar():
    listas = []

    # 1) Dataset manual (curado): dataset_manual.csv o, si no existe, dataset_anime_final.csv
    df_manual = cargar_csv(MANUAL_CSV)
    if df_manual is None:
        df_manual = cargar_csv(FALLBACK_MANUAL_CSV)
        if df_manual is not None:
            print("   (Usando dataset_anime_final.csv como base manual. Ejecuta generar_dataset.py para crear dataset_manual.csv)")
    if df_manual is not None:
        listas.append(df_manual)

    # 2) Recolectado por API
    df_api = cargar_csv(RECOLECTADO_CSV)
    if df_api is not None:
        listas.append(df_api)

    if not listas:
        print("❌ No hay ningún dataset válido.")
        print("   Ejecuta primero: python generar_dataset.py")
        print("   Luego (opcional): python recolector_mejorado.py --modo completo")
        return

    df = pd.concat(listas, ignore_index=True)

    # Quitar duplicados (misma combinación clave)
    clave = ["Nombre", "Caps_Manga", "Caps_Anime", "Year", "Studio"]
    antes = len(df)
    df = df.drop_duplicates(subset=clave, keep="first")
    df = df.reset_index(drop=True)

    # Ordenar por año y nombre
    df = df.sort_values(["Year", "Nombre"]).reset_index(drop=True)

    df.to_csv(SALIDA, index=False)
    print(f"✅ Dataset fusionado guardado en '{SALIDA}'")
    print(f"   Total de registros: {len(df)} (se eliminaron {antes - len(df)} duplicados)")
    print(f"   Géneros: {sorted(df['Genero'].unique().tolist())}")
    print(f"   Estudios (muestra): {df['Studio'].value_counts().head(8).to_dict()}")


if __name__ == "__main__":
    fusionar()
