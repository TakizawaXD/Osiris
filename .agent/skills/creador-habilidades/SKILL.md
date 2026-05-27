---
name: creador-habilidades
description: Habilidad para crear nuevas habilidades de Antigravity en español y diseñar páginas web profesionales usando ui-ux-pro-max.
---

# Creador de Habilidades y Páginas Web (ui-ux-pro-max)

Esta habilidad permite al agente crear de manera automatizada o manual nuevas habilidades de Antigravity en español, así como construir páginas web de alta calidad estética utilizando la inteligencia de diseño de `ui-ux-pro-max`.

---

## Cuándo usar esta habilidad

Utiliza esta habilidad cuando el usuario solicite:
1. **Crear una nueva habilidad** en el workspace actual o de forma global (ej. "crea una habilidad para validar APIs", "crear habilidad en español para X").
2. **Construir, diseñar o mejorar páginas web** o interfaces de usuario, requiriendo un sistema de diseño premium, paletas de colores armónicas y tipografías curadas.

---

## Cómo usarla

### Parte 1: Creación de Nuevas Habilidades (en Español)

Las habilidades de Antigravity son paquetes de instrucciones que extienden el comportamiento del agente. Para crear una habilidad en español, sigue las siguientes pautas.

#### Estructura de una habilidad:
Cada habilidad debe ser una carpeta dentro de:
- **Específica del Workspace**: `.agents/skills/<nombre-habilidad>/`
- **Global (Todos los Workspaces)**: `~/.gemini/antigravity/skills/<nombre-habilidad>/`

El archivo principal obligatorio es `SKILL.md`, el cual debe llevar un frontmatter YAML al principio.

#### Método A: Creación Automatizada (Recomendado)
Puedes ejecutar el script helper provisto en esta habilidad para generar la estructura:

```bash
python3 .agents/skills/creador-habilidades/scripts/creador.py \
  --nombre "nombre-habilidad" \
  --descripcion "Descripción clara para que el agente la autodescubra" \
  --titulo "Título de la Habilidad" \
  --cuando "Cuándo debe el agente usar esta habilidad..." \
  --como "Pasos detallados de cómo usarla..."
```

*Nota: Si ejecutas el script sin argumentos, se iniciará un asistente interactivo en la terminal.*

#### Método B: Creación Manual
Si decides crearla manualmente, asegúrate de cumplir con el siguiente formato en `SKILL.md`:

```markdown
---
name: nombre-de-habilidad
description: Descripción en tercera persona con palabras clave para el autodescubrimiento del agente.
---

# Nombre de la Habilidad

## Cuándo usar esta habilidad

- Detallar las condiciones exactas y palabras clave bajo las cuales el agente debe activar esta habilidad.

## Cómo usarla

- Instrucciones paso a paso, checklist de calidad y ejemplos de código.
```

---

### Parte 2: Creación de Páginas Web con `ui-ux-pro-max`

Para construir páginas web, debes apoyarte en la habilidad `ui-ux-pro-max` instalada en este workspace para generar sistemas de diseño a medida antes de codificar.

#### Flujo de Trabajo para Páginas Web:

1. **Analizar los requerimientos del usuario:**
   Identifica el tipo de producto (SaaS, e-commerce, spa, portafolio), la industria, el stack tecnológico (por defecto `html-tailwind`) y palabras clave de estilo (minimalista, dark mode, moderno).

2. **Generar el Sistema de Diseño (Obligatorio):**
   Ejecuta el script de búsqueda de `ui-ux-pro-max` para obtener una recomendación con base científica de colores, tipografías y anti-patrones:
   ```bash
   python3 .agents/skills/ui-ux-pro-max/scripts/search.py "<tipo_producto> <industria> <estilo>" --design-system -p "Nombre del Proyecto" --persist
   ```
   *Esto creará el archivo `design-system/MASTER.md` en el workspace.*

3. **Revisar e implementar:**
   Lee el archivo `design-system/MASTER.md` generado. Implementa la interfaz usando los colores HSL indicados, fuentes de Google Fonts sugeridas y transiciones suaves.

4. **Lista de comprobación de calidad (Pre-Delivery Checklist):**
   - **Iconos:** Nunca uses emojis como iconos de interfaz. Usa SVGs consistentes (Heroicons o Lucide).
   - **Interacción:** Agrega `cursor-pointer` a elementos cliqueables y transiciones de 150-300ms en los hovers.
   - **Alineación:** Usa contenedores limpios y consistentes (`max-w-6xl` o `max-w-7xl`).
