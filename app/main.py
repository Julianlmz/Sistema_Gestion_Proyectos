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
    """
    Endpoint raíz de la API.

    Proporciona información básica sobre el sistema y enlaces a la documentación.

    Returns:
        dict: Mensaje de bienvenida y enlaces a documentación Swagger y ReDoc
    """
    return {
        "message": "Bienvenido al Sistema de Gestión de Proyectos",
        "docs": "/docs",
        "redoc": "/redoc",
    }
