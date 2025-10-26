from fastapi import APIRouter
from Database import SessionDep
from models import Empleado, EmpleadoCreate

router = APIRouter(tags=["Empleado"], prefix="/empleado")

@router.post("/", response_model=Empleado, status_code=201)
async def create_empleado(new_empleado: EmpleadoCreate, session: SessionDep):
    empleado = Empleado.model_validate(new_empleado)
    session.add(empleado)
    session.commit()
    session.refresh(empleado)
    return empleado
