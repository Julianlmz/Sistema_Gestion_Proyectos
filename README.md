# Sistema de Gestión de Proyectos

API REST para la gestión de proyectos y empleados construida con FastAPI y SQLModel.

## 📋 Descripción

Sistema que permite administrar empleados y proyectos, incluyendo la asignación de empleados a proyectos y la gestión de gerentes. Implementa relaciones many-to-many entre empleados y proyectos, además de relaciones one-to-many para gerentes.

## ✨ Características

- ✅ CRUD completo para Empleados y Proyectos
- ✅ Asignación y desasignación de empleados a proyectos
- ✅ Relaciones entre entidades (Empleado-Proyecto, Gerente-Proyecto)
- ✅ Filtros avanzados de búsqueda
- ✅ Validaciones de negocio robustas
- ✅ Manejo de errores HTTP apropiados
- ✅ Documentación automática con Swagger
- ✅ 15 endpoints funcionales
- ✅ 6 reglas de negocio implementadas

## 🛠️ Tecnologías

- **FastAPI** 0.120.0 - Framework web moderno y rápido
- **SQLModel** 0.0.27 - ORM basado en SQLAlchemy y Pydantic
- **SQLite** - Base de datos embebida
- **Uvicorn** 0.38.0 - Servidor ASGI
- **Pydantic** 2.12.3 - Validación de datos

## 📋 Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd <nombre-del-proyecto>
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

### 1. Iniciar el servidor
```bash
uvicorn app.main:app --reload
```

### 2. Acceder a la aplicación
- **API**: http://127.0.0.1:8000
- **Documentación Swagger**: http://127.0.0.1:8000/docs
- **Documentación ReDoc**: http://127.0.0.1:8000/redoc

## 📁 Estructura del Proyecto
```
.
├── app/
│   ├── __init__.py              # Inicialización del paquete
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── database.py              # Configuración de base de datos
│   ├── models.py                # Modelos SQLModel y Pydantic
│   └── routes/
│       ├── __init__.py          # Inicialización de routers
│       ├── empleado.py          # Endpoints de empleados
│       └── proyecto.py          # Endpoints de proyectos
├── tests/
│   └── test_main.http           # Suite de tests HTTP (62 tests)
├── docs/
│   └── API_EXAMPLES.md          # Ejemplos de uso de la API
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
├── LICENSE                      # Licencia MIT
└── README.md                    # Este archivo
```

## 🗄️ Modelos de Datos

### Empleado
```python
{
  "id": int,              # Identificador único (auto-generado)
  "nombre": string,       # Nombre del empleado (3-50 caracteres)
  "especialidad": string, # Área de especialización (3-50 caracteres)
  "salario": float,       # Salario del empleado (> 0, redondeado a 2 decimales)
  "estado": Estado        # Estado: "Activo" o "Inactivo"
}
```

### Proyecto
```python
{
  "id": int,              # Identificador único (auto-generado)
  "nombre": string,       # Nombre del proyecto (3-50 caracteres, único)
  "descripcion": string,  # Descripción del proyecto (10-100 caracteres)
  "presupuesto": float,   # Presupuesto asignado (> 0, redondeado a 2 decimales)
  "estado": Estado,       # Estado: "Activo" o "Inactivo"
  "gerente_id": int       # ID del empleado gerente (FK a Empleado)
}
```

### Relaciones
- **Empleado ↔ Proyecto**: Relación Many-to-Many (tabla intermedia: `EmpleadoProyecto`)
- **Empleado → Proyecto**: Relación One-to-Many (un empleado puede ser gerente de varios proyectos)

## 🔗 Endpoints API

### 📊 Resumen de Endpoints

| Recurso | Endpoints | Operaciones |
|---------|-----------|-------------|
| **Empleados** | 6 | CRUD + relaciones |
| **Proyectos** | 8 | CRUD + asignaciones |
| **Root** | 1 | Información |
| **Total** | **15** | - |

---

### 👥 Empleados

