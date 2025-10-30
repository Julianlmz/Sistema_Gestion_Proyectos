from sqlmodel import SQLModel, Relationship, Field
from enum import Enum
from typing import List
from pydantic import field_validator
import re


class Estado(str, Enum):
    """
    Enumeración para los estados posibles de empleados y proyectos.

    Valores permitidos:
    - Activo: La entidad está activa y operativa
    - Inactivo: La entidad está inactiva
    """
    Activo = "Activo"
    Inactivo = "Inactivo"


class EmpleadoProyecto(SQLModel, table=True):
    """
    Tabla intermedia para la relación Many-to-Many entre Empleado y Proyecto.

    Attributes:
        empleado_id: ID del empleado (FK y PK)
        proyecto_id: ID del proyecto (FK y PK)
    """
    empleado_id: int = Field(foreign_key="empleado.id", primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id", primary_key=True)


class EmpleadoBase(SQLModel):
    """
    Modelo base de Empleado con validaciones.

    Attributes:
        nombre: Nombre del empleado (3-50 caracteres)
        especialidad: Especialidad o área del empleado (3-50 caracteres)
        salario: Salario del empleado (debe ser positivo, redondeado a 2 decimales)
        estado: Estado del empleado (Activo o Inactivo)
    """
    nombre: str = Field(min_length=3, max_length=50)
    especialidad: str = Field(min_length=3, max_length=50)
    salario: float = Field(gt=0)
    estado: Estado

    @field_validator('salario')
    @classmethod
    def redondear_salario(cls, v: float) -> float:
        """Redondea el salario a 2 decimales."""
        return round(v, 2)

    @field_validator('nombre', 'especialidad')
    @classmethod
    def validar_solo_letras(cls, v: str) -> str:
        patron = r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$"
        if not re.match(patron, v):
            raise ValueError(f"El campo debe contener solo letras y espacios. Valor recibido: '{v}'")
        return v


class Empleado(EmpleadoBase, SQLModel, table=True):
    """
    Modelo de tabla Empleado con relaciones.

    Relaciones:
    - Many-to-Many con Proyecto (como miembro del equipo)
    - One-to-Many con Proyecto (como gerente)

    Attributes:
        id: Identificador único del empleado
        proyectos: Lista de proyectos donde está asignado como miembro
        proyectos_gerente: Lista de proyectos donde es gerente
    """
    id: int | None = Field(default=None, primary_key=True)
    proyectos: List["Proyecto"] = Relationship(back_populates="empleados", link_model=EmpleadoProyecto)
    proyectos_gerente: List["Proyecto"] = Relationship(back_populates="gerente")


class EmpleadoCreate(EmpleadoBase):
    """
    Esquema para crear un nuevo empleado.
    Hereda todas las validaciones de EmpleadoBase.
    """
    pass


class EmpleadoConProyectos(EmpleadoBase):
    """
    Esquema de respuesta de empleado con sus proyectos asignados.

    Attributes:
        id: Identificador único del empleado
        proyectos: Lista de proyectos donde participa
    """
    id: int
    proyectos: List["ProyectoResumen"] = []


class EmpleadoResumen(SQLModel):
    """
    Esquema resumido de empleado para respuestas anidadas.

    Attributes:
        id: Identificador único
        nombre: Nombre del empleado
        especialidad: Especialidad del empleado
        salario: Salario del empleado
        estado: Estado actual
    """
    id: int
    nombre: str
    especialidad: str
    salario: float
    estado: Estado


class ProyectoResumen(SQLModel):
    """
    Esquema resumido de proyecto para respuestas anidadas.

    Attributes:
        id: Identificador único
        nombre: Nombre del proyecto
        descripcion: Descripción del proyecto
        presupuesto: Presupuesto asignado
        estado: Estado actual
    """
    id: int
    nombre: str
    descripcion: str
    presupuesto: float
    estado: Estado


class ProyectoBase(SQLModel):
    """
    Modelo base de Proyecto con validaciones.

    Attributes:
        nombre: Nombre del proyecto (3-50 caracteres, debe ser único)
        descripcion: Descripción del proyecto (10-100 caracteres)
        presupuesto: Presupuesto del proyecto (debe ser positivo, redondeado a 2 decimales)
        estado: Estado del proyecto (Activo o Inactivo)
    """
    nombre: str = Field(min_length=3, max_length=50)
    descripcion: str = Field(min_length=10, max_length=100)
    presupuesto: float = Field(gt=0)
    estado: Estado

    @field_validator('presupuesto')
    @classmethod
    def redondear_presupuesto(cls, v: float) -> float:
        """Redondea el presupuesto a 2 decimales."""
        return round(v, 2)

    @field_validator('nombre', 'descripcion')
    @classmethod
    def validar_solo_letras(cls, v: str) -> str:
        patron = r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$"
        if not re.match(patron, v):
            raise ValueError(f"El campo debe contener solo letras y espacios. Valor recibido: '{v}'")
        return v

class Proyecto(ProyectoBase, SQLModel, table=True):
    """
    Modelo de tabla Proyecto con relaciones.

    Relaciones:
    - Many-to-One con Empleado (gerente)
    - Many-to-Many con Empleado (miembros del equipo)

    Attributes:
        id: Identificador único del proyecto
        gerente_id: ID del empleado gerente (FK)
        gerente: Empleado que es gerente del proyecto
        empleados: Lista de empleados asignados al proyecto
    """
    id: int | None = Field(default=None, primary_key=True)
    gerente_id: int = Field(foreign_key="empleado.id")
    gerente: Empleado = Relationship(back_populates="proyectos_gerente")
    empleados: List[Empleado] = Relationship(back_populates="proyectos", link_model=EmpleadoProyecto)


class ProyectoCreate(ProyectoBase):
    """
    Esquema para crear un nuevo proyecto.

    Attributes:
        gerente_id: ID del empleado que será gerente del proyecto
    """
    gerente_id: int


class ProyectoConRelaciones(ProyectoBase):
    """
    Esquema de respuesta de proyecto con todas sus relaciones.

    Attributes:
        id: Identificador único del proyecto
        gerente_id: ID del gerente
        gerente: Información completa del gerente
        empleados: Lista de empleados asignados
    """
    id: int
    gerente_id: int
    gerente: EmpleadoResumen
    empleados: List[EmpleadoResumen] = []


class AsignarEmpleado(SQLModel):
    """
    Esquema para asignar un empleado a un proyecto.

    Attributes:
        empleado_id: ID del empleado a asignar
    """
    empleado_id: int