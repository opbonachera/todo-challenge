# To-Do Challenge

API Rest construida con DRF y Django para la gestión de tareas.
Ofrece autenticación con JWT, despliegue con Docker, logs y tests. Base de datos es sqlite3 por simplicidad (no persiste entre entornos).

----
## Funcionalidades
- Registro, logueo y deslogueo de usuarios de forma segura con JWT.
- Creación, actualización, eliminación de tareas.
- Descripción completa y realista de una tarea y su información asociada.
- Obtención de tarea y listado de tareas con filtros y ordenamiento. 
- Flexibilidad de filtrado aprovechando Django Filters tanto para consultas exactas como aproximadas.
- Logs completos útiles para asegurar la observabilidad de la aplicación. 
- Pruebas unitarias e integrales.
- Respuestas homogéneas de la API utilizando drf-standardized-errors.
## Requisitos previos

Este proyecto utiliza **Docker** y **Docker Compose** para simplificar la instalación y ejecución del entorno de desarrollo.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuración inicial
### 1. Cloná el repositorio: 
```bash
git clone https://github.com/opbonachera/todo-challenge
cd todo-challenge
```

## Construcción y ejecución 
### 1. Construí las imagenes

```bash
  docker-compose build
```

### 2. Levantá los contenedores
```bash 
docker-compose up
```
## Variables de entorno
Para correr el proyecto, tenés que agregar en tu archivo .env las siguientes variables de entorno:

`SECRET_KEY`
`DEBUG`
`ALLOWED_HOSTS`
`DB_ENGINE`
`DB_NAME`
`CORS_ALLOW_ALL_ORIGINS`
`CORS_ALLOWED_ORIGINS`

Para mayor referencia, mirá el archivo env-sample. 
## Documentación de la API
### Modulo de autenticación
#### Registro de usuario
```http
  POST /api/v1/register
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`   | `string` | **Requerido**. |
| `password`   | `string` | **Requerido**. |
| `email`   | `string` | **Opcional**  |
| `first_name`   | `string` | **Opcional**.  |
| `last_name`   | `string` | **Opcional**. |

#### Logout
```http
  POST /api/v1/logout
```

#### Login
```http
  POST /api/v1/login
```
[Request BODY en formato JSON]
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`   | `string` | **Requerido**. |
| `password`   | `string` | **Requerido**. |

#### Regenerar token
```http
  POST /api/v1/refresh-token
```
[Request BODY en formato JSON]
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `token`   | `string` | **Requerido**. |


### Módulo de tareas
Todas las solicitudes deben incluir el encabezado `Authorization` con un token válido, con el formato:

[Request HEADER]
| Encabezado | Valor | Descripción |
| :--- | :--- | :--- |
| `Authorization` | `Token <tu_token>` | **Requerido**. El token de acceso emitido para el usuario. |

#### Listar tareas

```http
  GET /api/v1/task?filtro1=valr&filtro2=valor
```
[Query params en URL]
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `filter` | `string` | **Opcional**. Filtra los resultados por distintos filtros (*)| 
| `ordering` | `string` | **Opcional**.  Ordena los resultados por created_at, priority o title. Se puede usar - para ordenar de forma descendente (por ejemplo, -created_at). |

------
(*) Filtros soportados
- Text: busqueda libre sobre titulo o descripción de la tarea
```http
  GET /api/v1/task?text=Django
```
- Priority: Soporta exact, gte o lte. 
```http
  GET /api/v1/task?priority=2
  GET /api/v1/task?priority__gte=1&priority__lte=3
```
- Title / Description: búsquedas parciales y exactas.
icontains: contiene (insensible a mayúsculas).
startswith / endswith: empieza o termina con.
```http
  GET /api/v1/task?title__icontains=plan
  GET /api/v1/task?description__startswith=Urgente
```
- Tags: buscar tareas que contengan un tag específico dentro de la lista de tags.
```http
  GET /api/v1/task?tags__icontains=backend
```
- Completed: estado de finalización (true/false)
```http
  GET /api/v1/task?completed=true
```
- Fecha de creación: Permite filtrar por fecha exacta (YYYY-MM-DD), devolviendo todas las tareas creadas en ese día.
También acepta filtros de rango (gte, lte) con fechas.
```http
  GET /api/v1/tasks?created_at=2025-09-26
  GET /api/v1/tasks?created_at__gte=2025-09-20&created_at__lte=2025-09-26
```
- Si se envía un datetime completo (YYYY-MM-DDTHH:MM:SSZ), se realizará la comparación exacta contra la marca de tiempo.

- Fecha de actualización: Filtrar por rango de actualización usando gte y lte.
```http
  GET /api/v1/tasks?updated_at__gte=2025-09-01
  GET /api/v1/tasks?updated_at__lte=2025-09-26
```
------
#### Crear tarea
```http
  POST /api/v1/task
```
[Request BODY en formato JSON]
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`   | `string` | **Requerido**. |
| `descripcion`   | `string` | **Opcional**. Máximo de 255 caracteres. |
| `priority`   | `string` | **Opcional** Rango del 1 al 5. |
| `tags`   | `string` | **Opcional**. Formato "tag1,tag2,tag3" |

#### Eliminar tarea

```http
  DELETE /api/v1/task/<taskId>
```
#### Actualizar tarea (PUT)
```http
  PUT /api/v1/task/<taskId>
```
[Request BODY en formato JSON]
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`   | `string` | **Requerido**. |
| `descripcion`   | `string` | **Opcional**. Máximo de 255 caracteres. |
| `priority`   | `string` | **Opcional** Rango del 1 al 5. |
| `tags`   | `string` | **Opcional**. Formato "tag1,tag2,tag3" |

#### Actualizar tarea parcialmente (PATCH)
```http
  PATCH /api/v1/task/<taskId>
```
[Request BODY en formato JSON]
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`   | `string` | **Opcional**. |
| `descripcion`   | `string` | **Opcional**. Máximo de 255 caracteres. |
| `priority`   | `string` | **Opcional** Rango del 1 al 5. |
| `tags`   | `string` | **Opcional**. Formato "tag1,tag2,tag3" |

## Base de datos
---
El proyecto utiliza SQLite3 como base de datos, montada en un volumen local (./db.sqlite3:/app/db.sqlite3) para garantizar persistencia fuera del contenedor. Esto simplifica la ejecución y evita perder datos al reiniciar.

En un entorno real de producción se reemplazaría por PostgreSQL o MySQL en un contenedor independiente, pero para un proyecto de evaluación y simplicidad se optó por SQLite.