---
name: pruebas-calidad
description: Habilidad para planificar y ejecutar pruebas de software funcionales, unitarias y de integración para asegurar la calidad de la aplicación.
---

# Ingeniero de Pruebas de Calidad (QA)

Esta habilidad capacita al agente para diseñar planes de prueba robustos, validar la experiencia de usuario (UX) en diferentes entornos y reportar bugs con precisión.

## Cuándo usar esta habilidad

Activa esta habilidad al:
- Diseñar casos de prueba funcionales para nuevas historias de usuario.
- Validar el comportamiento de la interfaz ante entradas inválidas o flujos alternativos.
- Redactar scripts de pruebas unitarias o de integración.
- Realizar pruebas de regresión antes de un despliegue importante.

## Cómo usarla: Control de Calidad Riguroso

### 1. Tipos de Pruebas a Diseñar e Implementar
- **Pruebas Unitarias**: Validan la lógica de funciones o componentes aislados. Usan mocks para bases de datos o llamadas HTTP externas.
- **Pruebas de Integración**: Validan la comunicación entre diferentes módulos (ej. validar que al guardar un registro en la base de datos se envíe la llamada al servicio de correo).
- **Pruebas de Extremo a Extremo (E2E)**: Simulan interacciones completas del usuario en un navegador real utilizando herramientas como Playwright, Cypress o Selenium.

### 2. Plantilla de Caso de Prueba Funcional
Para documentar escenarios de prueba, utiliza este formato estructurado:
- **ID / Nombre**: QA-[Número]: [Nombre descriptivo]
- **Precondiciones**: Estado inicial requerido (ej. "Usuario logueado con plan básico").
- **Pasos a Seguir**: Secuencia exacta de acciones.
- **Datos de Entrada**: Parámetros o valores ingresados.
- **Resultado Esperado**: Lo que la aplicación debería hacer si funciona correctamente.

### 3. Plantilla de Reporte de Bug
Cuando encuentres un fallo, repórtalo con el máximo detalle técnico:
- **Título**: [Módulo] - [Descripción concisa del fallo]
- **Severidad**: Crítica (caída del sistema) / Alta (flujo bloqueado) / Media (funcionalidad parcial) / Baja (estética).
- **Pasos para Reproducir**: Lista numerada de acciones desde el inicio.
- **Comportamiento Actual**: Qué hace la app en el paso final (añade mensajes de log o capturas si aplica).
- **Comportamiento Esperado**: Qué debería hacer en su lugar.
- **Entorno**: Sistema operativo, navegador, resolución de pantalla.
