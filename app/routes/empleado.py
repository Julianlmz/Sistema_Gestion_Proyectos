from fastapi import APIRouter, HTTPException, Query
from app.database import SessionDep
from app.models import Empleado, EmpleadoCreate, Estado, EmpleadoConProyectos
from typing import List
from sqlmodel import select

router = APIRouter(tags=["Empleado"], prefix="/empleado")


@router.post("/", response_model=Empleado, status_code=201)
async def create_empleado(new_empleado: EmpleadoCreate, session: SessionDep):
    """
    Crea un nuevo empleado en el sistema.

    Args:
        new_empleado: Datos del empleado a crear (nombre, especialidad, salario, estado)
        session: Sesión de base de datos

    Returns:
        Empleado: El empleado creado con su ID asignado

    Raises:
        HTTPException 400: Si los datos de validación fallan (salario negativo, campos vacíos, etc.)
    """
    empleado = Empleado.model_validate(new_empleado)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado


@router.get("/", response_model=List[Empleado])
async def lista_empleados(especialidad: str = Query(default=""), estado : Estado = Query(default=None), session: SessionDep = None):
    """
    Obtiene una lista de empleados con filtros opcionales.

    Args:
        especialidad: Filtro por especialidad (búsqueda parcial, case-sensitive)
        estado: Filtro por estado (Activo o Inactivo)
        session: Sesión de base de datos

    Returns:
        List[Empleado]: Lista de empleados que cumplen con los filtros

    Examples:
        - GET /empleado/ - Todos los empleados
        - GET /empleado/?especialidad=Desarrollador - Empleados con "Desarrollador" en especialidad
        - GET /empleado/?estado=Activo - Solo empleados activos
        - GET /empleado/?especialidad=Backend&estado=Activo - Combinación de filtros
    """
    query = select(Empleado)
    if especialidad:
        query = query.where(Empleado.especialidad.contains(especialidad))
    if estado:
        query = query.where(Empleado.estado == estado)
    empleados = session.exec(query).all()
    return empleados


@router.get("/{empleado_id}", response_model=EmpleadoConProyectos)
async def obtener_empleado(empleado_id: int, session: SessionDep):
    """
    Obtiene un empleado específico por su ID, incluyendo sus proyectos asignados.

    Args:
        empleado_id: ID único del empleado
        session: Sesión de base de datos

    Returns:
        EmpleadoConProyectos: Datos del empleado con lista de proyectos en los que participa

    Raises:
        HTTPException 404: Si el empleado no existe
    """
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="El empleado no existe")
    return empleado


@router.put("/{empleado_id}", response_model=Empleado)
async def update_empleado(empleado_id: int, updated: EmpleadoCreate, session: SessionDep):
    """
    Actualiza los datos de un empleado existente.

    Args:
        empleado_id: ID único del empleado a actualizar
        updated: Nuevos datos del empleado
        session: Sesión de base de datos

    Returns:
        Empleado: El empleado actualizado

    Raises:
        HTTPException 404: Si el empleado no existe
        HTTPException 400: Si los datos de validación fallan
    """
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
    """
    Elimina un empleado del sistema.

    Regla de negocio: No se puede eliminar un empleado que es gerente de algún proyecto.
    Primero se debe reasignar o eliminar los proyectos donde es gerente.

    Args:
        empleado_id: ID único del empleado a eliminar
        session: Sesión de base de datos

    Returns:
        None: Respuesta vacía con código 204

    Raises:
        HTTPException 404: Si el empleado no existe
        HTTPException 400: Si el empleado es gerente de algún proyecto
    """
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if empleado.proyectos_gerente:
        nombres_proyectos = [p.nombre for p in empleado.proyectos_gerente]
        raise HTTPException(status_code=400,
                            detail=f"El empleado no se puede eliminar, el empleado es gerente de: {'; '.join(nombres_proyectos)}")
    session.delete(empleado)
    session.commit()
    return


@router.get("/{empleado_id}/proyectos", response_model=dict)
async def proyectos_del_empleado(empleado_id: int, session: SessionDep):
    """
    Obtiene todos los proyectos relacionados con un empleado.

    Incluye dos tipos de relaciones:
    - Proyectos donde está asignado como miembro del equipo
    - Proyectos donde es gerente

    Args:
        empleado_id: ID único del empleado
        session: Sesión de base de datos

    Returns:
        dict: Diccionario con información del empleado y sus proyectos organizados por rol

    Raises:
        HTTPException 404: Si el empleado no existe
    """
    empleado = session.get(Empleado, empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="El empleado no existe")
    proyectos_asignados = [{"id": p.id, "nombre": p.nombre} for p in empleado.proyectos]
    proyectos_como_gerente = [{"id": p.id, "nombre": p.nombre, "rol": "gerente"} for p in empleado.proyectos_gerente]
    return {"empleado_id": empleado_id,
            "nombre": empleado.nombre,
            "proyectos_asignados": proyectos_asignados,
            "proyectos_como_gerente": proyectos_como_gerente}