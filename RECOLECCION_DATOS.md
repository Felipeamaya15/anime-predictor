# Recolección de datos para Anime Predictor

Para **aumentar la precisión del modelo** se añadió un flujo que recolecta muchos más datos desde la API de MyAnimeList (Jikan) y los fusiona con tu dataset manual.

## Flujo recomendado

### 1. Dataset manual (base curada)
```bash
python generar_dataset.py
```
Genera `dataset_manual.csv` y `dataset_anime_final.csv` con la lista curada de animes.

### 2. Recolectar datos de la API (muchos más registros)
```bash
python recolector_mejorado.py --modo completo
```
- **`--modo rapido`**: solo ~10 páginas del top (pruebas rápidas).
- **`--modo completo`**: top 20 páginas + temporadas 2018–2024 (recomendado).
- **`--modo maximo`**: top 30 páginas + temporadas 2010–2024 (máximo volumen, tarda más).

Salida: `dataset_recolectado_api.csv` (o `--salida otro_nombre.csv`).

La API tiene límite de peticiones; el script hace pausas automáticas. Un modo `completo` puede tardar **varios minutos**.

### 3. Fusionar manual + API
```bash
python fusionar_datasets.py
```
Genera `dataset_anime_final.csv` uniendo:
- tu dataset manual (`dataset_manual.csv` o `dataset_anime_final.csv`),
- y el recolectado (`dataset_recolectado_api.csv`),
eliminando duplicados.

### 4. Entrenar y usar la app
```bash
python entrenar.py
streamlit run app.py
```

## Archivos nuevos

| Archivo | Descripción |
|--------|-------------|
| `config_recolector.py` | Mapeo de géneros MAL → modelo (Shonen, Seinen, etc.). |
| `recolector_mejorado.py` | Recolector que usa top + temporadas y filtro de ratio. |
| `fusionar_datasets.py` | Fusiona manual + API en `dataset_anime_final.csv`. |
| `dataset_manual.csv` | Generado por `generar_dataset.py` (base curada). |
| `dataset_recolectado_api.csv` | Generado por `recolector_mejorado.py`. |

## Filtros de calidad (recolector)

- Solo animes con **origen Manga** y **Finished Airing**.
- Se obtienen los **capítulos del manga** vía relaciones (Adaptation).
- Se descartan ratios incoherentes: **ratio = caps_manga / episodios** debe estar entre **1.0 y 4.5** (evita temporadas parciales o relleno masivo).
- Los géneros de MAL se mapean a los 8 del modelo: Shonen, Seinen, Deportes, Comedia, Thriller, Romance, Drama, Accion.

## Si la API devuelve 429 (rate limit)

El script hace pausas de 15 s y reintenta. Si sigues teniendo límite, ejecuta en **modo rapido** o deja pasar unos minutos y vuelve a lanzar.
