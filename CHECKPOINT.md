# Checkpoint - Portfolio WEB

## Estado actual (guardado antes de reiniciar la notebook)

- Web publicada en GitHub Pages: https://saalaura-bit.github.io/ls/
- Repo publico: `saalaura-bit/ls` (rama main), push al dia.
- Renombrado 04/09/2026: repo `portfolio-web` -> `ls` (Laura no quiere la palabra "portfolio" en la URL; usa su logo LS). URL vieja `/portfolio-web/` ya no responde (404).
- Deploy local temporal: ruta vieja de otra pc, verificar carpeta actual del repo clonado.

## Cambios ya hechos y publicados

- Contact + footer en **modo oscuro** (fondo negro `--ink`, texto claro).
- Contact: titulo, texto y los 4 logos en el mismo row (`.contact-info`).
- Icono del telefono (azul) con el logo en **blanco** para que se vea en oscuro.
- Nav flotante: boton "Menu / Menu" desplegable con Home/QA/BA/SM/Mentoring.
- Footer sin columna Contact ni social icons; barra inferior con privacy.html.
- `privacy.html` creado (EN/ES).
- Contacto real: saalaura@gmail.com, +598 97 496 335, LinkedIn, Montevideo.
- Bilingue EN/ES con `<span class="en">` / `<span class="es">`.

## Pendiente al reabrir

1. Confirmar que en Chrome se ve el modo oscuro (el usuario limpiara cache / reiniciara).
2. Seguir con los ajustes de oscuro que el usuario pidio ("Contact en los iconos" - falta pulir).
3. Recordarle: cerrar/reiniciar Chrome para ver los cambios (cache).

## Workflow de deploy

1. Editar archivos en `C:\Users\vikia\OneDrive\Documentos\raiz Laura\WEB\`.
2. `Copy-Item -Recurse -Force WEB\*` al repo temporal.
3. `git add -A; git commit; git push origin main`.
4. Abrir en Chrome: https://saalaura-bit.github.io/ls/
