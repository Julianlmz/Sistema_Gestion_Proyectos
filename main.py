from fastapi import FastAPI
import Empleado, Proyecto

app = FastAPI(title="Sistema de Gestion de Proyectos")

app.include_router(Empleado.router)
app.include_router(Proyecto.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
