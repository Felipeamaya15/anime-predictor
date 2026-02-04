import pandas as pd
import tensorflow as tf
import numpy as np

# --- PASO 1: Cargar datos con Pandas ---
df = pd.read_csv('casas.csv')

print("Datos originales:")
print(df.head())

# --- PASO 2: Preprocesamiento (CORREGIDO) ---
df = pd.get_dummies(df, columns=['Barrio'], prefix='', prefix_sep='')

# Separamos X e y
X_pandas = df.drop('Precio', axis=1)
y_pandas = df['Precio']

# AQUÍ ESTÁ EL CAMBIO: Convertimos explícitamente a arreglos de NumPy
X = np.array(X_pandas).astype('float32')
y = np.array(y_pandas).astype('float32')

# --- PASO 3: Crear el Modelo de Regresión ---
model = tf.keras.Sequential([
    # Capa de normalización (ajusta la escala de los datos automáticamente)
    tf.keras.layers.Normalization(axis=-1),
    # Capa oculta con 64 neuronas
    tf.keras.layers.Dense(64, activation='relu'),
    # Otra capa oculta
    tf.keras.layers.Dense(64, activation='relu'),
    # Capa de salida: 1 sola neurona porque queremos predecir 1 solo valor (el precio)
    tf.keras.layers.Dense(1)
])

# Paso extra: Configurar la normalización con nuestros datos X
normalizer = model.layers[0]
normalizer.adapt(X)

# --- PASO 4: Compilar y Entrenar ---
# Usamos 'mae' (Mean Absolute Error) para saber cuántos $$ nos equivocamos en promedio
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
              loss='mean_absolute_error')

print("\nEntrenando...")
history = model.fit(X, y, epochs=100, verbose=0) # verbose=0 para que no llene la pantalla
print("Entrenamiento finalizado.")

# --- PASO 5: Probar una predicción ---
# Vamos a predecir una casa de: 120m2, 3 hab, 2 baños, 15 años, Barrio Norte
# Nota: Debes ingresar los datos en el mismo orden que quedaron las columnas de X
# (Imprime X.columns para ver el orden exacto si tienes dudas)
casa_ejemplo = np.array([[120, 3, 2, 15, 0, 1, 0, 0]]) # El 1 está en la posición de 'Norte'

prediccion = model.predict(casa_ejemplo)
print(f"\nPrecio Real esperado (aprox): 210000")
print(f"Predicción de la IA: {prediccion[0][0]:.2f}")