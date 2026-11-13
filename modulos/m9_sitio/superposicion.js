/* ============================================================================
   ARCHIVO: modulos/m9_sitio/superposicion.js
   MODULO: m9_sitio (Lote D)
   ROL: Dibuja sobre el visor la trayectoria de cada candidato.
   LEE: candidatos de carga_datos.js; la transformación de vista de visor.js; la selección actual.
   PRODUCE: Un círculo en cada posición con una flecha de A a B; el candidato seleccionado resaltado.
   FUNCIONAMIENTO PREVISTO:
     Recibe de carga_datos.js: posiciones A, B de cada candidato.
     1. Convertir coordenadas de rejilla a coordenadas de lienzo  ->  puntos en pantalla
     2. Trazar círculo con flecha de A a B  ->  marcas
     3. Resaltar el candidato seleccionado  ->  marcas sobre el lienzo
     Entrega a visitante: marcas sobre el lienzo.
   VERIFICACION: Con los ejemplos aparecen dos flechas; cada una empieza en posicion_a.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
