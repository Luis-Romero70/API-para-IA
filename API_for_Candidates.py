from fastapi import FastAPI, Query
from typing import List, Optional
import pandas as pd

# Importar la función buscar_candidatos
from tu_modulo import buscar_candidatos  # Reemplaza 'tu_modulo' con el nombre de tu módulo

# Crear una instancia de FastAPI
app = FastAPI()

# Ruta para obtener la lista de candidatos
@app.get("/candidatos/")
def obtener_candidatos(
    N: int = 10,
    tech_skills: Optional[List[str]] = Query(None, description="Habilidades técnicas requeridas"),
    soft_skills: Optional[List[str]] = Query(None, description="Habilidades blandas requeridas"),
    idioma: Optional[str] = Query(None, description="Nivel de idioma requerido"),
    disponibilidad_horaria: Optional[List[str]] = Query(None, description="Disponibilidad horaria requerida"),
    perfil_psicologico: Optional[List[str]] = Query(None, description="Perfil psicológico requerido")
):  
    # Aquí deberías cargar tu DataFrame db_candidates
    db_candidates = pd.read_csv('ruta/a/tu/db_candidates.csv')  # Reemplaza 'ruta/a/tu/db_candidates.csv' con la ruta de tu archivo CSV
    
    # Construir la solicitud a partir de los parámetros recibidos
    solicitud = {
        'Tech Skills': tech_skills,
        'Soft Skills': soft_skills,
        'Idioma': idioma,
        'Disponibilidad Horaria': disponibilidad_horaria,
        'Perfil Psicológico': perfil_psicologico
    }
    
    # Obtener la puntuación de los candidatos
    puntuacion = buscar_candidatos(db_candidates, solicitud)
    puntuacion.name = 'puntuacion'
    
    # Obtener los índices de los N candidatos con mayor puntuación
    candidatos_seleccionados = puntuacion.nlargest(N).index.tolist()
    
    # Convertir el índice en una columna normal
    db_candidates_indexed = db_candidates.reset_index()
    
    # Unir las series `puntuacion` y `db_candidates_indexed`
    db_candidates_indexed = db_candidates_indexed.join(puntuacion)
    
    # Seleccionar las filas deseadas
    listado_candidatos_selecc = db_candidates_indexed.set_index(['index']).loc[candidatos_seleccionados].set_index(['Apellido', 'Nombre'])
    
    # Devolver el listado de candidatos seleccionados ordenados por puntuación total
    return listado_candidatos_selecc.to_dict(orient='index')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

