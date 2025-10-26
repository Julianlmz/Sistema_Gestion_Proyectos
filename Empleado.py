from fastapi import APIRouter
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