from fastapi import FastAPI
from app.database import create_tables
from app.routes import empleado, proyecto

app = FastAPI(
    title="Sistema de Gestión de Proyectos",
    description="API REST para gestión de proyectos y empleados con FastAPI y SQLModel")

create_tables()

app.include_router(empleado.router)
app.include_router(proyecto.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido al Sistema de Gestión de Proyectos",
        "docs": "/docs",
        "redoc": "/redoc",
    }
