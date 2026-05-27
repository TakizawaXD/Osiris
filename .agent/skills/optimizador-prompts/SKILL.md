---
name: optimizador-prompts
description: Habilidad para optimizar y refinar prompts de forma técnica. Se utiliza para resolver errores de autocompletado y mejorar la precisión de los modelos de IA.
---

# Optimizador de Prompts y Autocompletado

Esta habilidad se encarga de reescribir y optimizar las solicitudes (prompts) del usuario, adaptándolas a formatos altamente estructurados y técnicos para evitar alucinaciones, solucionar errores de autocompletado (ej. Copilot, Cursor, Supermaven) y obtener respuestas de código ultra-precisas.

---

## Cuándo usar esta habilidad

Activa esta habilidad cuando el usuario:
1. Solicite: *"mejora mi prompt"*, *"optimiza esta instrucción"* o *"haz este prompt más técnico"*.
2. Reporte errores de autocompletado en su editor de código (código cortado, sugerencias basura, bucles de autocompletado).
3. Requiera estructurar una tarea compleja para que otra IA (como Copilot o un agente autónomo) la ejecute de manera perfecta.

---

## Cómo usarla

### 1. Fórmula de Optimización de Prompts (Prompt Técnico)
Cuando el usuario te dé una instrucción informal, conviértela en un **Prompt Técnico Estructurado** siguiendo esta plantilla:

```markdown
# Petición Técnica Optimizada

**[Rol Profesional]**
Actúa como un experto en [Tecnología/Paradigma] enfocado en [Rendimiento/Seguridad/etc.].

**[Contexto del Sistema]**
- **Arquitectura:** [Ej. Frontend Modular, Backend Hexagonal]
- **Entorno:** [Ej. Node.js v20, React v18]
- **Archivos Relacionados:** `[lista_de_archivos]`

**[Objetivo Principal]**
[Descripción unívoca y clara del resultado esperado, sin ambigüedades]

**[Restricciones Técnicas]**
- [ ] Aplicar principios SOLID.
- [ ] Tipado estricto (TypeScript/Pydantic).
- [ ] Sin dependencias externas innecesarias.

**[Contrato de Entrada/Salida]**
- **Input:** `[Estructura de datos]`
- **Output:** `[Estructura de datos]`

**[Instrucciones de Completado (Firma)]**
[Firma exacta de la función o clase para iniciar el código]
```

### 2. Resolución de Errores de Autocompletado (IDE Completions)
Si el autocompletado de su IDE (GitHub Copilot, Cursor, etc.) está fallando o sugiriendo código erróneo, provéele una **Guía de Anclaje de Contexto**:

1. **Limpieza de Pestañas Abiertas:** Aconseja cerrar las pestañas del editor que no tengan relación con el archivo actual para no contaminar el contexto del modelo del IDE.
2. **Comentarios de Anclaje Semántico (SACS):** Enséñale a escribir la cabecera del archivo o función usando comentarios estructurados antes de activar el autocompletado:
   ```typescript
   // @context: usa types de './types/api.ts'
   // @rules: función pura, manejo estricto de errores con Try/Catch
   // @output: retorna Promise<UserResponse>
   ```
3. **Inicio de Firma Explícito:** Escribir los primeros caracteres del tipo de retorno o de la firma de la función para forzar al modelo de autocompletado a alinearse con el estilo del proyecto.

### 3. Checklist de Validación del Prompt
Antes de entregar el prompt mejorado al usuario, verifica:
- [ ] ¿Tiene delimitadores claros para el código y el contexto?
- [ ] ¿Evita palabras vagas como "eficiente", "rápido" o "moderno" y las reemplaza por métricas técnicas (ej. O(1), no-bloqueante)?
- [ ] ¿Especifica el manejo de errores esperado?
