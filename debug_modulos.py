"""
Script para debuggear la importación de módulos
"""
from data_import import DataImporter
from database import SistemaDAO
import pandas as pd

dao = SistemaDAO()
importer = DataImporter(dao)

# Leer módulos del Excel
df_modulos = pd.read_excel('propuesta_importacion_completa.xlsx', sheet_name='Módulos')
print(f"Total módulos en Excel: {len(df_modulos)}")

# Verificar carreras en BD
carreras = dao.obtener_carreras()
print(f"\nCarreras en BD: {len(carreras)}")
for c in carreras:
    print(f"  ID: {c['id']}, Nombre: {c['nombre']}")

# Intentar validar el primer módulo
if len(df_modulos) > 0:
    primer_modulo = df_modulos.iloc[0].to_dict()
    print(f"\nPrimer módulo del Excel:")
    for key, value in primer_modulo.items():
        print(f"  {key}: {value}")
    
    valido, mensaje = importer.validar_modulo(primer_modulo)
    print(f"\n¿Es válido? {valido}")
    if not valido:
        print(f"Error: {mensaje}")
