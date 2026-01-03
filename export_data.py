import json
import logging
from database import SistemaDAO
import datetime
import decimal

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, datetime.timedelta):
            return str(obj)
        return super().default(obj)

def export_data():
    dao = SistemaDAO()
    data = {}
    
    tables = [
        'salas', 
        'carreras', 
        'docentes', 
        'modulos', 
        'carrera_semestres', 
        'carrera_salas', 
        'disponibilidad_docentes', 
        'modulo_horarios'
    ]
    
    logging.info("Exporting data from database...")
    
    for table in tables:
        try:
            rows = dao.db.execute_query(f"SELECT * FROM {table}", fetch=True)
            data[table] = rows
            logging.info(f"Exported {len(rows)} rows from {table}")
        except Exception as e:
            logging.error(f"Error exporting {table}: {e}")
            
    with open('initial_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, cls=CustomEncoder, indent=4, ensure_ascii=False)
        
    logging.info("Data export completed to initial_data.json")

if __name__ == "__main__":
    export_data()
