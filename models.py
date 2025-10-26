from sqlmodel import SQLModel, Field

class EmpleadoBase(SQLModel):
    nombre: str
    especialidad: str
    salario: float
    estado: bool

class Empleado(EmpleadoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class EmpleadoCreate(EmpleadoBase):
    pass

class ProyectoBase(SQLModel):
    nombre: str
    descripcion: str
    presupuesto: float
    estado: bool

class Proyecto(ProyectoBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ProyectoCreate(ProyectoBase):
    pass