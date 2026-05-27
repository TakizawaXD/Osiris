---
name: arquitecto-software
description: Habilidad para definir la arquitectura de software, patrones de diseño, estructura de base de datos y flujos lógicos de la aplicación.
---

# Arquitecto de Software

Esta habilidad guía al agente en la toma de decisiones estructurales del software, asegurando escalabilidad, mantenibilidad, modularidad y rendimiento técnico.

## Cuándo usar esta habilidad

Activa esta habilidad al:
- Estructurar las carpetas y módulos de un nuevo proyecto o API.
- Diseñar el esquema de base de datos (relaciones, índices, colecciones).
- Elegir patrones de diseño (MVC, Arquitectura Hexagonal, Clean Architecture, Repository Pattern).
- Definir integraciones de sistemas, autenticación, flujos lógicos o APIs (RESTful, GraphQL).

## Cómo usarla: Lineamientos de Arquitectura

### 1. Estructura de Proyecto Limpia y Modular
- **Separación de Concernimientos (SoC)**: Divide la lógica de la aplicación en capas bien delimitadas:
  - **Capa de Presentación / Controladores**: Gestiona las peticiones HTTP y respuestas. No contiene lógica de negocio.
  - **Capa de Negocio / Servicios**: Contiene las reglas del negocio de la aplicación.
  - **Capa de Datos / Repositorios**: Gestiona la persistencia (consultas a base de datos, llamadas a APIs externas).
- **Modularidad**: Agrupa la funcionalidad por dominios (ej. `users/`, `billing/`, `products/`) en lugar de agrupar todo en carpetas genéricas como `controllers/` y `models/`.

### 2. Diseños de Base de Datos y Persistencia
- **Modelado de Datos**: Define esquemas claros con tipos de datos correctos, llaves primarias/foráneas y restricciones (null, unique).
- **Indexación**: Identifica los campos de búsqueda más frecuentes (ej. `email`, `slug`, `created_at`) e indica la creación de índices para optimizar consultas.
- **Normalización vs Desnormalización**: En SQL, mantén las tablas normalizadas (hasta 3NF). En NoSQL (MongoDB), desnormaliza solo cuando el rendimiento de lectura lo justifique y los datos no cambien frecuentemente.

### 3. Diseño de APIs RESTful
- **Convención de Nombres**: Usa sustantivos en plural para las rutas (ej. `/api/v1/products`, no `/api/v1/getProduct`).
- **Métodos HTTP**:
  - `GET`: Obtener recursos (debe ser idempotente).
  - `POST`: Crear nuevos recursos.
  - `PUT`: Reemplazar un recurso existente.
  - `PATCH`: Modificar parcialmente un recurso.
  - `DELETE`: Eliminar un recurso.
- **Códigos de Estado HTTP**:
  - `200 OK` / `201 Created` para éxito.
  - `400 Bad Request` / `401 Unauthorized` / `403 Forbidden` / `404 Not Found` para errores de cliente.
  - `500 Internal Server Error` para fallos del servidor.

### 4. Registro de Decisiones de Arquitectura (ADR)
Documenta las decisiones críticas bajo el siguiente formato simple en markdown:
- **Título**: ADR [Número]: [Decisión]
- **Contexto**: ¿Qué problema estamos resolviendo? ¿Qué alternativas existen?
- **Decisión**: ¿Qué alternativa elegimos y por qué?
- **Consecuencias**: ¿Cuáles son las ventajas y desventajas de esta elección?
