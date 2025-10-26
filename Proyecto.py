from fastapi import APIRouter
from Database import SessionDep
from models import Proyecto, ProyectoCreate

router = APIRouter(tags=["Proyecto"], prefix="/proyecto")

@router.post("/", response_model=Proyecto, status_code=201)
async def create_proyecto(new_proyecto: ProyectoCreate, session: SessionDep):
    proyecto = Proyecto.model_validate(new_proyecto)
    session.add(proyecto)
    session.commit()
    session.refresh(proyecto)
    return proyecto