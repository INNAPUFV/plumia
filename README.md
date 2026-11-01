# PlumIA · versión web (v2.0 · L)

Editor de noticias potenciado con IA para la práctica de redacción periodística.

- `plumia.html`: la aplicación (comprimida) que carga el lanzador del Canvas de Gemini.
- `plumia.js`: la misma app empaquetada como script, para cargarla desde el CDN jsDelivr (`cdn.jsdelivr.net/gh/INNAPUFV/plumia@main/plumia.js`).
- `src/plumia-v2.0-L.html`: código fuente legible de la misma versión.
- El lanzador que se pega en el Canvas de Gemini descarga `https://innapufv.github.io/plumia/plumia.html`.

Para publicar una versión nueva: sustituir `src/…`, `plumia.html` y `plumia.js` y subir los cambios. Todos los alumnos reciben la nueva versión con el mismo enlace de Gemini (GitHub Pages tarda unos minutos en actualizarse).

El CDN jsDelivr puede tardar hasta 12 horas en servir la versión nueva; para forzarlo, abrir https://purge.jsdelivr.net/gh/INNAPUFV/plumia@main/plumia.js
