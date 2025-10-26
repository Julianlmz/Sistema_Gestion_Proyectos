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

