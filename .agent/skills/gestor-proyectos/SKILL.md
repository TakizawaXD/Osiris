---
name: gestor-proyectos
description: Habilidad para organizar tareas, hitos del proyecto, estimar tiempos y estructurar el roadmap de desarrollo de la aplicación.
---

# Gestor de Proyectos (Project Manager)

Esta habilidad dota al agente de técnicas ágiles de gestión de proyectos, permitiéndole organizar el trabajo, priorizar el backlog y mantener una comunicación estructurada sobre el progreso.

## Cuándo usar esta habilidad

Activa esta habilidad al:
- Organizar el roadmap de desarrollo de una nueva aplicación o característica.
- Estimar tiempos de entrega o dividir requerimientos complejos en tareas accionables.
- Priorizar el backlog del producto mediante marcos ágiles (Scrum / Kanban).

## Cómo usarla: Planificación y Gestión Ágil

### 1. Historias de Usuario (User Stories) y Criterios de Aceptación
Divide los requisitos funcionales del usuario en historias escritas bajo el formato estándar:
- **Narrativa**:
  - **Como** [tipo de usuario],
  - **quiero** [realizar una acción],
  - **para** [obtener un beneficio o valor de negocio].
- **Criterios de Aceptación (BDD - Given/When/Then)**:
  - **Dado que** [contexto inicial],
  - **cuando** [el usuario realiza una acción],
  - **entonces** [se produce el resultado esperado].

### 2. Priorización del Backlog (Matriz de Impacto vs Esfuerzo)
Clasifica las tareas para maximizar el retorno de valor en cada iteración (Sprint):
- **Victorias Rápidas (Quick Wins)**: Alto impacto y bajo esfuerzo. (Prioridad Máxima).
- **Proyectos Clave (Major Projects)**: Alto impacto y alto esfuerzo. (Requieren planificación).
- **Rellenos (Fill-ins)**: Bajo impacto y bajo esfuerzo. (Hacer cuando haya tiempo libre).
- **Tareas Inútiles (Thankless Tasks)**: Bajo impacto y alto esfuerzo. (Descartar o postergar).

### 3. Gestión de Riesgos y Mitigación
Identifica los cuellos de botella técnicos o de negocio comunes:
- **Riesgo**: Alcance no delimitado (scope creep). -> **Mitigación**: Congelar requisitos al inicio del sprint y rechazar cambios intermedios.
- **Riesgo**: Retrasos por integraciones de terceros. -> **Mitigación**: Crear contratos de API e implementar mocks de inmediato para no bloquear el desarrollo del frontend.