#### Crear empleado
```http
POST /empleado/
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "especialidad": "Desarrollador Backend",
  "salario": 5000.0,
  "estado": "Activo"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "especialidad": "Desarrollador Backend",
  "salario": 5000.0,
  "estado": "Activo"
}
```

#### Listar empleados (con filtros opcionales)
```http
GET /empleado/
GET /empleado/?especialidad=Backend
GET /empleado/?estado=Activo
GET /empleado/?especialidad=Desarrollador&estado=Activo
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "especialidad": "Desarrollador Backend",
    "salario": 5000.0,
    "estado": "Activo"
  }
]
```

#### Obtener empleado por ID (con proyectos)
```http
GET /empleado/{empleado_id}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "especialidad": "Desarrollador Backend",
  "salario": 5000.0,
  "estado": "Activo",
  "proyectos": [
    {
      "id": 1,
      "nombre": "Sistema CRM",
      "descripcion": "Sistema de gestión de clientes",
      "presupuesto": 50000.0,
      "estado": "Activo"
    }
  ]
}
```

#### Actualizar empleado
```http
PUT /empleado/{empleado_id}
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "especialidad": "Desarrollador Full Stack",
  "salario": 6000.0,
  "estado": "Activo"
}
```

#### Eliminar empleado
```http
DELETE /empleado/{empleado_id}
```

**⚠️ Regla de negocio:** No se puede eliminar un empleado que es gerente de proyectos.

#### Ver proyectos del empleado
```http
GET /empleado/{empleado_id}/proyectos
```

**Respuesta (200 OK):**
```json
{
  "empleado_id": 1,
  "nombre": "Juan Pérez",
  "proyectos_asignados": [
    {
      "id": 2,
      "nombre": "App Mobile"
    }
  ],
  "proyectos_como_gerente": [
    {
      "id": 1,
      "nombre": "Sistema CRM",
      "rol": "gerente"
    }
  ]
}
```

---

### 📁 Proyectos

#### Crear proyecto
```http
POST /proyecto/
Content-Type: application/json

{
  "nombre": "Sistema CRM",
  "descripcion": "Desarrollo de sistema de gestión de clientes",
  "presupuesto": 50000.0,
  "estado": "Activo",
  "gerente_id": 1
}
```

**⚠️ Reglas de negocio:**
- El gerente debe existir
- El nombre del proyecto debe ser único

#### Listar proyectos (con filtros opcionales)
```http
GET /proyecto/
GET /proyecto/?estado=Activo
GET /proyecto/?presupuesto_min=10000
GET /proyecto/?presupuesto_max=100000
GET /proyecto/?presupuesto_min=10000&presupuesto_max=100000
GET /proyecto/?estado=Activo&presupuesto_min=20000&presupuesto_max=80000
```

#### Obtener proyecto por ID (con gerente y empleados)
```http
GET /proyecto/{proyecto_id}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Sistema CRM",
  "descripcion": "Sistema de gestión de clientes",
  "presupuesto": 50000.0,
  "estado": "Activo",
  "gerente_id": 1,
  "gerente": {
    "id": 1,
    "nombre": "Juan Pérez",
    "especialidad": "Desarrollador Backend",
    "salario": 5000.0,
    "estado": "Activo"
  },
  "empleados": [
    {
      "id": 2,
      "nombre": "Carlos López",
      "especialidad": "Frontend Developer",
      "salario": 5500.0,
      "estado": "Activo"
    }
  ]
}
```

#### Actualizar proyecto
```http
PUT /proyecto/{proyecto_id}
Content-Type: application/json

{
  "nombre": "Sistema CRM v2",
  "descripcion": "Actualización del sistema CRM",
  "presupuesto": 60000.0,
  "estado": "Activo",
  "gerente_id": 1
}
```

#### Eliminar proyecto
```http
DELETE /proyecto/{proyecto_id}
```

#### Asignar empleado a proyecto
```http
POST /proyecto/{proyecto_id}/asignar
Content-Type: application/json

{
  "empleado_id": 2
}
```

