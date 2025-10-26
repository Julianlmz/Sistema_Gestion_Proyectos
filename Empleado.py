from fastapi import APIRouter, HTTPException
from Database import SessionDep
from models import Empleado, EmpleadoCreate, Estado
from typing import List
from sqlmodel import select

router = APIRouter(tags=["Empleado"], prefix="/empleado")

@router.post("/", response_model=Empleado, status_code=201)
async def create_empleado(new_empleado: EmpleadoCreate, session: SessionDep):
    empleado = Empleado.model_validate(new_empleado)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado

@router.get("/", response_model=List[Empleado])
async def lista_empleados(especialidad: str, estado: Estado, session: SessionDep):
    query = select(Empleado).where(Empleado.especialidad.contains(especialidad), Empleado.estado == estado)
    empleados = session.exec(query).all()
    return empleados

@router.put("/{empleado_id}", response_model=Empleado)
async def update_empleado(empleado_id: int, updated: EmpleadoCreate, session: SessionDep):
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    empleado.nombre = updated.nombre
    empleado.especialidad = updated.especialidad
    empleado.salario = updated.salario
    empleado.estado = updated.estado
    session.commit()
    session.refresh(empleado)
    return empleado