---
name: convertidor-imagenes-ui
description: Habilidad para procesar imágenes, capturas y bocetos del usuario para rediseñarlos estéticamente con generate_image o convertirlos a código limpio.
---

# Convertidor de Imágenes a UI (Image-to-Code & Design Refinement)

Esta habilidad se encarga de analizar fotos, bocetos hechos a mano, capturas de pantalla o maquetas (mockups) que compartas, para:
1. Rediseñarlos estéticamente usando la herramienta de IA `generate_image` adaptándolos al contexto de desarrollo del proyecto.
2. Traducir la distribución, componentes y elementos visuales de la imagen en código web estructurado, semántico y responsivo (HTML, CSS, React, Tailwind, etc.).

---

## Cuándo usar esta habilidad

Activa esta habilidad cuando el usuario:
1. Suba o comparta una imagen, boceto o captura de pantalla y solicite: *"haz esto en código"*, *"rediseña esta captura"* o *"convierte esta foto a una página premium"*.
2. Solicite generar imágenes de interfaz (UI), banners, logos o componentes visuales de referencia para el desarrollo web.

---

## Cómo usarla

### 1. Flujo de Análisis de Imagen a Código (Image-to-Code)
Al recibir una imagen, realiza un análisis sistemático antes de codificar:
1. **Layout y Estructura:** Identifica la rejilla (Bento Grid, Flexbox, asimetría) y zonas principales (Hero header, Sidebar, Footer).
2. **Componentes clave:** Cataloga inputs, botones, tarjetas, modales y charts.
3. **Estilo visual original:** Identifica la paleta de colores, bordes (redondeados, afilados), sombras y fuentes.
4. **Traducción Semántica:** Escribe el código HTML5/CSS estructurado mapeando cada elemento visual analizado, aplicando transiciones suaves de `150ms-300ms` en los hovers.

### 2. Refinamiento Estético con `generate_image` (Image-to-Image)
Si deseas generar una propuesta de diseño premium de alta fidelidad basada en la imagen del usuario:
1. Usa la herramienta `generate_image` pasando la ruta de la imagen original en el array `ImagePaths`.
2. Escribe un prompt que describa la transformación estética y el estilo premium deseado.
3. **Regla de Prompting:** Usa términos de diseño moderno (Glassmorphism, gradientes HSL curados, diseño limpio, modo oscuro elegante) y prohíbe marcos de dispositivos (device mockups) a menos que se soliciten explícitamente.

**Ejemplo de llamada:**
```json
{
  "Prompt": "Sleek premium SaaS landing page, dark mode interface, glassmorphism card components, vibrant HSL gradients in royal blue and neon violet, elegant layout, ultra-clean web design",
  "ImageName": "saas_landing_redesign",
  "ImagePaths": ["/absolute/path/to/user_sketch.png"]
}
```

### 3. Checklist de Entrega
- [ ] ¿El código resultante es responsivo y fiel a la jerarquía de la imagen?
- [ ] ¿Se han reemplazado los placeholders y emojis de la imagen por SVGs reales e imágenes generadas?
- [ ] ¿Los botones e inputs tienen el cursor correcto (`cursor-pointer`) y estilos de hover interactivos?
