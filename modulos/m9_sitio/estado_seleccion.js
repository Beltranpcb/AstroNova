/* ============================================================================
   ARCHIVO: modulos/m9_sitio/estado_seleccion.js
   MODULO: m9_sitio (Lote D)
   ROL: Mantiene la selección actual de campo con su candidato.
   LEE: Los clics que le comunican selector_campo.js, visor.js, tabla.js.
   PRODUCE: Un aviso de cambio para cada vista suscrita.
   FUNCIONAMIENTO PREVISTO:
     Recibe de vistas: campo elegido, id de candidato.
     1. Guardar la selección  ->  selección actual
     2. Avisar a las vistas suscritas  ->  aviso de cambio
     Entrega a carga_datos.js, vistas: aviso de cambio.
   VERIFICACION: Cada cambio de selección avisa una sola vez a cada vista suscrita.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
