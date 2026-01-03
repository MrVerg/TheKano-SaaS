"""
Script para importar datos desde el archivo Excel generado por IMPORT.py
"""
from data_import import DataImporter
from database import SistemaDAO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("🚀 Iniciando importación de datos desde Excel...")
    
    dao = SistemaDAO()
    importer = DataImporter(dao)
    
    archivo_excel = "propuesta_importacion_completa.xlsx"
    
    try:
        resultados = importer.importar_desde_excel(archivo_excel, limpiar_existentes=False)
        
        print("\n✅ Importación completada")
        print("\n📊 Resumen:")
        for tabla, count in resultados.items():
            print(f"  • {tabla}: {count} registros")
        
        if importer.errores:
            print(f"\n⚠️  Se encontraron {len(importer.errores)} errores:")
            for i, error in enumerate(importer.errores[:10], 1):
                print(f"  {i}. {error}")
            if len(importer.errores) > 10:
                print(f"  ... y {len(importer.errores) - 10} errores más")
        else:
            print("\n✅ No se encontraron errores")
            
    except Exception as e:
        print(f"\n❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
