---
name: desarrollador-frontend
description: Habilidad para desarrollar interfaces de usuario interactivas, responsivas y de alto rendimiento utilizando tecnologías web modernas.
---

# Desarrollador Frontend

Esta habilidad dota al agente de las capacidades de un Ingeniero Frontend profesional, enfocado en construir interfaces del lado del cliente que sean rápidas, accesibles, responsivas y modulares.

## Cuándo usar esta habilidad

Activa esta habilidad cuando debas:
- Programar la interfaz de usuario en frameworks como React, Next.js, Vue, Angular o HTML/JS vanilla.
- Gestionar el estado local o global de la aplicación cliente (ej. Redux, Pinia, Context API, Zustand).
- Consumir y conectar APIs del servidor (REST, GraphQL, WebSockets) en el cliente.
- Optimizar el rendimiento de renderizado en el navegador y asegurar la responsividad.

## Cómo usarla: Lineamientos de Desarrollo Frontend

### 1. Estructura de Componentes y Reutilización
- **Atomic Design / Componentes Modulares**: Diseña componentes pequeños y reutilizables. Evita archivos de componentes gigantescos de más de 300 líneas de código.
- **Props y Tipado**: Define contratos claros para tus componentes mediante TypeScript, PropTypes o validaciones en tiempo de desarrollo.

### 2. Gestión de Estado y Ciclo de Vida
- **Estado Local vs Global**: Mantén el estado lo más cercano posible a donde se usa. No guardes en el estado global (Redux, Zustand) datos que solo pertenecen a un componente aislado (ej. si un modal está abierto o cerrado).
- **Evitar Re-renders Innecesarios**: Memoriza componentes pesados (`React.memo`, `useMemo`, `useCallback`) y utiliza técnicas de optimización en listas largas (virtualización).

### 3. Consumo Eficiente y Seguro de APIs
- **Gestión de Carga y Error**: Muestra siempre estados de carga (skeletons o spinners) y maneja las fallas de red de manera elegante.
- **Seguridad**: Nunca guardes tokens de acceso sensibles (`JWT`, claves de API privadas) en el `localStorage`. Utiliza cookies HttpOnly o variables de estado volátiles en memoria.

### 4. Responsividad y Accesibilidad (A11y)
- **Mobile-First**: Escribe estilos comenzando por el diseño móvil y expandiéndolo hacia pantallas grandes mediante media queries (o prefijos de Tailwind como `md:`, `lg:`).
- **Accesibilidad**: Usa etiquetas HTML semánticas y atributos `aria-*` adecuados. Asegúrate de que todos los elementos interactivos sean navegables por teclado (`tabindex`, `focus states`).
