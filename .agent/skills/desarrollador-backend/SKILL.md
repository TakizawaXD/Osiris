---
name: desarrollador-backend
description: Habilidad para diseñar y desarrollar servidores, APIs, bases de datos y la lógica del negocio de la aplicación.
---

# Desarrollador Backend

Esta habilidad capacita al agente para actuar como un Ingeniero Backend profesional, encargado de construir lógica de servidor segura, APIs eficientes, integraciones de bases de datos sólidas y servicios escalables.

## Cuándo usar esta habilidad

Activa esta habilidad cuando debas:
- Programar la lógica del servidor (Node.js, Python, Go, Java, PHP, etc.).
- Diseñar, estructurar y optimizar endpoints de API (RESTful, GraphQL, gRPC).
- Conectar, consultar o migrar bases de datos (SQL y NoSQL).
- Implementar autenticación, autorización, encriptación y medidas de seguridad del lado del servidor.

## Cómo usarla: Lineamientos de Desarrollo Backend

### 1. Validación de Datos y Seguridad (Defensa en el Servidor)
- **Validación de Entradas**: Nunca confíes en los datos del cliente. Valida todos los parámetros de entrada (`req.body`, `req.query`, `req.params`) utilizando esquemas estrictos (ej. Zod, Joi, Pydantic).
- **Sanitización**: Limpia las entradas para prevenir inyecciones SQL, NoSQL o ataques XSS.
- **Autenticación y Autorización**: Implementa estándares de la industria como JWT (Json Web Tokens), OAuth2 o sesiones basadas en cookies seguras. Usa control de acceso basado en roles (RBAC).

### 2. Optimización de Consultas a Bases de Datos
- **Evitar el problema N+1**: Diseña tus consultas (usando ORMs como Prisma, Sequelize, Mongoose o SQL directo) para traer los datos relacionados en una sola consulta mediante joins o agregaciones.
- **Transacciones**: Usa transacciones de base de datos cuando realices múltiples operaciones de escritura que deban completarse juntas (operaciones atómicas, ej. crear un pedido y restar stock).

### 3. Manejo de Errores Centralizado y Registro (Logging)
- **Middleware de Errores**: Implementa un manejador de errores global para capturar excepciones no controladas, registrar el fallo detalladamente y responder al cliente con un formato JSON limpio y sin exponer detalles internos del servidor (stack traces).
- **Logs Estructurados**: Registra eventos importantes con niveles de severidad (`INFO`, `WARN`, `ERROR`) indicando la marca de tiempo, el endpoint y el ID de correlación de la solicitud.

### 4. Rendimiento y Escalabilidad
- **Paginación**: Nunca devuelvas listas completas de la base de datos. Implementa paginación basada en cursor u offset por defecto en todos los endpoints de consulta de colecciones.
- **Caché**: Identifica consultas pesadas que cambien poco (catálogos de productos, configuraciones) e impleméntales almacenamiento en caché (ej. Redis).
