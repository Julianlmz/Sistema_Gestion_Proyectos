"""
Configuración de la base de datos SQLModel.

Este módulo configura la conexión a la base de datos SQLite
y proporciona funciones para crear tablas y gestionar sesiones.
"""

from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends
from typing import Annotated

# Motor de base de datos SQLite
engine = create_engine('sqlite:///Proyectos.db')


def create_tables():
    """
    Crea todas las tablas definidas en los modelos SQLModel.

    Se ejecuta automáticamente al iniciar la aplicación.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Generador de sesiones de base de datos.

    Yields:
        Session: Sesión de SQLModel para operaciones de BD

    Usage:
        async def endpoint(session: SessionDep):
            # usar session aquí
    """
    with Session(engine) as session:
        yield session


# Tipo anotado para inyección de dependencias
SessionDep = Annotated[Session, Depends(get_session)]