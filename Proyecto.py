from fastapi import APIRouter, HTTPException, Query
from Database import SessionDep
from models import Proyecto, ProyectoCreate, Estado, ProyectoConRelaciones, Empleado, EmpleadoProyecto, AsignarEmpleado, EmpleadoResumen
from typing import List
from sqlmodel import select

router = APIRouter(tags=["Proyecto"], prefix="/proyecto")

@router.post("/", response_model=Proyecto, status_code=201)
async def create_proyecto(new_proyecto: ProyectoCreate, session: SessionDep):
    gerente = session.get(Empleado, new_proyecto.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")
    proyecto_existente = session.exec(select(Proyecto).where(Proyecto.nombre == new_proyecto.nombre)).first()
    if proyecto_existente:
        raise HTTPException(status_code=400, detail=f"Ya existe un proyecto con el nombre '{new_proyecto.nombre}'")
    proyecto = Proyecto.model_validate(new_proyecto)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto

@router.get("/", response_model=List[Proyecto])
async def lista_proyectos(presupuesto: float, estado: Estado, session: SessionDep):
    query = select(Proyecto).where(Proyecto.presupuesto.contains(presupuesto), Proyecto.estado == estado)
    proyectos = session.exec(query).all()
    return proyectos

@router.put("/{proyecto_id}", response_model=Proyecto)
async def update_proyecto(proyecto_id: int, updated: ProyectoCreate, session: SessionDep):
    proyecto =session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    proyecto.nombre = updated.nombre
    proyecto.descripcion = updated.descripcion
    proyecto.presupuesto = updated.presupuesto
    proyecto.estado = updated.estado
    session.commit()
    session.refresh(proyecto)
    return proyecto

@router.delete("/{proyecto_id}", status_code=204)
async def delete_proyecto(proyecto_id: int, session: SessionDep):
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    session.delete(proyecto)
    session.commit()
    return