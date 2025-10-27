from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import List

class Estado(str,Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class EmpleadoProyecto(SQLModel, table=True):
    empleado_id: int = Field(foreign_key="empleado.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)

class EmpleadoBase(SQLModel):
    nombre: str
    especialidad: str
    salario: float
    estado: Estado

class Empleado(EmpleadoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    proyectos: List["Proyecto"] = Relationship(back_populates="empleados", link_model=EmpleadoProyecto)
    proyectos_gerente: List["Proyecto"] = Relationship(back_populates="gerente")

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoConProyectos(EmpleadoBase):
    id: int
    proyectos: List["ProyectoResumen"] = []

class ProyectoResumen(SQLModel):
    id: int
    nombre: str
    descripcion: str
    presupuesto: str
    estado: Estado

class ProyectoBase(SQLModel):
    nombre: str
    descripcion: str
    presupuesto: float
    estado: Estado

class Proyecto(ProyectoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gerente_id: int = Field(foreign_key="empleado.id")
    gerente: Empleado = Relationship(back_populates="proyectos_gerente")
    empleados: List[Empleado] = Relationship(back_populates="proyectos", link_model=EmpleadoProyecto)

class ProyectoCreate(ProyectoBase):
    gerente_id: int

class EmpleadoResumen(SQLModel):
    id: int
    nombre: str
    especialidad: str
    salario: float
    estado: Estado

class ProyectoConRelaciones(ProyectoBase):
    id: int
    gerente_id: int
    gerente: EmpleadoResumen
    empleados: List[EmpleadoResumen] = []

class AsignarEmpleado(SQLModel):
    empleado_id: int