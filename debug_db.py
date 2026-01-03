import logging
from database import SistemaDAO

# Configure logging
logging.basicConfig(level=logging.INFO)

def debug_modules():
    dao = SistemaDAO()
    try:
        dao.inicializar_base_de_datos()
        modulos = dao.obtener_modulos()
        print(f"Total modules found: {len(modulos)}")
        
        sin_docente = []
        for m in modulos:
            docente_id = m.get('docente_id')
            print(f"Module: {m['nombre']}, Docente ID: {docente_id} (Type: {type(docente_id)})")
            
            # Check the condition used in the app
            if not docente_id:
                sin_docente.append(m)
                
        print(f"Modules without teacher (using 'if not docente_id'): {len(sin_docente)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_modules()
