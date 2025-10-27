# Sistema de Gestión de Proyectos

API para la gestión de proyectos y empleados construida con FastAPI y SQLModel.

## Descripción

Sistema que permite administrar empleados y proyectos, incluyendo la asignación de empleados a proyectos y la gestión de gerentes. Implementa relaciones many-to-many entre empleados y proyectos, además de relaciones one-to-many para gerentes.

## Características

- ✅ CRUD completo para Empleados y Proyectos
- ✅ Asignación y desasignación de empleados a proyectos
- ✅ Relaciones entre entidades (Empleado-Proyecto, Gerente-Proyecto)
- ✅ Filtros avanzados de búsqueda
- ✅ Validaciones de negocio
- ✅ Manejo de errores HTTP apropiados
- ✅ Documentación automática con Swagger

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLModel**: ORM basado en SQLAlchemy y Pydantic
- **SQLite**: Base de datos embebida
- **Uvicorn**: Servidor ASGI

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el repositorio**
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd <nombre-del-proyecto>
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## Ejecución

1. **Iniciar el servidor**
```bash
uvicorn main:app --reload
```

2. **Acceder a la aplicación**
   - API: http://127.0.0.1:8000
   - Documentación Swagger: http://127.0.0.1:8000/docs
   - Documentación ReDoc: http://127.0.0.1:8000/redoc

## Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada de la aplicación
├── Database.py            # Configuración de base de datos
├── models.py              # Modelos SQLModel y Pydantic
├── Empleado.py            # Endpoints de empleados
├── Proyecto.py            # Endpoints de proyectos
├── requirements.txt       # Dependencias del proyecto
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Este archivo
```

## Endpoints API

### Empleados

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

#### Listar empleados (con filtros)
```http
GET /empleado/?especialidad=Backend&estado=Activo
```

#### Obtener empleado por ID
```http
GET /empleado/{empleado_id}
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

### Proyectos

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

#### Listar proyectos (con filtros)
```http
GET /proyecto/?estado=Activo&presupuesto_min=10000&presupuesto_max=100000
```

#### Obtener proyecto por ID
```http
GET /proyecto/{proyecto_id}
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

#### Desasignar empleado de proyecto
```http
DELETE /proyecto/{proyecto_id}/desasignar/{empleado_id}
```

#### Listar empleados del proyecto
```http
GET /proyecto/{proyecto_id}/empleados
```

## Modelos de Datos

### Empleado
- `id`: Identificador único (auto-generado)
- `nombre`: Nombre del empleado
- `especialidad`: Área de especialización
- `salario`: Salario del empleado
- `estado`: Estado (Activo/Inactivo)

### Proyecto
- `id`: Identificador único (auto-generado)
- `nombre`: Nombre del proyecto (único)
- `descripcion`: Descripción del proyecto
- `presupuesto`: Presupuesto asignado
- `estado`: Estado (Activo/Inactivo)
- `gerente_id`: ID del empleado gerente

## Reglas de Negocio

1. **Validación de gerente**: Al crear un proyecto, el gerente debe existir en la base de datos
2. **Nombre único de proyecto**: No pueden existir dos proyectos con el mismo nombre
3. **Protección de eliminación**: No se puede eliminar un empleado que es gerente de algún proyecto
4. **Prevención de duplicados**: No se puede asignar el mismo empleado dos veces al mismo proyecto
5. **Validación de relaciones**: Al asignar/desasignar empleados, se valida que tanto el proyecto como el empleado existan

## Validaciones

- Estados permitidos: `Activo` o `Inactivo`
- Salario y presupuesto deben ser valores numéricos positivos
- Los nombres no pueden estar vacíos
- Validación de existencia de entidades antes de operaciones relacionales

## Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Solicitud inválida o regla de negocio violada
- `404 Not Found`: Recurso no encontrado
- `409 Conflict`: Conflicto 

## Ejemplos de Uso

### Crear un empleado y un proyecto

```bash
# 1. Crear empleado
curl -X POST "http://127.0.0.1:8000/empleado/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "especialidad": "Project Manager",
    "salario": 7000.0,
    "estado": "Activo"
  }'

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

# 3. Crear otro empleado para asignar al proyecto
curl -X POST "http://127.0.0.1:8000/empleado/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos López",
    "especialidad": "Desarrollador Mobile",
    "salario": 5500.0,
    "estado": "Activo"
  }'

# 4. Asignar empleado al proyecto
curl -X POST "http://127.0.0.1:8000/proyecto/1/asignar" \
  -H "Content-Type: application/json" \
  -d '{"empleado_id": 2}'
```

## Desarrollo

### Agregar nuevos endpoints

1. Crear función en el router correspondiente (`Empleado.py` o `Proyecto.py`)
2. Decorar con `@router.get/post/put/delete`
3. Definir modelos de respuesta en `models.py` si es necesario

### Agregar nuevas validaciones

Las validaciones se implementan usando:
- Validaciones de Pydantic en los modelos
- Validaciones de negocio en los endpoints (usando HTTPException)

## Pruebas

Para probar los endpoints, puedes usar:
- Swagger UI en `/docs`
- Herramientas como Postman, Insomnia o curl
- El archivo `test_main.http` (compatible con VS Code REST Client)

## Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de haber activado el entorno virtual
# y de haber instalado las dependencias
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# El puerto 8000 está ocupado, usa otro puerto
uvicorn main:app --reload --port 8001
```

### La base de datos no se crea
```bash
# Elimina la base de datos existente y reinicia
rm Proyectos.db
uvicorn main:app --reload
```

## Autor

Julian Steven Leal Martinez - 67001277

## Licencia

Este proyecto es parte de un ejercicio académico.

## Contacto

Para preguntas o sugerencias, contactar a: [jsleal77@ucatolica.edu.co]