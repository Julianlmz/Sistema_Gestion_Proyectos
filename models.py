from sqlmodel import SQLModel, Field
from enum import Enum

class Estado(str,Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class EmpleadoBase(SQLModel):
    nombre: str
    especialidad: str
    salario: float
    estado: Estado

class Empleado(EmpleadoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class EmpleadoCreate(EmpleadoBase):
    pass

class ProyectoBase(SQLModel):
    nombre: str
    descripcion: str
    presupuesto: float
    estado: Estado

class Proyecto(ProyectoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ProyectoCreate(ProyectoBase):
    pass