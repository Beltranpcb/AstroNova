/* ============================================================================
   ARCHIVO: modulos/m8_calculadora/veredicto.js
   MODULO: m8_calculadora (Lote C)
   ROL: Decide si el planeta calculado supera el límite de SPHEREx.
   LEE: El resultado de fisica_planeta.js; sensibilidad_spherex.json.
   PRODUCE: Un veredicto (detectable o no detectable) con su motivo en texto.
   FUNCIONAMIENTO PREVISTO:
     Recibe de fisica_planeta.js: magnitud, máximo de emisión.
     1. Leer sensibilidad_spherex.json  ->  límite por detector
     2. Comparar el brillo con cada límite  ->  detectores que lo verían
     3. Redactar el motivo  ->  veredicto con motivo
     Entrega a interfaz.js: veredicto con motivo.
   VERIFICACION: Un planeta más débil que el límite de todos los detectores da no detectable.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
