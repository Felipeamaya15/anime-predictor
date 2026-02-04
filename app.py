import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Anime Predictor Pro", page_icon="📈", layout="centered")

st.title("📈 Anime Production AI")
st.markdown("Herramienta de estimación de episodios basada en **Deep Learning**.")
st.markdown("---")

# 1. CARGAR RECURSOS (MODELO V2 Y METADATA)
@st.cache_resource
def load_resources():
    # Cargamos el cerebro actualizado
    model = tf.keras.models.load_model('anime_predictor_v2.keras')
    
    # Cargamos la lista de columnas y la lista de estudios permitidos
    # (El orden de carga debe ser el mismo en el que guardamos en entrenar.py)
    with open('columnas_v2.pkl', 'rb') as f:
        cols_modelo = pickle.load(f)
        top_studios = pickle.load(f)
        
    return model, cols_modelo, top_studios

# Intentamos cargar. Si falla, mostramos error amigable.
try:
    model, columnas_modelo, top_studios_list = load_resources()
except FileNotFoundError:
    st.error("⚠️ No encuentro los archivos 'v2'. Asegúrate de haber ejecutado el nuevo entrenar.py")
    st.stop()

# 2. BARRA LATERAL (INPUTS DEL USUARIO)
st.sidebar.header("⚙️ Parámetros del Proyecto")

# A) Datos del Manga
caps_manga = st.sidebar.number_input("Capítulos del Manga", min_value=10, max_value=2000, value=150)
genero = st.sidebar.selectbox("Género Principal", 
                              ["Shonen", "Seinen", "Deportes", "Comedia", "Thriller", "Romance", "Drama", "Accion"])

# B) Datos de Producción (NUEVO)
st.sidebar.markdown("---")
anio_estreno = st.sidebar.slider("Año estimado de estreno", 1980, 2030, 2024)

# Selector de Estudio Inteligente (Usa la lista que guardamos en el pickle)
# Agregamos 'Otros' por si el usuario quiere probar algo genérico
opciones_estudios = sorted(top_studios_list) + ['Otros']
estudio = st.sidebar.selectbox("Estudio de Animación", opciones_estudios)

# 3. PROCESAMIENTO DE DATOS (EL CEREBRO DE INGENIERÍA)

# A) Calcular Década (Feature Engineering en tiempo real)
decada = (anio_estreno // 10) * 10

# B) Crear DataFrame base con los datos del usuario
input_data = pd.DataFrame({
    'Caps_Manga': [caps_manga],
    'Genero': [genero],
    'Studio_Clean': [estudio],
    'Decada': [decada]
})

# C) Convertir a One-Hot (Gen_X, Std_X, Dec_X)
# Usamos los mismos prefijos que en el entrenamiento
input_data = pd.get_dummies(input_data, columns=['Genero', 'Studio_Clean', 'Decada'], 
                            prefix=['Gen', 'Std', 'Dec'])

# D) ALINEACIÓN DE COLUMNAS (CRÍTICO)
# Creamos una plantilla vacía con TODAS las columnas que el modelo espera
df_final = pd.DataFrame(columns=columnas_modelo)
df_final.loc[0] = 0 # Llenamos todo con ceros inicialmente

# Rellenamos solo las columnas que coinciden
for col in input_data.columns:
    if col in df_final.columns:
        df_final.loc[0, col] = input_data.iloc[0][col]
    
    # Aseguramos que la columna numérica principal pase siempre
    if col == 'Caps_Manga':
        df_final.loc[0, 'Caps_Manga'] = input_data.iloc[0]['Caps_Manga']

# Convertir a matriz NumPy
X_pred = np.array(df_final).astype('float32')

# 4. PREDICCIÓN Y RESULTADOS
if st.button("Calcular Estimación", type="primary"):
    
    # Predecir
    prediccion = model.predict(X_pred)
    resultado = float(prediccion[0][0])
    
    # Evitar números negativos
    resultado = max(0, resultado)
    
    # --- MOSTRAR RESULTADOS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Episodios Estimados")
        st.metric(label="Total", value=f"{int(resultado)}")
    
    with col2:
        ratio = caps_manga / resultado if resultado > 0 else 0
        st.subheader("Ritmo de Adaptación")
        st.metric(label="Caps Manga / Episodio", value=f"{ratio:.2f}")

    # Análisis contextual
    st.info(f"📊 Análisis: Un anime de **{genero}** producido por **{estudio}** en los **{decada}s** suele tener este comportamiento.")

    # Advertencias de negocio
    if estudio == "Toei Animation" and ratio < 1.5:
        st.warning("⚠️ Nota: Toei suele agregar contenido original (relleno), por lo que el número de episodios podría ser aún mayor.")
    elif estudio == "MAPPA" or estudio == "Madhouse":
        st.success("✅ Nota: Estos estudios suelen tener ritmos rápidos y fieles al manga.")