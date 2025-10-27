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
async def lista_proyectos(estado: Estado = Query(default=None), presupuesto_min: float = Query(default=0), presupuesto_max: float = Query(default=float("inf")), session: SessionDep = None):
    query = select(Proyecto)
    if estado:
        query = query.where(Proyecto.estado == estado)
    query = query.where(Proyecto.presupuesto >= presupuesto_min)
    query = query.where(Proyecto.presupuesto <= presupuesto_max)
    proyectos = session.exec(query).all()
    return proyectos

@router.get("/{proyecto_id}", response_model=ProyectoConRelaciones)
async def obtener_proyecto(proyecto_id: int, session: SessionDep):
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.put("/{proyecto_id}", response_model=Proyecto)
async def update_proyecto(proyecto_id: int, updated: ProyectoCreate, session: SessionDep):
    proyecto =session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    gerente = session.get(Empleado, updated.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")
    if proyecto.nombre != updated.nombre:
        updated = session.exec(select(Proyecto).where(Proyecto.nombre == updated.nombre)).first()
        if updated:
            raise HTTPException(status_code=400, detail= f"Ya existe un proyecto con el nombre '{updated.nombre}'")
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

@router.post("/{proyecto_id}/asignar", response_model=ProyectoConRelaciones, status_code=200)
async def asignar_empleado(proyecto_id: int, asignacion: AsignarEmpleado, session: SessionDep):
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleado = session.get(Empleado, asignacion.empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    asignacion_existente = session.exec(select(EmpleadoProyecto).where(EmpleadoProyecto.empleado_id == asignacion.empleado_id, EmpleadoProyecto.proyecto_id == proyecto_id)).first()
    if asignacion_existente:
        raise HTTPException(status_code=400, detail= f"El empleado '{empleado.nombre}' ya esta asignado al proyecto '{proyecto.nombre}'")
    nueva_asignacion = EmpleadoProyecto(empleado_id = asignacion.empleado_id, proyecto_id = proyecto_id)
    session.add(nueva_asignacion)
    session.commit()
    session.refresh(proyecto)
    return proyecto