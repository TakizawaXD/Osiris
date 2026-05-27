---
name: disenador
description: Habilidad para diseñar interfaces de usuario (UI), crear mockups, y definir la identidad visual y sistemas de diseño de la aplicación.
---

# Diseñador UI/UX

Esta habilidad dota al agente de las capacidades de un Diseñador UI/UX profesional, enfocado en crear interfaces estéticas, usables, consistentes y de alto impacto visual.

## Cuándo usar esta habilidad

Activa esta habilidad cuando debas:
- Definir la identidad visual, paleta de colores o tipografías de un proyecto.
- Crear o mejorar la interfaz de usuario (UI) de una vista, componente o página completa.
- Estructurar el layout (bento grid, bento box, layouts responsivos, etc.) y la jerarquía visual.
- Diseñar estados interactivos (hovers, transiciones, animaciones, loaders).

## Cómo usarla: Principios de Diseño Profesional

### 1. Sistema de Rejilla y Espaciado (Grid & Spacing)
- **Regla del 8px/4px**: Todo el espaciado (padding, margin, gap, altos y anchos) debe ser múltiplo de 8px (o 4px para elementos muy pequeños). En Tailwind: `p-2` (8px), `p-4` (16px), `p-6` (24px), `gap-4` (16px), etc.
- **Bento Grid**: Utiliza distribuciones de rejilla con tarjetas de bordes redondeados pronunciados (`rounded-2xl` o `rounded-3xl`) y bordes sutiles para crear interfaces modernas y organizadas.

### 2. Jerarquía Visual y Tipografía
- **Emparejamiento Tipográfico**: Usa una fuente Serif elegante para títulos (ej. *Playfair Display* o *Cormorant Garamond*) y una Sans-Serif limpia para el cuerpo (ej. *Inter* o *Montserrat*).
- **Escala de Tamaños**: Asegura contrastes claros en tamaño y peso de texto. Ejemplo:
  - H1: `text-4xl md:text-5xl font-extrabold tracking-tight`
  - H2: `text-2xl md:text-3xl font-bold`
  - Cuerpo: `text-base text-slate-600 dark:text-slate-300 font-normal leading-relaxed`

### 3. Teoría del Color y Contraste (Accesibilidad WCAG AA)
- **Regla 60-30-10**:
  - **60% Color Dominante**: Fondos limpios y amplios (blancos cálidos, grises oscuros o negros OLED).
  - **30% Color Secundario**: Estructura, tarjetas, bordes, textos principales.
  - **10% Color de Acento (CTA)**: Botones de acción principal, indicadores, elementos destacados (ej. un color vibrante con buena legibilidad).
- **Contraste de Texto**: Asegura un contraste mínimo de **4.5:1** para texto normal y **3:1** para texto grande. Evita grises claros sobre fondos blancos.

### 4. Estados Interactivos y Micro-animaciones
- **Transiciones Suaves**: Todo elemento interactivo (botones, tarjetas, enlaces) debe llevar transiciones suaves. Añade siempre `transition-all duration-300 ease-in-out`.
- **Hovers Estables**: Los hovers no deben cambiar el tamaño del contenedor principal para evitar saltos en la interfaz (layout shift). Usa cambios de color de fondo, opacidad de bordes o elevación sutil de sombra (`hover:-translate-y-0.5 hover:shadow-lg`).
- **Cursor**: Añade siempre la clase `cursor-pointer` a todo elemento cliqueable.

### 5. Integración con `ui-ux-pro-max`
- Antes de diseñar, busca en la biblioteca de estilos de `ui-ux-pro-max` el estilo recomendado para la industria del proyecto (ej. Glassmorphism para Fintech, Biophilic para Wellness).
