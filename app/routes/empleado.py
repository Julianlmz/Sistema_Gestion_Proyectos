from fastapi import APIRouter, HTTPException, Query
from app.database import SessionDep
from app.models import Empleado, EmpleadoCreate, Estado, EmpleadoConProyectos
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
async def lista_empleados(especialidad: str = Query(default=""), estado : Estado = Query(default=None), session: SessionDep = None):
    query = select(Empleado)
    if especialidad:
        query = query.where(Empleado.especialidad.contains(especialidad))
    if estado:
        query = query.where(Empleado.estado == estado)
    empleados = session.exec(query).all()
    return empleados

@router.get("/{empleado_id}", response_model=EmpleadoConProyectos)
async def obtener_empleado(empleado_id: int, session: SessionDep):
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="El empleado no existe")
    return empleado

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

@router.delete("/{empleado_id}", status_code=204)
async def delete_empleado(empleado_id: int, session: SessionDep):
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if empleado.proyectos_gerente:
        nombres_proyectos = [p.nombre for p in empleado.proyectos_gerente]
        raise HTTPException(status_code=400, detail=f"El empleado no se puede eliminar, el empleado es gerente de: {'; '.join(nombres_proyectos)}")
    session.delete(empleado)
    session.commit()
    return

@router.get("/{empleado_id}/proyectos", response_model=dict)
async def proyectos_del_empleado(empleado_id: int, session: SessionDep):
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="El empleado no existe")
    proyectos_asignados = [{"id": p.id, "nombre": p.nombre} for p in empleado.proyectos]
    proyectos_como_gerente = [{"id": p.id, "nombre": p.nombre, "rol": "gerente"}for p in empleado.proyectos_gerente]
    return {"empleado_id": empleado_id,
            "nombre": empleado.nombre,
            "proyectos_asignados": proyectos_asignados,
            "proyectos_como_gerente": proyectos_como_gerente}