**⚠️ Reglas de negocio:**
- El proyecto y el empleado deben existir
- No se puede asignar el mismo empleado dos veces

#### Desasignar empleado de proyecto
```http
DELETE /proyecto/{proyecto_id}/desasignar/{empleado_id}
```

**⚠️ Regla de negocio:** La asignación debe existir.

#### Listar empleados del proyecto
```http
GET /proyecto/{proyecto_id}/empleados
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 2,
    "nombre": "Carlos López",
    "especialidad": "Frontend Developer",
    "salario": 5500.0,
    "estado": "Activo"
  }
]
```

---

## 🎯 Reglas de Negocio

### 1. **Protección de eliminación de gerentes**
No se puede eliminar un empleado que es gerente de uno o más proyectos. Primero se debe reasignar o eliminar los proyectos donde es gerente.

**Código HTTP:** `400 Bad Request`

### 2. **Unicidad del nombre de proyecto**
No pueden existir dos proyectos con el mismo nombre. Esta validación se aplica tanto en creación como en actualización.

**Código HTTP:** `409 Conflict`

### 3. **Validación de gerente**
Al crear o actualizar un proyecto, el gerente especificado debe existir en la base de datos.

**Código HTTP:** `404 Not Found`

### 4. **Prevención de asignaciones duplicadas**
No se puede asignar el mismo empleado dos veces al mismo proyecto.

**Código HTTP:** `409 Conflict`

### 5. **Validación de existencia en asignaciones**
Al asignar un empleado a un proyecto, tanto el empleado como el proyecto deben existir.

**Código HTTP:** `404 Not Found`

### 6. **Validación de desasignación**
Solo se puede desasignar un empleado que esté actualmente asignado al proyecto.

**Código HTTP:** `404 Not Found`

---

## ✅ Validaciones

### Validaciones Automáticas (Pydantic)

| Campo | Validación | Descripción |
|-------|------------|-------------|
| `nombre` (Empleado) | `min_length=3, max_length=50` | Longitud entre 3 y 50 caracteres |
| `especialidad` | `min_length=3, max_length=50` | Longitud entre 3 y 50 caracteres |
| `salario` | `gt=0` | Mayor que 0, redondeado a 2 decimales |
| `estado` | `Enum` | Solo acepta "Activo" o "Inactivo" |
| `nombre` (Proyecto) | `min_length=3, max_length=50` | Longitud entre 3 y 50 caracteres |
| `descripcion` | `min_length=10, max_length=100` | Longitud entre 10 y 100 caracteres |
| `presupuesto` | `gt=0` | Mayor que 0, redondeado a 2 decimales |

### Validaciones Custom

- **Salario redondeado**: `@field_validator('salario')` redondea automáticamente a 2 decimales
- **Presupuesto redondeado**: `@field_validator('presupuesto')` redondea automáticamente a 2 decimales

---

## 📡 Códigos de Estado HTTP

| Código | Descripción | Uso |
|--------|-------------|-----|
| **200 OK** | Operación exitosa | GET, POST (asignar) |
| **201 Created** | Recurso creado exitosamente | POST (crear) |
| **204 No Content** | Eliminación exitosa | DELETE |
| **400 Bad Request** | Solicitud inválida o regla de negocio violada | Validación Pydantic, reglas de negocio |
| **404 Not Found** | Recurso no encontrado | Empleado/Proyecto inexistente |
| **409 Conflict** | Conflicto (duplicado) | Nombre duplicado, asignación duplicada |

---

## 🧪 Ejemplos de Uso Completos

