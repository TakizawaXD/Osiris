---
name: analista-seo
description: Habilidad para optimizar la estructura de la aplicación y el contenido para mejorar el posicionamiento en motores de búsqueda (SEO).
---

# Consultor y Analista SEO

Esta habilidad guía al agente en la implementación de mejores prácticas de SEO técnico y SEO On-Page para maximizar la visibilidad orgánica de la aplicación en los buscadores.

## Cuándo usar esta habilidad

Activa esta habilidad cuando debas:
- Diseñar la estructura HTML semántica de una página o sitio.
- Optimizar la velocidad de carga (Core Web Vitals) y rendimiento SEO.
- Configurar etiquetas meta de posicionamiento y redes sociales (Open Graph, Twitter Cards).
- Estructurar el sitemap, robots.txt o datos estructurados (JSON-LD Schema).

## Cómo usarla: Directrices de SEO Técnico y Semántica

### 1. Estructura HTML Semántica y Accesibilidad
- **Jerarquía de Encabezados**:
  - Debe haber **exactamente un solo** elemento `<h1>` por página (representa el título principal).
  - Los encabezados secundarios deben seguir una jerarquía estricta (`<h1>` -> `<h2>` -> `<h3>`). Nunca uses etiquetas de encabezados por su tamaño visual; usa estilos CSS para la apariencia.
- **Elementos Semánticos**: Utiliza etiquetas HTML5 adecuadas para dar significado al contenido: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`.

### 2. Metadatos y Social Media (SEO On-Page)
Cada página debe incluir las siguientes etiquetas en el `<head>`:
- **Title Tag**: Máximo 60 caracteres. Debe contener la palabra clave principal y ser descriptivo.
- **Meta Description**: Entre 120 y 160 caracteres. Debe persuadir al usuario a hacer clic (CTA sutil).
- **Open Graph (OG)**: Permite que el contenido se visualice correctamente al compartirse en Facebook, LinkedIn o WhatsApp (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`).
- **Twitter Cards**: Etiquetas equivalentes optimizadas para Twitter/X (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`).

### 3. Core Web Vitals (Rendimiento)
- **Carga de Imágenes**: Usa siempre atributos `alt` descriptivos en todas las imágenes. Añade lazy loading (`loading="lazy"`) a las imágenes fuera de la pantalla inicial. Define las dimensiones (`width` y `height`) para evitar el Cumulative Layout Shift (CLS).
- **Fuentes Web**: Utiliza precarga (`rel="preload"`) para las fuentes críticas para acelerar el renderizado del texto (evitar el parpadeo de fuente invisible).
