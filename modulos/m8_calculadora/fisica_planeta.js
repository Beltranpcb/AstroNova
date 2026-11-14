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
   USO: se carga con <script> en calculadora.html o con require() en las pruebas.
   ============================================================================ */
(function (raiz, fabrica) {
  "use strict";
  if (typeof module === "object" && module.exports) {
    module.exports = fabrica();
  } else {
    raiz.FisicaPlaneta = fabrica();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var CONSTANTE_H_KM = 1329;              // km, constante de la magnitud absoluta
  var TEMPERATURA_A_UNA_UA_K = 278;       // K, temperatura de equilibrio a 1 UA
  var CONSTANTE_WIEN_MICRAS_KELVIN = 2898; // micras kelvin

  function exigirPositivo(nombre, valor) {
    if (typeof valor !== "number" || !Number.isFinite(valor) || valor <= 0) {
      throw new RangeError(nombre + " debe ser un número positivo; recibido: " + valor);
    }
  }

  function magnitud_absoluta(diametro_km, albedo) {
    exigirPositivo("el diámetro", diametro_km);
    exigirPositivo("el albedo", albedo);
    return 5 * Math.log10(CONSTANTE_H_KM / (diametro_km * Math.sqrt(albedo)));
  }

  function magnitud_aparente(magnitud_abs, distancia_au) {
    if (typeof magnitud_abs !== "number" || !Number.isFinite(magnitud_abs)) {
      throw new TypeError("la magnitud absoluta debe ser un número finito");
    }
    exigirPositivo("la distancia", distancia_au);
    return magnitud_abs + 5 * Math.log10(distancia_au * distancia_au);
  }

  function temperatura_equilibrio(distancia_au) {
    exigirPositivo("la distancia", distancia_au);
    return TEMPERATURA_A_UNA_UA_K / Math.sqrt(distancia_au);
  }

  function pico_wien_micras(temperatura_k) {
    exigirPositivo("la temperatura", temperatura_k);
    return CONSTANTE_WIEN_MICRAS_KELVIN / temperatura_k;
  }

  function calcular(distancia_au, diametro_km, albedo) {
    var absoluta = magnitud_absoluta(diametro_km, albedo);
    var temperatura = temperatura_equilibrio(distancia_au);
    return {
      distancia_au: distancia_au,
      diametro_km: diametro_km,
      albedo: albedo,
      magnitud_absoluta: absoluta,
      magnitud_aparente: magnitud_aparente(absoluta, distancia_au),
      temperatura_k: temperatura,
      pico_wien_micras: pico_wien_micras(temperatura),
    };
  }

  return {
    CONSTANTE_H_KM: CONSTANTE_H_KM,
    TEMPERATURA_A_UNA_UA_K: TEMPERATURA_A_UNA_UA_K,
    CONSTANTE_WIEN_MICRAS_KELVIN: CONSTANTE_WIEN_MICRAS_KELVIN,
    magnitud_absoluta: magnitud_absoluta,
    magnitud_aparente: magnitud_aparente,
    temperatura_equilibrio: temperatura_equilibrio,
    pico_wien_micras: pico_wien_micras,
    calcular: calcular,
  };
});
