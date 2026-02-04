import requests
import pandas as pd
import time

def obtener_datos_masivos():
    data_list = []
    # Límite de seguridad: Escanearemos solo los primeros 50 animes para probar.
    # Si funciona bien, puedes aumentar 'pages_to_scan' a 5 o 10.
    pages_to_scan = 2 
    
    print(f"🚀 Iniciando recolección. Se escanearán {pages_to_scan} páginas del Top Anime...")

    for page in range(1, pages_to_scan + 1): 
        print(f"\n--- Procesando Página {page} ---")
        try:
            url = f"https://api.jikan.moe/v4/top/anime?page={page}&filter=bypopularity"
            response = requests.get(url)
            
            if response.status_code == 429:
                print("⚠️ Límite de velocidad alcanzado. Pausando 10 segundos...")
                time.sleep(10)
                continue
            
            if response.status_code != 200:
                print(f"❌ Error en API (Código {response.status_code}). Saltando página.")
                continue
                
            animes = response.json()['data']
        except Exception as e:
            print(f"Error de conexión: {e}")
            continue
        
        for anime in animes:
            # FILTRO 1: Solo animes basados en Manga
            # Usamos .get() para evitar errores si el campo no existe
            source = anime.get('source', '')
            if source != 'Manga':
                continue
            
            # FILTRO 2: Solo terminados
            if anime.get('status') != 'Finished Airing':
                continue

            anime_id = anime['mal_id']
            anime_title = anime['title']
            
            # --- PASO CRÍTICO: Obtener detalles completos para ver relaciones ---
            # La lista "Top" no tiene relations, hay que pedirla individualmente.
            try:
                # Pausa OBLIGATORIA para no ser baneado (Rate Limit)
                time.sleep(1.5) 
                
                # Pedimos las relaciones específicas de ESTE anime
                url_rel = f"https://api.jikan.moe/v4/anime/{anime_id}/relations"
                r_rel = requests.get(url_rel)
                
                if r_rel.status_code != 200:
                    continue
                    
                relations_data = r_rel.json()['data']
                
                manga_chapters = None
                
                # Buscamos en las relaciones dónde está el "Adaptation" -> "manga"
                for relation in relations_data:
                    if relation['relation'] == 'Adaptation':
                        for entry in relation['entry']:
                            if entry['type'] == 'manga':
                                manga_id = entry['mal_id']
                                
                                # --- PASO FINAL: Consultar cuántos caps tiene ese manga ---
                                time.sleep(1.5) # Otra pausa de seguridad
                                r_manga = requests.get(f"https://api.jikan.moe/v4/manga/{manga_id}")
                                
                                if r_manga.status_code == 200:
                                    manga_data = r_manga.json()['data']
                                    # Verificamos que el manga esté terminado y tenga dato de capítulos
                                    if manga_data.get('status') == 'Finished' and manga_data.get('chapters'):
                                        manga_chapters = manga_data['chapters']
                                        
                                        # ¡ÉXITO! Guardamos todo
                                        print(f"✅ {anime_title}: {anime['episodes']} eps <-> {manga_chapters} caps")
                                        
                                        # Guardamos el estudio principal (si existe)
                                        studios = anime.get('studios', [])
                                        studio_name = studios[0]['name'] if studios else 'Desconocido'
                                        
                                        # Guardamos género principal
                                        genres = anime.get('genres', [])
                                        genre_name = genres[0]['name'] if genres else 'General'

                                        data_list.append({
                                            'Nombre': anime_title,
                                            'Caps_Manga': manga_chapters,
                                            'Caps_Anime': anime['episodes'],
                                            'Year': anime.get('year', 2000),
                                            'Studio': studio_name,
                                            'Genero': genre_name
                                        })
                                break # Ya encontramos el manga, rompemos el bucle interno
                
                if manga_chapters:
                    pass # Ya se guardó arriba
                    
            except Exception as e:
                print(f"Error procesando {anime_title}: {e}")
                continue

    return pd.DataFrame(data_list)

# EJECUCIÓN
if __name__ == "__main__":
    df_nuevo = obtener_datos_masivos()
    if not df_nuevo.empty:
        df_nuevo.to_csv('dataset_anime_bigdata_v2.csv', index=False)
        print(f"\n🎉 ¡Éxito! Se recolectaron {len(df_nuevo)} animes nuevos en 'dataset_anime_bigdata_v2.csv'")
    else:
        print("\nNo se encontraron datos. Intenta más tarde o revisa tu conexión.")