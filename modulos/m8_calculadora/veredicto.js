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
   USO: se carga con <script> en calculadora.html o con require() en las pruebas.
   ============================================================================ */
(function (raiz, fabrica) {
  "use strict";
  if (typeof module === "object" && module.exports) {
    module.exports = fabrica();
  } else {
    raiz.Veredicto = fabrica();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function detectores_que_lo_ven(medida, detectores) {
    return detectores
      .filter(function (detector) {
        return (
          typeof detector.limite_magnitud_ab === "number" &&
          Number.isFinite(detector.limite_magnitud_ab) &&
          medida.magnitud_aparente <= detector.limite_magnitud_ab
        );
      })
      .map(function (detector) {
        return detector.detector;
      });
  }

  function evaluar(medida, detectores) {
    if (!medida || typeof medida.magnitud_aparente !== "number" || !Number.isFinite(medida.magnitud_aparente)) {
      throw new TypeError("la medida debe traer una magnitud aparente finita");
    }
    if (!Array.isArray(detectores) || detectores.length === 0) {
      throw new TypeError("faltan los detectores de sensibilidad_spherex.json");
    }

    var visibles = detectores_que_lo_ven(medida, detectores);
    if (visibles.length > 0) {
      return {
        detectable: true,
        etiqueta: "Detectable",
        motivo:
          "Con magnitud aparente " +
          medida.magnitud_aparente.toFixed(1) +
          ", SPHEREx lo vería en el detector " +
          visibles.join(", ") +
          ".",
        detectores: visibles,
      };
    }

    var mas_sensible = detectores.reduce(function (mejor, detector) {
      return detector.limite_magnitud_ab > mejor.limite_magnitud_ab ? detector : mejor;
    });
    return {
      detectable: false,
      etiqueta: "No detectable",
      motivo:
        "Con magnitud aparente " +
        medida.magnitud_aparente.toFixed(1) +
        " no llega al límite del detector más sensible (detector " +
        mas_sensible.detector +
        ", " +
        mas_sensible.limite_magnitud_ab +
        " AB).",
      detectores: [],
    };
  }

  return {
    detectores_que_lo_ven: detectores_que_lo_ven,
    evaluar: evaluar,
  };
});
