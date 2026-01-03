import pandas as pd

# Leer el archivo Excel
df_modulos = pd.read_excel('propuesta_importacion_completa.xlsx', sheet_name='Módulos')

print(f"Total módulos: {len(df_modulos)}")
print(f"\nColumnas: {df_modulos.columns.tolist()}")
print(f"\nPrimeros 5 módulos:")
print(df_modulos.head(5))
print(f"\nÚltimos 3 módulos:")
print(df_modulos.tail(3))
