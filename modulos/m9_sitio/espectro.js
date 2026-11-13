/* ============================================================================
   ARCHIVO: modulos/m9_sitio/espectro.js
   MODULO: m9_sitio (Lote D)
   ROL: Dibuja la huella espectral del candidato seleccionado.
   LEE: espectros de carga_datos.js; la selección actual; Chart.js.
   PRODUCE: La gráfica de flujo frente a longitud de onda, rotulada con tipo, temperatura.
   FUNCIONAMIENTO PREVISTO:
     Recibe de estado_seleccion.js: id de candidato.
     1. Buscar los puntos del espectro  ->  longitud de onda, flujo, error, fecha
     2. Ordenar los puntos por fecha  ->  secuencia temporal
     3. Rellenar la gráfica banda a banda  ->  animación
     4. Rotular tipo con temperatura  ->  gráfica rotulada
     Entrega a visitante: gráfica rotulada.
   VERIFICACION: Los puntos aparecen en orden de fecha de observación; el eje horizontal va de 0,75 a 5,0 micras.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
