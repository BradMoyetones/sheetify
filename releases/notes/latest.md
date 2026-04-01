# Release v1.2.1 - Fluidez Absoluta: Sidebar Patch 🧊

Esta pequeña pero significativa actualización se enfoca exclusivamente en la experiencia táctil y visual de la navegación principal.

### ✨ Mejoras de UX:
- **Interpolación Sincrónica:** Se implementó `QParallelAnimationGroup` para coordinar el `minimumWidth` y el `maximumWidth` de la sidebar.
- **Adiós al "Jump-Cut":** Corregido el error de layout donde la apertura de la sidebar se sentía brusca. Ahora el desplazamiento es suave (OutCubic) en ambas direcciones.