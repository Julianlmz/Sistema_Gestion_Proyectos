from fastapi import APIRouter, HTTPException, Query
from app.database import SessionDep
from app.models import Proyecto, ProyectoCreate, Estado, ProyectoConRelaciones, Empleado, EmpleadoProyecto, AsignarEmpleado, EmpleadoResumen, ProyectoUpdate
from typing import List
from sqlmodel import select

router = APIRouter(tags=["Proyecto"], prefix="/proyecto")


@router.post("/", response_model=Proyecto, status_code=201)
async def create_proyecto(new_proyecto: ProyectoCreate, session: SessionDep):
    """
    Crea un nuevo proyecto en el sistema.

    Reglas de negocio:
    - El gerente debe existir en la base de datos
    - El nombre del proyecto debe ser único

    Args:
        new_proyecto: Datos del proyecto a crear (nombre, descripción, presupuesto, estado, gerente_id)
        session: Sesión de base de datos

    Returns:
        Proyecto: El proyecto creado con su ID asignado

    Raises:
        HTTPException 404: Si el gerente especificado no existe
        HTTPException 409: Si ya existe un proyecto con el mismo nombre
        HTTPException 400: Si los datos de validación fallan
    """
    gerente = session.get(Empleado, new_proyecto.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")
    proyecto_existente = session.exec(select(Proyecto).where(Proyecto.nombre == new_proyecto.nombre)).first()
    if proyecto_existente:
        raise HTTPException(status_code=409, detail=f"Ya existe un proyecto con el nombre '{new_proyecto.nombre}'")
    proyecto = Proyecto.model_validate(new_proyecto)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto


@router.get("/", response_model=List[Proyecto])
async def lista_proyectos(estado: Estado = Query(default=None), presupuesto_min: float = Query(default=0), presupuesto_max: float = Query(default=float("inf")), session: SessionDep = None):
    """
    Obtiene una lista de proyectos con filtros opcionales.

    Args:
        estado: Filtro por estado (Activo o Inactivo)
        presupuesto_min: Presupuesto mínimo (inclusive)
        presupuesto_max: Presupuesto máximo (inclusive)
        session: Sesión de base de datos

    Returns:
        List[Proyecto]: Lista de proyectos que cumplen con los filtros

    Examples:
        - GET /proyecto/ - Todos los proyectos
        - GET /proyecto/?estado=Activo - Solo proyectos activos
        - GET /proyecto/?presupuesto_min=10000 - Proyectos con presupuesto >= 10000
        - GET /proyecto/?presupuesto_min=10000&presupuesto_max=50000 - Rango de presupuesto
        - GET /proyecto/?estado=Activo&presupuesto_min=20000 - Combinación de filtros
    """
    query = select(Proyecto)
    if estado:
        query = query.where(Proyecto.estado == estado)
    query = query.where(Proyecto.presupuesto >= presupuesto_min)
    query = query.where(Proyecto.presupuesto <= presupuesto_max)
    proyectos = session.exec(query).all()
    return proyectos


@router.get("/{proyecto_id}", response_model=ProyectoConRelaciones)
async def obtener_proyecto(proyecto_id: int, session: SessionDep):
    """
    Obtiene un proyecto específico por su ID, incluyendo gerente y empleados asignados.

    Args:
        proyecto_id: ID único del proyecto
        session: Sesión de base de datos

    Returns:
        ProyectoConRelaciones: Datos completos del proyecto con información del gerente
                               y lista de empleados asignados

    Raises:
        HTTPException 404: Si el proyecto no existe
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@router.put("/{proyecto_id}", response_model=Proyecto)
async def update_proyecto(proyecto_id: int, updated: ProyectoCreate, session: SessionDep):
    """
    Actualiza los datos de un proyecto existente.

    Reglas de negocio:
    - El nuevo gerente debe existir
    - Si se cambia el nombre, el nuevo nombre debe ser único

    Args:
        proyecto_id: ID único del proyecto a actualizar
        updated: Nuevos datos del proyecto
        session: Sesión de base de datos

    Returns:
        Proyecto: El proyecto actualizado

    Raises:
        HTTPException 404: Si el proyecto o el nuevo gerente no existen
        HTTPException 409: Si el nuevo nombre ya está en uso por otro proyecto
        HTTPException 400: Si los datos de validación fallan
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    gerente = session.get(Empleado, updated.gerente_id)
    if not gerente:
        raise HTTPException(status_code=404, detail="Gerente no encontrado")
    if proyecto.nombre != updated.nombre:
        proyecto_existente = session.exec(select(Proyecto).where(Proyecto.nombre == updated.nombre)).first()
        if proyecto_existente:
            raise HTTPException(status_code=409, detail=f"Ya existe un proyecto con el nombre '{updated.nombre}'")
    proyecto.nombre = updated.nombre
    proyecto.descripcion = updated.descripcion
    proyecto.presupuesto = updated.presupuesto
    proyecto.estado = updated.estado
    proyecto.gerente_id = updated.gerente_id
    session.commit()
    session.refresh(proyecto)
    return proyecto


@router.patch("/{proyecto_id}", response_model=Proyecto)
async def patch_proyecto(proyecto_id: int, updated: ProyectoUpdate, session: SessionDep):
    """
        Args:
            proyecto_id (int): ID único del proyecto a actualizar.
            updated (ProyectoUpdate): Datos nuevos del proyecto (parciales).
            session (SessionDep): Sesión activa de base de datos.

        Returns:
            Proyecto: Instancia del proyecto actualizada con los nuevos datos.

        Raises:
            HTTPException 404: Si el proyecto o el gerente especificado no existen.
            HTTPException 400: Si no se proporcionan datos para actualizar.
            HTTPException 409: Si el nuevo nombre de proyecto ya está en uso.
        """

    proyecto_db = session.get(Proyecto, proyecto_id)
    if not proyecto_db:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    update_data = updated.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
    if "gerente_id" in update_data:
        nuevo_gerente_id = update_data["gerente_id"]
        gerente = session.get(Empleado, nuevo_gerente_id)
        if not gerente:
            raise HTTPException(status_code=404, detail=f"Gerente con id {nuevo_gerente_id} no encontrado")
    if "nombre" in update_data:
        nuevo_nombre = update_data["nombre"]
        if proyecto_db.nombre != nuevo_nombre:
            proyecto_existente = session.exec(select(Proyecto).where(Proyecto.nombre == nuevo_nombre)).first()
            if proyecto_existente:
                raise HTTPException(status_code=409, detail=f"Ya existe un proyecto con el nombre '{nuevo_nombre}'")
    for key, value in update_data.items():
        setattr(proyecto_db, key, value)
    session.add(proyecto_db)
    session.commit()
    session.refresh(proyecto_db)

    return proyecto_db


@router.delete("/{proyecto_id}", status_code=204)
async def delete_proyecto(proyecto_id: int, session: SessionDep):
    """
    Elimina un proyecto del sistema.

    Nota: La eliminación también removerá automáticamente todas las asignaciones
    de empleados a este proyecto (cascada en tabla intermedia).

    Args:
        proyecto_id: ID único del proyecto a eliminar
        session: Sesión de base de datos

    Returns:
        None: Respuesta vacía con código 204

    Raises:
        HTTPException 404: Si el proyecto no existe
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    session.delete(proyecto)
    session.commit()
    return


@router.post("/{proyecto_id}/asignar", response_model=ProyectoConRelaciones, status_code=200)
async def asignar_empleado(proyecto_id: int, asignacion: AsignarEmpleado, session: SessionDep):
    """
    Asigna un empleado a un proyecto.

    Reglas de negocio:
    - El proyecto y el empleado deben existir
    - No se puede asignar el mismo empleado dos veces al mismo proyecto

    Args:
        proyecto_id: ID del proyecto
        asignacion: Objeto con el empleado_id a asignar
        session: Sesión de base de datos

    Returns:
        ProyectoConRelaciones: El proyecto actualizado con la lista completa de empleados

    Raises:
        HTTPException 404: Si el proyecto o el empleado no existen
        HTTPException 409: Si el empleado ya está asignado al proyecto
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    empleado = session.get(Empleado, asignacion.empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    asignacion_existente = session.exec(select(EmpleadoProyecto).where(EmpleadoProyecto.empleado_id == asignacion.empleado_id, EmpleadoProyecto.proyecto_id == proyecto_id)).first()
    if asignacion_existente:
        raise HTTPException(status_code=409, detail= f"El empleado '{empleado.nombre}' ya esta asignado al proyecto '{proyecto.nombre}'")
    nueva_asignacion = EmpleadoProyecto(empleado_id = asignacion.empleado_id, proyecto_id = proyecto_id)
    session.add(nueva_asignacion)
    session.commit()
    session.refresh(proyecto)
    return proyecto


@router.delete("/{proyecto_id}/desasignar/{empleado_id}", status_code=204)
async def desasignar_empleado(proyecto_id: int, empleado_id: int, session: SessionDep):
    """
    Desasigna un empleado de un proyecto.

    Remueve la relación entre el empleado y el proyecto sin eliminar
    ninguna de las entidades principales.

    Args:
        proyecto_id: ID del proyecto
        empleado_id: ID del empleado a desasignar
        session: Sesión de base de datos

    Returns:
        None: Respuesta vacía con código 204

    Raises:
        HTTPException 404: Si el proyecto no existe o el empleado no está asignado al proyecto
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    asignacion = session.exec(select(EmpleadoProyecto).where(EmpleadoProyecto.empleado_id == empleado_id, EmpleadoProyecto.proyecto_id == proyecto_id)).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="El empleado no esta asignado a este proyecto")
    session.delete(asignacion)
    session.commit()
    return


@router.get("/{proyecto_id}/empleados", response_model= List[EmpleadoResumen])
async def empleados_del_proyecto(proyecto_id: int, session: SessionDep):
    """
    Obtiene la lista de empleados asignados a un proyecto.

    Args:
        proyecto_id: ID del proyecto
        session: Sesión de base de datos

    Returns:
        List[EmpleadoResumen]: Lista de empleados con información resumida
                               (id, nombre, especialidad, salario, estado)

    Raises:
        HTTPException 404: Si el proyecto no existe
    """
    proyecto = session.get(Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto.empleados