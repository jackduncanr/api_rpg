from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="RPG API")

class Personaje(BaseModel):
    id: Optional[int] = None
    nombre: str          
    color_piel: str      
    raza: str            
    clase: str
    fuerza: int          
    agilidad: int        
    magia: int           
    conocimiento: int    

db_personajes = []

@app.post("/personajes/", response_model=Personaje)
def crear_personaje(personaje: Personaje):
    personaje.id = len(db_personajes) + 1
    db_personajes.append(personaje)
    return personaje

@app.get("/personajes/", response_model=List[Personaje])
def obtener_personajes():
    return db_personajes

@app.post("/batalla/")
def simular_batalla(id_jugador1: int, id_jugador2: int):

    p1 = next((p for p in db_personajes if p.id == id_jugador1), None)
    p2 = next((p for p in db_personajes if p.id == id_jugador2), None)
    
    if not p1 or not p2:
        raise HTTPException(status_code=404, detail="Uno o ambos personajes no existen")

    def calcular_poder(p):
        return (p.fuerza * 1.5) + (p.magia * 1.3) + (p.conocimiento * 1.1) + (p.agilidad * 0.5)

    poder1 = calcular_poder(p1)
    poder2 = calcular_poder(p2)

    if poder1 > poder2:
        ganador = p1
        perdedor = p2
        puntaje = poder1
    elif poder2 > poder1:
        ganador = p2
        perdedor = p1
        puntaje = poder2
    else:
        return {"resultado": "Empate"}

    return {
        "ganador": ganador.nombre,
        "resumen": f"{ganador.nombre} venció a {perdedor.nombre}",
        "puntaje": round(puntaje, 2)
    }


@app.get("/")
def interfaz():
    return FileResponse("templates/index.html")