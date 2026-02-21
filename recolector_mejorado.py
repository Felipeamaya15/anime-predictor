# -*- coding: utf-8 -*-
"""
Recolector mejorado: obtiene muchos más datos de la API Jikan (MyAnimeList)
para entrenar un modelo más preciso. Combina varias fuentes y filtra por calidad.
"""
import requests
import pandas as pd
import time
import argparse
from config_recolector import normalizar_genero_mal, GENEROS_MODELO

# Límites de ratio caps_manga / episodios para considerar el dato "coherente"
# Evita temporadas parciales (ratio muy alto) o relleno masivo (ratio muy bajo)
RATIO_MIN = 1.0
RATIO_MAX = 4.5

# Pausa entre requests (segundos) para respetar rate limit de Jikan (3 req/s recomendado 1)
PAUSA_REQUEST = 1.3
PAUSA_429 = 15


def _get(url, session=None):
    s = session or requests
    try:
        r = s.get(url, timeout=15)
        if r.status_code == 429:
            return None, 429
        if r.status_code != 200:
            return None, r.status_code
        return r.json(), 200
    except Exception as e:
        return None, str(e)


def obtener_anime_desde_top(pages_to_scan, data_list, ids_vistos, session):
    """Obtiene anime desde /v4/top/anime por popularidad."""
    for page in range(1, pages_to_scan + 1):
        print(f"   Top anime - página {page}/{pages_to_scan} (registros: {len(data_list)})")
        time.sleep(PAUSA_REQUEST)
        data, code = _get(
            f"https://api.jikan.moe/v4/top/anime?page={page}&filter=bypopularity",
            session,
        )
        if code == 429:
            print("⚠️ Rate limit (429). Pausando", PAUSA_429, "s...")
            time.sleep(PAUSA_429)
            page -= 1
            continue
        if not data or "data" not in data:
            continue
        for anime in data["data"]:
            if anime.get("mal_id") in ids_vistos:
                continue
            item = procesar_anime(anime, session)
            if item:
                data_list.append(item)
                ids_vistos.add(anime["mal_id"])
    return data_list, ids_vistos


def obtener_anime_desde_temporadas(anios, paginas_por_temporada, data_list, ids_vistos, session):
    """Obtiene anime por temporada (winter, spring, summer, fall) para más variedad."""
    seasons = ["winter", "spring", "summer", "fall"]
    for year in anios:
        for season in seasons:
            for page in range(1, paginas_por_temporada + 1):
                time.sleep(PAUSA_REQUEST)
                url = f"https://api.jikan.moe/v4/seasons/{year}/{season}?page={page}"
                data, code = _get(url, session)
                if code == 429:
                    print("⚠️ Rate limit (429). Pausando", PAUSA_429, "s...")
                    time.sleep(PAUSA_429)
                    continue
                if not data or "data" not in data:
                    continue
                for anime in data["data"]:
                    if anime.get("mal_id") in ids_vistos:
                        continue
                    item = procesar_anime(anime, session, year_temporada=year)
                    if item:
                        data_list.append(item)
                        ids_vistos.add(anime["mal_id"])
            print(f"   Temporadas {year} {season} (total: {len(data_list)})")
    return data_list, ids_vistos


