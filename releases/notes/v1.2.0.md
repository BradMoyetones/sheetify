# Release v1.2.0 - Luz y Sombra 🌓

Esta versión no es solo un cambio de cara; es una reingeniería completa de cómo **Sheetify** gestiona su identidad y su estructura interna. Introducimos el esperado soporte para temas dinámicos y una arquitectura inspirada en los estándares modernos de diseño web.

### 🎨 Lo nuevo en Interfaz & UX:
- **Dynamic Theme Engine:** Implementación de un `ThemeManager` reactivo que permite alternar entre **Modo Oscuro** y **Modo Claro** en tiempo real.
- **Estética Inset (Shadcn Style):** Rediseño del layout principal utilizando un contenedor de contenido con bordes redondeados y márgenes negativos, logrando una profundidad visual premium.
- **Iconografía Inteligente:** Sistema de renderizado dinámico de SVGs que adapta el color de los iconos automáticamente según el tema activo.
- **Sidebar Refinada:** Nueva barra lateral minimalista con animaciones de colapso optimizadas y estados de hover persistentes.

### 🏗️ Mejoras de Arquitectura (Under the Hood):
- **Global Style Engine:** Migración de estilos inline a un motor de QSS centralizado basado en tokens. Ahora, cambiar un color en toda la app toma exactamente un segundo.
- **Componentización Total:** Refactorización de `FileItem` y `ZipGroup` como componentes independientes y desacoplados.
- **Centralización de Utils:** Nueva navaja suiza `app/core/utils.py` para la gestión de rutas de recursos y procesamiento de imágenes, eliminando redundancia de código.

### 🛠️ Roadmap Próximo:
- [ ] Implementación de filtros de columnas antes de la exportación.
- [ ] Sistema de logs en tiempo real para procesos de conversión extensos.
- [ ] Soporte para plantillas personalizadas de Excel.