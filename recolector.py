import requests
import pandas as pd
import time

def obtener_datos_limpios():
    data_list = []
    # Aumentamos las páginas para compensar que ahora descartaremos muchos datos "malos"
    pages_to_scan = 5 
    
    print(f"🚀 Iniciando recolección INTELIGENTE ({pages_to_scan} páginas)...")
    print("---------------------------------------------------------------")

    for page in range(1, pages_to_scan + 1): 
        try:
            url = f"https://api.jikan.moe/v4/top/anime?page={page}&filter=bypopularity"
            response = requests.get(url)
            if response.status_code != 200: continue
            animes = response.json()['data']
        except:
            continue
        
        for anime in animes:
            # FILTRO BÁSICO
            if anime.get('source') != 'Manga' or anime.get('status') != 'Finished Airing':
                continue
            
            anime_eps = anime['episodes']
            if not anime_eps or anime_eps < 1: continue # Evitar división por cero

            # FILTRO DE TÍTULO (Opcional pero útil)
            # Si dice "Season 2", "Part 2", etc., suele ser problemático.
            # Lo saltamos para priorizar historias completas o primeras temporadas.
            title = anime['title'].lower()
            if 'season' in title or '2nd' in title or 'part 2' in title:
                print(f"⚠️ Saltando secuela: {anime['title']}")
                continue

            # --- BUSCAR RELACIONES ---
            try:
                time.sleep(1.2) # Pausa anti-ban
                url_rel = f"https://api.jikan.moe/v4/anime/{anime['mal_id']}/relations"
                r_rel = requests.get(url_rel)
                if r_rel.status_code != 200: continue
                
                manga_chapters = None
                
                for relation in r_rel.json()['data']:
                    if relation['relation'] == 'Adaptation':
                        for entry in relation['entry']:
                            if entry['type'] == 'manga':
                                time.sleep(1.2)
                                r_manga = requests.get(f"https://api.jikan.moe/v4/manga/{entry['mal_id']}")
                                if r_manga.status_code == 200:
                                    manga_data = r_manga.json()['data']
                                    if manga_data.get('status') == 'Finished':
                                        manga_chapters = manga_data.get('chapters')
                                break 
                
                # --- AQUÍ ESTÁ LA MAGIA: EL FILTRO MATEMÁTICO ---
                if manga_chapters and manga_chapters > 0:
                    
                    ratio = manga_chapters / anime_eps
                    
                    # REGLA DE ORO: 
                    # Si el ratio es > 5 (ej: 432 caps / 13 eps = 33), es un error de "Temporada vs Manga Completo".
                    # Si el ratio es < 0.8 (ej: 20 caps / 100 eps), es puro relleno masivo.
                    
                    if 1.2 <= ratio <= 3.8:
                        print(f"✅ GUARDADO: {anime['title']}")
                        print(f"   Datos: {manga_chapters} caps / {anime_eps} eps (Ratio: {ratio:.2f})")
                        
                        studios = anime.get('studios', [])
                        
                        data_list.append({
                            'Nombre': anime['title'],
                            'Caps_Manga': manga_chapters,
                            'Caps_Anime': anime_eps,
                            'Year': anime.get('year', 2000),
                            'Studio': studios[0]['name'] if studios else 'Otros',
                            'Genero': anime['genres'][0]['name'] if anime['genres'] else 'General'
                        })
                    else:
                        print(f"❌ DESCARTADO (Incoherente): {anime['title']}")
                        print(f"   La API dice: {manga_chapters} caps para {anime_eps} eps. (Ratio {ratio:.1f} es imposible)")

            except Exception as e:
                pass

    return pd.DataFrame(data_list)

# EJECUCIÓN
if __name__ == "__main__":
    df_smart = obtener_datos_limpios()
    df_smart.to_csv('dataset_anime_filtrado.csv', index=False)
    print(f"\n✨ Dataset final generado con {len(df_smart)} animes de alta calidad.")