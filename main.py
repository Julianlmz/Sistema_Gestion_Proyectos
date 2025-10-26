from fastapi import FastAPI
from Database import create_tables
import Empleado, Proyecto

app = FastAPI(title="Sistema de Gestion de Proyectos")
create_tables()

app.include_router(Empleado.router)
app.include_router(Proyecto.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
