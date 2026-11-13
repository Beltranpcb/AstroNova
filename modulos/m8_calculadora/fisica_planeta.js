/* ============================================================================
   ARCHIVO: modulos/m8_calculadora/fisica_planeta.js
   MODULO: m8_calculadora (Lote C)
   ROL: Evalúa las fórmulas de brillo del planeta hipotético.
   LEE: Distancia en UA, diámetro en km, albedo, entregados por interfaz.js.
   PRODUCE: Magnitud aparente, temperatura de equilibrio, longitud de onda del máximo.
   FUNCIONAMIENTO PREVISTO:
     Recibe de interfaz.js: distancia, diámetro, albedo.
     1. Calcular la magnitud absoluta H = 5 log10(1329 / (D raíz de p))  ->  H
     2. Calcular la magnitud aparente m = H + 5 log10(r delta)  ->  m
     3. Calcular T = 278 / raíz de r, con el pico de Wien 2898 / T  ->  magnitud, temperatura, máximo de emisión
     Entrega a veredicto.js, interfaz.js: magnitud, temperatura, máximo de emisión.
   VERIFICACION: Reproduce el ejemplo numérico de la propuesta dentro de los márgenes del criterio de aceptación.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
