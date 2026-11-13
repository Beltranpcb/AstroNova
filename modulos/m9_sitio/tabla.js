/* ============================================================================
   ARCHIVO: modulos/m9_sitio/tabla.js
   MODULO: m9_sitio (Lote D)
   ROL: Muestra la tabla ordenable de candidatos.
   LEE: candidatos de carga_datos.js; la selección actual.
   PRODUCE: Las filas visibles; el id de la fila pulsada pasa a estado_seleccion.js.
   FUNCIONAMIENTO PREVISTO:
     Recibe de carga_datos.js: candidatos.
     1. Ordenar por la columna elegida  ->  filas ordenadas
     2. Filtrar por clase de movimiento  ->  filas visibles
     3. Comunicar el clic de fila  ->  id de candidato
     Entrega a estado_seleccion.js: id de candidato.
   VERIFICACION: Pulsar una cabecera reordena las filas; el filtro por clase oculta las demás.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
