from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="RPG Battle API")

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
    # 1. Buscar personajes por ID [cite: 41]
    p1 = next((p for p in db_personajes if p.id == id_jugador1), None)
    p2 = next((p for p in db_personajes if p.id == id_jugador2), None)
    
    if not p1 or not p2:
        raise HTTPException(status_code=404, detail="Uno o ambos personajes no existen")

    # 2. Lógica de combate basada en atributos [cite: 13, 43]
    # Calculamos el Poder Total (PT) de cada uno
    # Fuerza influye en daño, Magia en especiales y Conocimiento en estrategia
    def calcular_poder(p):
        poder_base = (p.fuerza * 1.5) + (p.magia * 1.3) + (p.conocimiento * 1.1)
        # Bonus por Agilidad (Evasión/Velocidad)
        return poder_base + (p.agilidad * 0.5)
    poder1 = calcular_poder(p1)
    poder2 = calcular_poder(p2)
    # 3. Determinar ganador
    if poder1 > poder2:
        ganador = p1
        perdedor = p2
        puntaje_ganador = poder1
    elif poder2 > poder1:
        ganador = p2
        perdedor = p1
        puntaje_ganador = poder2
    else:
        return {"resultado": "Empate", "detalle": "Ambos guerreros han caído al mismo tiempo."}
    # 4. Retornar resultado con detalles 
    return {
        "ganador": {
            "nombre": ganador.nombre,
            "clase": ganador.clase,
            "retrato": ganador.url_retrato,
            "puntaje_final": round(puntaje_ganador, 2)
        },
        "resumen": f"¡{ganador.nombre} ha derrotado a {perdedor.nombre} en una batalla épica!",
        "estadisticas_combate": {
            p1.nombre: round(poder1, 2),
            p2.nombre: round(poder2, 2)
        }
    }