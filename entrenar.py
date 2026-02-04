import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import pickle

# 1. CARGAR DATOS
# Asegúrate de usar el CSV que generó el script recolector masivo
archivo_csv = 'dataset_anime_final.csv' 
print(f"Cargando dataset: {archivo_csv}...")

try:
    df = pd.read_csv(archivo_csv)
except FileNotFoundError:
    print("❌ Error: No encuentro el archivo 'dataset_anime_bigdata.csv'.")
    print("Asegúrate de haber corrido primero el script 'recolector_masivo.py'")
    exit()

# 2. INGENIERÍA DE CARACTERÍSTICAS (CREAR COLUMNAS INTELIGENTES)

# A) DECADA: Convertimos 2014 -> 2010, 1999 -> 1990
# Esto ayuda a la IA a ver tendencias generacionales
df['Decada'] = (df['Year'] // 10) * 10

# B) LIMPIEZA DE ESTUDIOS (REDUCCIÓN DE DIMENSIONALIDAD)
# Hay demasiados estudios pequeños. Vamos a quedarnos con los Top 20 más frecuentes
# y al resto los llamaremos "Otros". Esto mejora mucho el rendimiento.
top_studios = df['Studio'].value_counts().nlargest(20).index
df['Studio_Clean'] = df['Studio'].apply(lambda x: x if x in top_studios else 'Otros')

print("Top 5 Estudios en tu data:", list(top_studios[:5]))

# 3. SELECCIÓN DE COLUMNAS
# Ahora usamos: Caps_Manga, Decada, Genero y el Estudio Limpio
X = df[['Caps_Manga', 'Decada', 'Genero', 'Studio_Clean']]
y = df['Caps_Anime']

# 4. CONVERTIR TEXTO A NÚMEROS (ONE-HOT ENCODING)
# Esto creará columnas como: "Studio_Clean_MAPPA", "Decada_2010", etc.
X = pd.get_dummies(X, columns=['Genero', 'Studio_Clean', 'Decada'], prefix=['Gen', 'Std', 'Dec'])

# Guardamos los nombres de las columnas para la App (CRÍTICO)
columnas_entrenamiento = X.columns.tolist()
print(f"Dimensiones de entrada: {len(columnas_entrenamiento)} columnas.")

# 5. SPLIT (ENTRENAMIENTO VS PRUEBA)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convertir a float32
X_train = np.array(X_train).astype('float32')
y_train = np.array(y_train).astype('float32')
X_test = np.array(X_test).astype('float32')
y_test = np.array(y_test).astype('float32')

# 6. ARQUITECTURA DEL MODELO MEJORADA
# Como ahora tenemos más columnas (por los estudios), aumentamos un poco la capacidad
model = tf.keras.Sequential([
    layers.Normalization(axis=-1),
    layers.Dense(128, activation='relu'), # Aumentamos neuronas (64 -> 128)
    layers.Dropout(0.2), # Apaga el 20% de neuronas al azar para evitar memorización
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
])

# Configurar normalización
model.layers[0].adapt(X_train)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
              loss='mean_absolute_error')

# 7. ENTRENAR
print("Entrenando IA con datos de estudios y décadas...")
history = model.fit(X_train, y_train, epochs=250, verbose=0, validation_data=(X_test, y_test))

# 8. EVALUAR
loss = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ Entrenamiento finalizado.")
print(f"Error promedio del modelo: +/- {loss:.1f} episodios")

# 9. GUARDAR
model.save('anime_predictor_v2.keras')
with open('columnas_v2.pkl', 'wb') as f:
    pickle.dump(columnas_entrenamiento, f)
    # También guardamos la lista de Top Studios para que la App sepa cuáles mostrar
    pickle.dump(list(top_studios), f)

print("Archivos guardados: 'anime_predictor_v2.keras' y 'columnas_v2.pkl'")
# Calcular el porcentaje de error promedio (MAPE)
y_pred = model.predict(X_test)
mape = np.mean(np.abs((y_test - y_pred.flatten()) / y_test)) * 100

print(f"📊 Margen de error promedio del modelo: {mape:.2f}%")