# Ejemplos de Uso de la API

## 🚀 Inicio Rápido

### Crear un Empleado

```bash
curl -X POST "http://127.0.0.1:8000/empleado/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "especialidad": "Backend Developer",
    "salario": 5000,
    "estado": "Activo"
  }'
```

### Crear un Proyecto

```bash
curl -X POST "http://127.0.0.1:8000/proyecto/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Sistema CRM",
    "descripcion": "Sistema de gestión de clientes",
    "presupuesto": 50000,
    "estado": "Activo",
    "gerente_id": 1
  }'
```

### Listar Empleados con Filtros

```bash
curl "http://127.0.0.1:8000/empleado/?especialidad=Backend&estado=Activo"
```

### Listar Proyectos por Presupuesto

```bash
curl "http://127.0.0.1:8000/proyecto/?presupuesto_min=10000&presupuesto_max=100000"
```

### Asignar Empleado a Proyecto

```bash
curl -X POST "http://127.0.0.1:8000/proyecto/1/asignar" \
  -H "Content-Type: application/json" \
  -d '{"empleado_id": 2}'
```

## 📊 Respuestas Ejemplo

### Empleado Creado
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "especialidad": "Backend Developer",
  "salario": 5000.0,
  "estado": "Activo"
}
```

### Proyecto con Relaciones
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
    "especialidad": "Backend Developer",
    "salario": 5000.0,
    "estado": "Activo"
  },
  "empleados": []
}
```
