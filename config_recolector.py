# -*- coding: utf-8 -*-
"""
Configuración para el recolector de datos: mapeo de géneros MAL → modelo
y géneros válidos para el predictor.
"""

# Géneros que usa el modelo (deben coincidir con app.py)
GENEROS_MODELO = [
    "Shonen", "Seinen", "Deportes", "Comedia", "Thriller", "Romance", "Drama", "Accion"
]

# Mapeo: nombre de género/demographic en MAL (inglés) → género del modelo
# Demographics en MAL: Shounen, Seinen, Josei, Kids
# Genres en MAL: Action, Adventure, Comedy, Drama, Sports, Romance, etc.
MAPEO_MAL_A_MODELO = {
    # Demographics (prioridad si se usa)
    "Shounen": "Shonen",
    "Seinen": "Seinen",
    "Josei": "Seinen",
    "Kids": "Shonen",
    # Genres
    "Action": "Accion",
    "Adventure": "Shonen",
    "Comedy": "Comedia",
    "Drama": "Drama",
    "Sports": "Deportes",
    "Romance": "Romance",
    "Horror": "Thriller",
    "Mystery": "Thriller",
    "Suspense": "Thriller",
    "Thriller": "Thriller",
    "Sci-Fi": "Seinen",
    "Fantasy": "Shonen",
    "Supernatural": "Shonen",
    "Slice of Life": "Drama",
    "Avant Garde": "Seinen",
    "Girls Love": "Romance",
    "Boys Love": "Drama",
    "General": "Shonen",
}

def normalizar_genero_mal(genres_list, demographics_list=None):
    """
    Convierte géneros/demographics de la API MAL (Jikan) al género del modelo.
    Prioridad: demographic Seinen/Shounen > primer género mapeado.
    """
    # Preferir demographic si está disponible
    if demographics_list:
        for d in demographics_list:
            name = (d.get("name") or "").strip()
            if name in MAPEO_MAL_A_MODELO:
                return MAPEO_MAL_A_MODELO[name]
    # Sino, usar el primer género de la lista
    if genres_list:
        for g in genres_list:
            name = (g.get("name") or "").strip()
            if name in MAPEO_MAL_A_MODELO:
                return MAPEO_MAL_A_MODELO[name]
    return "Shonen"  # valor por defecto seguro para el modelo
