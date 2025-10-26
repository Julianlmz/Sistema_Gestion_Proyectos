from fastapi import FastAPI
import Empleado

app = FastAPI(title="Sistema de Gestion de Proyectos")

app.include_router(Empleado.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
