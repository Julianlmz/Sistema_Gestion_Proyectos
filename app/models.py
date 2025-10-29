from sqlmodel import SQLModel, Relationship
from enum import Enum
from typing import List
from pydantic import Field, field_validator


class Estado(str,Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class EmpleadoProyecto(SQLModel, table=True):
    empleado_id: int = Field(foreign_key="empleado.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)

class EmpleadoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=50)
    especialidad: str = Field(min_length=3, max_length=50)
    salario: float = Field(gt=0)
    estado: Estado

    @field_validator('salario')
    @classmethod
    def redondear_salario(cls, v: float) -> float:
        return round(v, 2)

class Empleado(EmpleadoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    proyectos: List["Proyecto"] = Relationship(back_populates="empleados", link_model=EmpleadoProyecto)
    proyectos_gerente: List["Proyecto"] = Relationship(back_populates="gerente")

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoConProyectos(EmpleadoBase):
    id: int
    proyectos: List["ProyectoResumen"] = []

class EmpleadoResumen(SQLModel):
    id: int
    nombre: str
    especialidad: str
    salario: float
    estado: Estado

class ProyectoResumen(SQLModel):
    id: int
    nombre: str
    descripcion: str
    presupuesto: float
    estado: Estado

class ProyectoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=50)
    descripcion: str = Field(min_length=10, max_length=100)
    presupuesto: float = Field(gt=0)
    estado: Estado

    @field_validator('presupuesto')
    @classmethod
    def redondear_presupuesto(cls, v: float) -> float:
        return round(v, 2)

class Proyecto(ProyectoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gerente_id: int = Field(foreign_key="empleado.id")
    gerente: Empleado = Relationship(back_populates="proyectos_gerente")
    empleados: List[Empleado] = Relationship(back_populates="proyectos", link_model=EmpleadoProyecto)

class ProyectoCreate(ProyectoBase):
    gerente_id: int

class ProyectoConRelaciones(ProyectoBase):
    id: int
    gerente_id: int
    gerente: EmpleadoResumen
    empleados: List[EmpleadoResumen] = []

class AsignarEmpleado(SQLModel):
    empleado_id: int