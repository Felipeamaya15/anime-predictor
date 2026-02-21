import pandas as pd

# Lista MAESTRA corregida con Estudios Reales
# Estructura: Nombre (fusionado), Caps_Manga, Caps_Anime, Año_Estreno, Estudio, Genero
datos_corregidos = [
    # --- SHONEN DE PELEA (MODERNOS) ---
    {"Nombre": "My Hero Academia S1", "Caps_Manga": 21, "Caps_Anime": 13, "Year": 2016, "Studio": "Bones", "Genero": "Shonen"},
    {"Nombre": "My Hero Academia S2", "Caps_Manga": 49, "Caps_Anime": 25, "Year": 2017, "Studio": "Bones", "Genero": "Shonen"},
    {"Nombre": "My Hero Academia S3", "Caps_Manga": 52, "Caps_Anime": 25, "Year": 2018, "Studio": "Bones", "Genero": "Shonen"},
    {"Nombre": "My Hero Academia S4", "Caps_Manga": 66, "Caps_Anime": 25, "Year": 2019, "Studio": "Bones", "Genero": "Shonen"},
    {"Nombre": "My Hero Academia S5", "Caps_Manga": 68, "Caps_Anime": 25, "Year": 2021, "Studio": "Bones", "Genero": "Shonen"},
    {"Nombre": "Jujutsu Kaisen S1", "Caps_Manga": 63, "Caps_Anime": 24, "Year": 2020, "Studio": "MAPPA", "Genero": "Shonen"},
    {"Nombre": "Jujutsu Kaisen S2", "Caps_Manga": 74, "Caps_Anime": 23, "Year": 2023, "Studio": "MAPPA", "Genero": "Shonen"},
    {"Nombre": "Demon Slayer S1", "Caps_Manga": 54, "Caps_Anime": 26, "Year": 2019, "Studio": "ufotable", "Genero": "Shonen"},
    {"Nombre": "Demon Slayer S2", "Caps_Manga": 43, "Caps_Anime": 18, "Year": 2021, "Studio": "ufotable", "Genero": "Shonen"},
    {"Nombre": "Black Clover", "Caps_Manga": 270, "Caps_Anime": 170, "Year": 2017, "Studio": "Pierrot", "Genero": "Shonen"},
    {"Nombre": "Dr. Stone S1", "Caps_Manga": 60, "Caps_Anime": 24, "Year": 2019, "Studio": "TMS Entertainment", "Genero": "Shonen"},
    {"Nombre": "Fire Force S1", "Caps_Manga": 90, "Caps_Anime": 24, "Year": 2019, "Studio": "David Production", "Genero": "Shonen"},
    {"Nombre": "Chainsaw Man", "Caps_Manga": 38, "Caps_Anime": 12, "Year": 2022, "Studio": "MAPPA", "Genero": "Shonen"},
    {"Nombre": "Hell's Paradise", "Caps_Manga": 44, "Caps_Anime": 13, "Year": 2023, "Studio": "MAPPA", "Genero": "Shonen"},
    {"Nombre": "Mashle S1", "Caps_Manga": 39, "Caps_Anime": 12, "Year": 2023, "Studio": "A-1 Pictures", "Genero": "Comedia"},
    {"Nombre": "Blue Lock", "Caps_Manga": 94, "Caps_Anime": 24, "Year": 2022, "Studio": "8bit", "Genero": "Deportes"},
    {"Nombre": "Kaiju No. 8", "Caps_Manga": 38, "Caps_Anime": 12, "Year": 2024, "Studio": "Production I.G", "Genero": "Shonen"},

    # --- CLÁSICOS Y LARGOS ---
    {"Nombre": "Naruto", "Caps_Manga": 244, "Caps_Anime": 220, "Year": 2002, "Studio": "Pierrot", "Genero": "Shonen"},
    {"Nombre": "Naruto Shippuden", "Caps_Manga": 456, "Caps_Anime": 500, "Year": 2007, "Studio": "Pierrot", "Genero": "Shonen"},
    {"Nombre": "Bleach (Original)", "Caps_Manga": 479, "Caps_Anime": 366, "Year": 2004, "Studio": "Pierrot", "Genero": "Shonen"},
    {"Nombre": "Bleach TYBW P1", "Caps_Manga": 50, "Caps_Anime": 13, "Year": 2022, "Studio": "Pierrot", "Genero": "Shonen"},
    {"Nombre": "One Piece (East Blue)", "Caps_Manga": 100, "Caps_Anime": 61, "Year": 1999, "Studio": "Toei Animation", "Genero": "Shonen"},
    {"Nombre": "Dragon Ball Z Kai", "Caps_Manga": 325, "Caps_Anime": 167, "Year": 2009, "Studio": "Toei Animation", "Genero": "Shonen"},
    {"Nombre": "Fullmetal Alchemist Bro.", "Caps_Manga": 108, "Caps_Anime": 64, "Year": 2009, "Studio": "Bones", "Genero": "Shonen"},
    {"Nombre": "Hunter x Hunter", "Caps_Manga": 339, "Caps_Anime": 148, "Year": 2011, "Studio": "Madhouse", "Genero": "Shonen"},
    {"Nombre": "Gintama S1", "Caps_Manga": 292, "Caps_Anime": 201, "Year": 2006, "Studio": "Sunrise", "Genero": "Comedia"},
    {"Nombre": "Death Note", "Caps_Manga": 108, "Caps_Anime": 37, "Year": 2006, "Studio": "Madhouse", "Genero": "Thriller"},
    {"Nombre": "Fairy Tail S1", "Caps_Manga": 253, "Caps_Anime": 175, "Year": 2009, "Studio": "A-1 Pictures", "Genero": "Shonen"},
    {"Nombre": "Seven Deadly Sins S1", "Caps_Manga": 100, "Caps_Anime": 24, "Year": 2014, "Studio": "A-1 Pictures", "Genero": "Shonen"},

    # --- DEPORTES Y OTROS ---
    {"Nombre": "Haikyuu!! S1", "Caps_Manga": 71, "Caps_Anime": 25, "Year": 2014, "Studio": "Production I.G", "Genero": "Deportes"},
    {"Nombre": "Haikyuu!! S2", "Caps_Manga": 78, "Caps_Anime": 25, "Year": 2015, "Studio": "Production I.G", "Genero": "Deportes"},
    {"Nombre": "Haikyuu!! S3", "Caps_Manga": 37, "Caps_Anime": 10, "Year": 2016, "Studio": "Production I.G", "Genero": "Deportes"},
    {"Nombre": "Haikyuu!! To the Top", "Caps_Manga": 70, "Caps_Anime": 25, "Year": 2020, "Studio": "Production I.G", "Genero": "Deportes"},
    {"Nombre": "Kuroko no Basket S1", "Caps_Manga": 73, "Caps_Anime": 25, "Year": 2012, "Studio": "Production I.G", "Genero": "Deportes"},
    {"Nombre": "Slam Dunk", "Caps_Manga": 197, "Caps_Anime": 101, "Year": 1993, "Studio": "Toei Animation", "Genero": "Deportes"},
    {"Nombre": "Blue Box", "Caps_Manga": 33, "Caps_Anime": 13, "Year": 2024, "Studio": "Telecom", "Genero": "Romance"},

    # --- SEINEN / DRAMA ---
    {"Nombre": "Vinland Saga S1", "Caps_Manga": 54, "Caps_Anime": 24, "Year": 2019, "Studio": "Wit Studio", "Genero": "Seinen"},
    {"Nombre": "Vinland Saga S2", "Caps_Manga": 46, "Caps_Anime": 24, "Year": 2023, "Studio": "MAPPA", "Genero": "Seinen"},
    {"Nombre": "One Punch Man S1", "Caps_Manga": 37, "Caps_Anime": 12, "Year": 2015, "Studio": "Madhouse", "Genero": "Seinen"},
    {"Nombre": "One Punch Man S2", "Caps_Manga": 47, "Caps_Anime": 12, "Year": 2019, "Studio": "J.C.Staff", "Genero": "Seinen"},
    {"Nombre": "Kaguya-sama S1", "Caps_Manga": 46, "Caps_Anime": 12, "Year": 2019, "Studio": "A-1 Pictures", "Genero": "Seinen"},
    {"Nombre": "Oshi no Ko", "Caps_Manga": 40, "Caps_Anime": 11, "Year": 2023, "Studio": "Doga Kobo", "Genero": "Seinen"},
    {"Nombre": "Frieren", "Caps_Manga": 60, "Caps_Anime": 28, "Year": 2023, "Studio": "Madhouse", "Genero": "Shonen"},
    {"Nombre": "Monster", "Caps_Manga": 162, "Caps_Anime": 74, "Year": 2004, "Studio": "Madhouse", "Genero": "Seinen"},
    {"Nombre": "Parasyte", "Caps_Manga": 64, "Caps_Anime": 24, "Year": 2014, "Studio": "Madhouse", "Genero": "Seinen"},
    {"Nombre": "Tokyo Ghoul S1", "Caps_Manga": 66, "Caps_Anime": 12, "Year": 2014, "Studio": "Pierrot", "Genero": "Seinen"},
    {"Nombre": "Mob Psycho 100 S1", "Caps_Manga": 50, "Caps_Anime": 12, "Year": 2016, "Studio": "Bones", "Genero": "Accion"},
    {"Nombre": "Spy x Family S1", "Caps_Manga": 38, "Caps_Anime": 25, "Year": 2022, "Studio": "Wit Studio", "Genero": "Comedia"},
    {"Nombre": "Assassination Classroom S1", "Caps_Manga": 73, "Caps_Anime": 22, "Year": 2015, "Studio": "Lerche", "Genero": "Shonen"},
]

df = pd.DataFrame(datos_corregidos)

# Guardamos el dataset manual (base para fusionar con datos de la API)
archivo_manual = 'dataset_manual.csv'
archivo_salida = 'dataset_anime_final.csv'
df.to_csv(archivo_manual, index=False)
df.to_csv(archivo_salida, index=False)

print(f"✅ ¡Dataset generado con éxito!")
print(f"📄 Archivos: {archivo_manual}, {archivo_salida}")
print(f"📊 Filas: {len(df)}")
print(f"🔍 Ejemplo de Estudios: {df['Studio'].unique()[:5]}")