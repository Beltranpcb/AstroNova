/* ============================================================================
   ARCHIVO: modulos/m8_calculadora/pruebas/prueba_calculadora.js
   MODULO: m8_calculadora (Lote C)
   ROL: Comprueba las fórmulas con el ejemplo numérico de la propuesta.
   LEE: Los valores 25 000 km, 0,4, 500 UA escritos en la propia prueba; sensibilidad_spherex.json.
   PRODUCE: El veredicto de node --test.
   FUNCIONAMIENTO PREVISTO:
     Recibe de prueba: 25 000 km, albedo 0,4, 500 UA.
     1. Ejecutar fisica_planeta.js, veredicto.js  ->  magnitud, temperatura, máximo, veredicto
     2. Comparar con 21,6, con 12,4 K, con 233 micras  ->  veredicto de la prueba
     Entrega a node --test: veredicto de la prueba.
   VERIFICACION: Es el propio verificador: pasa cuando se cumplen los criterios de aceptación del módulo.
   USO: node --test modulos/m8_calculadora/pruebas/prueba_calculadora.js
   ============================================================================ */
"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");

const { calcular } = require("../fisica_planeta.js");
const { evaluar } = require("../veredicto.js");
const { detectores } = require("../sensibilidad_spherex.json");

const EJEMPLO = calcular(500, 25000, 0.4);

test("con 25 000 km, albedo 0,4 y 500 UA la magnitud aparente vale 21,6 ± 0,1", () => {
  assert.ok(
    Math.abs(EJEMPLO.magnitud_aparente - 21.6) <= 0.1,
    `magnitud aparente ${EJEMPLO.magnitud_aparente}`
  );
});

test("con esos datos la temperatura de equilibrio vale 12,4 K ± 0,1", () => {
  assert.ok(
    Math.abs(EJEMPLO.temperatura_k - 12.4) <= 0.1,
    `temperatura ${EJEMPLO.temperatura_k}`
  );
});

test("con esos datos el máximo de emisión cae en 233 micras ± 5", () => {
  assert.ok(
    Math.abs(EJEMPLO.pico_wien_micras - 233) <= 5,
    `máximo ${EJEMPLO.pico_wien_micras}`
  );
});

test("con esos datos el veredicto es no detectable", () => {
  const veredicto = evaluar(EJEMPLO, detectores);
  assert.equal(veredicto.detectable, false);
  assert.equal(veredicto.etiqueta, "No detectable");
  assert.deepEqual(veredicto.detectores, []);
});

test("un planeta grande y cercano sí resulta detectable", () => {
  const cerca = calcular(1, 25000, 0.4);
  assert.ok(cerca.magnitud_aparente < 0);
  assert.equal(evaluar(cerca, detectores).detectable, true);
});

test("los seis detectores traen límite y cubren de 0,75 a 5,0 micras", () => {
  assert.equal(detectores.length, 6);
  detectores.forEach((detector, indice) => {
    assert.equal(detector.detector, indice + 1);
    assert.equal(typeof detector.limite_magnitud_ab, "number");
    assert.ok(detector.limite_magnitud_ab > 0);
    assert.ok(detector.longitud_onda_min_micras < detector.longitud_onda_max_micras);
    if (indice > 0) {
      const separacion = detector.longitud_onda_min_micras - detectores[indice - 1].longitud_onda_max_micras;
      assert.ok(separacion >= 0 && separacion <= 0.02, `hueco de ${separacion} micras entre detectores`);
    }
  });
  assert.equal(detectores[0].longitud_onda_min_micras, 0.75);
  assert.equal(detectores[detectores.length - 1].longitud_onda_max_micras, 5.0);
});

test("un diámetro o un albedo no positivos se rechazan", () => {
  assert.throws(() => calcular(500, 0, 0.4), RangeError);
  assert.throws(() => calcular(500, 25000, 0), RangeError);
});
