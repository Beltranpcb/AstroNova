/* ============================================================================
   ARCHIVO: modulos/m9_sitio/visor.js
   MODULO: m9_sitio (Lote D)
   ROL: Dibuja las dos épocas en el lienzo según el modo elegido.
   LEE: epoca_a.png, epoca_b.png, diferencia.png; meta.json a través de carga_datos.js.
   PRODUCE: El lienzo con la imagen, las fechas de A, B, el tiempo transcurrido.
   FUNCIONAMIENTO PREVISTO:
     Recibe de m7_publicacion: epoca_a.png, epoca_b.png, diferencia.png.
     1. Componer el fotograma del modo parpadeo, cortina o diferencia  ->  fotograma
     2. Aplicar zoom, arrastre  ->  transformación de vista
     3. Rotular fechas con tiempo transcurrido de meta.json  ->  lienzo rotulado
     Entrega a superposicion.js, visitante: lienzo rotulado.
   VERIFICACION: Los tres modos (parpadeo, cortina, diferencia) cambian la imagen; la rueda hace zoom; el arrastre desplaza.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