def procesar_anime(anime, session, year_temporada=None):
    """
    Filtra que sea manga + finished, obtiene capítulos del manga por relations,
    aplica filtro de ratio y devuelve un dict con Nombre, Caps_Manga, Caps_Anime, Year, Studio, Genero.
    year_temporada: año de la temporada (usado cuando se llama desde el endpoint de temporadas).
    """
    if anime.get("source") != "Manga":
        return None
    if anime.get("status") != "Finished Airing":
        return None

    episodes = anime.get("episodes")
    if not episodes or episodes < 1:
        return None

    title = (anime.get("title") or "").lower()
    if "season" in title and ("2nd" in title or "2 " in title or "part 2" in title):
        return None

    time.sleep(PAUSA_REQUEST)
    data_rel, code = _get(f"https://api.jikan.moe/v4/anime/{anime['mal_id']}/relations", session)
    if code == 429:
        return None
    if not data_rel or "data" not in data_rel:
        return None

    manga_chapters = None
    for relation in data_rel["data"]:
        if relation.get("relation") == "Adaptation":
            for entry in relation.get("entry", []):
                if entry.get("type") == "manga":
                    time.sleep(PAUSA_REQUEST)
                    r_manga, c = _get(f"https://api.jikan.moe/v4/manga/{entry['mal_id']}", session)
                    if c == 429:
                        return None
                    if c == 200 and r_manga and r_manga.get("data", {}).get("status") == "Finished":
                        manga_chapters = r_manga["data"].get("chapters")
                    break
            break

    if not manga_chapters or manga_chapters < 1:
        return None

    ratio = manga_chapters / episodes
    if ratio < RATIO_MIN or ratio > RATIO_MAX:
        return None

    studios = anime.get("studios") or []
    studio_name = studios[0]["name"] if studios else "Otros"
    genres = anime.get("genres") or []
    demographics = anime.get("demographics") or []
    genero = normalizar_genero_mal(genres, demographics)
    year = year_temporada
    if year is None:
        year = anime.get("year")
        if year is None and isinstance(anime.get("aired"), dict):
            from_ = anime["aired"].get("prop", {}).get("from") or anime["aired"].get("from")
            if isinstance(from_, dict) and "year" in from_:
                year = from_["year"]
        year = int(year) if year is not None else 2000
    year = int(year)

    return {
        "Nombre": anime.get("title", "Unknown"),
        "Caps_Manga": manga_chapters,
        "Caps_Anime": episodes,
        "Year": int(year),
        "Studio": studio_name,
        "Genero": genero,
    }


def recolectar(modo="completo", guardar_en="dataset_recolectado_api.csv"):
    """
    modo: 'rapido' (solo top 10 páginas), 'completo' (top 20 + temporadas recientes), 'maximo' (más páginas y años)
    """
    data_list = []
    ids_vistos = set()
    session = requests.Session()

    if modo == "rapido":
        pages_top = 10
        data_list, ids_vistos = obtener_anime_desde_top(pages_top, data_list, ids_vistos, session)
    elif modo == "completo":
        pages_top = 20
        data_list, ids_vistos = obtener_anime_desde_top(pages_top, data_list, ids_vistos, session)
        anios_temporadas = list(range(2018, 2025))  # últimos años
        data_list, ids_vistos = obtener_anime_desde_temporadas(
            anios_temporadas, 1, data_list, ids_vistos, session
        )
    else:  # maximo
        pages_top = 30
        data_list, ids_vistos = obtener_anime_desde_top(pages_top, data_list, ids_vistos, session)
        anios_temporadas = list(range(2010, 2025))
        data_list, ids_vistos = obtener_anime_desde_temporadas(
            anios_temporadas, 2, data_list, ids_vistos, session
        )

    df = pd.DataFrame(data_list)
    if not df.empty:
        df = df.drop_duplicates(subset=["Nombre", "Caps_Manga", "Caps_Anime", "Year", "Studio"], keep="first")
        df.to_csv(guardar_en, index=False)
        print(f"✅ Guardados {len(df)} registros en '{guardar_en}'")
    else:
        print("No se recolectaron registros. Revisa conexión o rate limit.")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recolector mejorado de datos MAL para Anime Predictor")
    parser.add_argument(
        "--modo",
        choices=["rapido", "completo", "maximo"],
        default="completo",
        help="rapido= solo top 10 páginas; completo= top 20 + temporadas 2018-2024; maximo= más páginas y años",
    )
    parser.add_argument(
        "--salida",
        default="dataset_recolectado_api.csv",
        help="Archivo CSV de salida",
    )
    args = parser.parse_args()

    print(f"🚀 Recolector mejorado - Modo: {args.modo}")
    print("   Fuentes: Top anime (popularidad) + temporadas por año")
    print("   Filtros: source=Manga, Finished Airing, ratio caps/episodios entre", RATIO_MIN, "y", RATIO_MAX)
    print("   Esto puede tardar varios minutos por el rate limit de la API.\n")

    recolectar(modo=args.modo, guardar_en=args.salida)
