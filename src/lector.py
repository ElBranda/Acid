import pandas as pd
import os

def get_data_from_excel(path: str) -> pd.DataFrame:
    '''
    Obtiene la data cruda del Excel, devuelve en un DataFrame sin ningún formato específico.
    '''

    if not os.path.exists(path):
        raise IOError(f"No se encontró el archivo en la ruta: {path}")
    
    extension = os.path.splitext(path)[1].lower()

    try:
        engine: str

        if extension == ".xls":
            engine = 'xlrd'
        elif extension == ".xlsx":
            engine = 'openpyxl'
        else:
            raise IOError(f"Formato {extension} NO soportado. Usar .xlsx o .xls")
        
        df = pd.read_excel(path, engine=engine, sheet_name=None, dtype=str)

        return df
    except Exception as e:
        raise IOError(f"Error al intentar leer el archivo Excel: {e}")