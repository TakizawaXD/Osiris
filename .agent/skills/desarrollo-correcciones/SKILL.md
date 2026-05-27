---
name: desarrollo-correcciones
description: Habilidad para realizar el desarrollo de código limpio, refactorizaciones y correcciones de errores (bugs) en la aplicación.
---

# Desarrollador y Corrector de Aplicaciones

Esta habilidad está enfocada en el desarrollo de software bajo estrictos estándares de ingeniería de software, enfocándose en la resolución de bugs, refactorización y código limpio.

## Cuándo usar esta habilidad

Activa esta habilidad al:
- Implementar nuevas funcionalidades de programación (backend o frontend).
- Investigar la causa raíz de un error, bug o comportamiento inesperado.
- Refactorizar código existente para mejorar su legibilidad, eficiencia o mantenimiento.
- Escribir scripts utilitarios, configuraciones de compilación o de despliegue.

## Cómo usarla: Estándares de Programación

### 1. Código Limpio y Principios SOLID
- **S - Responsabilidad Única**: Cada clase, función o módulo debe tener una sola razón para cambiar (hacer una sola cosa bien).
- **KISS (Keep It Simple, Stupid)**: Escribe el código de la manera más simple posible. Evita la sobre-ingeniería.
- **DRY (Don't Repeat Yourself)**: Si detectas lógica duplicada, extráela a una función o módulo utilitario reutilizable.
- **Autodocumentación**: Nombra tus variables, clases y funciones con verbos y sustantivos claros y descriptivos (ej. `calculate_monthly_revenue` en lugar de `calcRev`). Evita comentarios redundantes que solo expliquen *qué* hace el código; escribe comentarios para explicar *por qué* se tomó una decisión compleja.

### 2. Gestión de Errores y Excepciones
- **Evita capturas genéricas (Bare Excepts)**: Nunca captures excepciones sin especificar el tipo (ej. en Python usa `except ValueError:` en lugar de un `except:` genérico).
- **Falla Rápido (Fail-Fast)**: Valida las condiciones de entrada al principio de tus funciones (guard clauses) y lanza excepciones inmediatamente si los parámetros son inválidos.
- **Manejo de Errores en UI**: Nunca dejes que la aplicación se congele o muestre una pantalla blanca. Implementa límites de error (Error Boundaries) y muestra mensajes amigables con opciones de recuperación (ej. "Reintentar").

### 3. Proceso Sistemático de Depuración (Debugging)
Cuando te enfrentes a un error reportado:
1. **Reproducción**: Intenta aislar y reproducir el error mediante un script mínimo o caso de prueba.
2. **Localización**: Analiza el stack trace (traza de error) desde la base hasta el punto donde ocurre el fallo en tu propio código.
3. **Análisis**: Comprueba el estado de las variables y las condiciones en ese punto (usando logs estructurados o depurador).
4. **Solución**: Aplica una corrección que resuelva el error de raíz, no solo los síntomas. Asegúrate de que no introduzca efectos colaterales (regresiones).