### Flujo 1: Crear empleado y proyecto
```bash
# 1. Crear empleado gerente
curl -X POST "http://127.0.0.1:8000/empleado/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "especialidad": "Project Manager",
    "salario": 7000.0,
    "estado": "Activo"
  }'
# Respuesta: {"id": 1, ...}

# 2. Crear proyecto con ese empleado como gerente
curl -X POST "http://127.0.0.1:8000/proyecto/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "App Mobile",
    "descripcion": "Desarrollo de aplicación móvil",
    "presupuesto": 75000.0,
    "estado": "Activo",
    "gerente_id": 1
  }'
# Respuesta: {"id": 1, ...}

# 3. Crear empleado desarrollador
curl -X POST "http://127.0.0.1:8000/empleado/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos López",
    "especialidad": "Desarrollador Mobile",
    "salario": 5500.0,
    "estado": "Activo"
  }'
# Respuesta: {"id": 2, ...}

# 4. Asignar empleado al proyecto
curl -X POST "http://127.0.0.1:8000/proyecto/1/asignar" \
  -H "Content-Type: application/json" \
  -d '{"empleado_id": 2}'

# 5. Ver empleados del proyecto
curl "http://127.0.0.1:8000/proyecto/1/empleados"
```

### Flujo 2: Filtrar y consultar
```bash
# Listar empleados activos con especialidad específica
curl "http://127.0.0.1:8000/empleado/?especialidad=Desarrollador&estado=Activo"

# Listar proyectos en rango de presupuesto
curl "http://127.0.0.1:8000/proyecto/?presupuesto_min=50000&presupuesto_max=100000"

# Ver proyectos de un empleado
curl "http://127.0.0.1:8000/empleado/2/proyectos"
```

---

## 🧪 Pruebas

El proyecto incluye una suite completa de 62 tests en `tests/test_main.http`.

### Ejecutar tests con VS Code REST Client

1. Instalar extensión **REST Client** en VS Code
2. Abrir `tests/test_main.http`
3. Click en "Send Request" sobre cada test
4. O usar `Ctrl+Alt+R` (Windows) / `Cmd+Alt+R` (Mac)

### Categorías de tests

- ✅ Root & Health: 3 tests
- ✅ Empleados CRUD: 13 tests
- ✅ Proyectos CRUD: 13 tests
- ✅ Asignaciones: 15 tests
- ✅ Validaciones de negocio: 8 tests
- ✅ Actualización de gerente: 3 tests
- ✅ Casos extremos: 5 tests
- ✅ Limpieza: 2 tests

---

## 🔧 Desarrollo

### Agregar nuevos endpoints

1. Crear función en el router correspondiente (`app/routes/empleado.py` o `app/routes/proyecto.py`)
2. Decorar con `@router.get/post/put/delete`
3. Definir modelos de respuesta en `app/models.py` si es necesario
4. Agregar docstring completo
5. Manejar errores con `HTTPException`

### Agregar nuevas validaciones

- **Validaciones Pydantic**: En los modelos con `Field()`
- **Validaciones custom**: Con `@field_validator`
- **Validaciones de negocio**: En los endpoints con `HTTPException`

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"
```bash
# Asegúrate de estar en la raíz del proyecto
cd /ruta/al/proyecto
uvicorn app.main:app --reload
```

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Activa el entorno virtual e instala dependencias
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# Usa otro puerto
uvicorn app.main:app --reload --port 8001
```

### La base de datos no se crea o tiene datos corruptos
```bash
# Elimina la base de datos y reinicia
rm Proyectos.db
uvicorn app.main:app --reload
```

---

## 📚 Recursos Adicionales

- **Documentación FastAPI**: https://fastapi.tiangolo.com/
- **Documentación SQLModel**: https://sqlmodel.tiangolo.com/
- **Ejemplos adicionales**: Ver `docs/API_EXAMPLES.md`
- **Suite de tests**: Ver `tests/test_main.http`

---

## 👨‍💻 Autor

**Julian Steven Leal Martinez**  
ID: 67001277  
Email: jsleal77@ucatolica.edu.co

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📊 Estadísticas del Proyecto

- **Total de Endpoints**: 15
- **Modelos de Datos**: 2 principales + 1 tabla intermedia
- **Reglas de Negocio**: 6
- **Tests**: 62
- **Validaciones**: 13 (8 Pydantic + 2 custom + 3 de negocio)
- **Códigos HTTP**: 6 (200, 201, 204, 400, 404, 409)

---

**¡Gracias por usar el Sistema de Gestión de Proyectos!** 🚀