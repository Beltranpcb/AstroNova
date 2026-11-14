/* ============================================================================
   ARCHIVO: modulos/m8_calculadora/interfaz.js
   MODULO: m8_calculadora (Lote C)
   ROL: Refleja en pantalla el resultado de cada movimiento de deslizador.
   LEE: Los tres deslizadores de calculadora.html; fisica_planeta.js; veredicto.js; sensibilidad_spherex.json.
   PRODUCE: Las cifras con el mensaje actualizados en la página.
   FUNCIONAMIENTO PREVISTO:
     Recibe de calculadora.html: valores de los tres deslizadores.
     1. Pedir el cálculo a fisica_planeta.js  ->  magnitud, temperatura, máximo
     2. Pedir el veredicto a veredicto.js  ->  veredicto con motivo
     3. Escribir cifras con mensaje  ->  pantalla actualizada
     Entrega a visitante: pantalla actualizada.
   VERIFICACION: Al mover un deslizador cambian las tres cifras sin recargar la página.
   USO: se carga con <script> al final de calculadora.html.
   ============================================================================ */
(function () {
  "use strict";

  var DESLIZADORES = [
    { id: "distancia", salida: "valor_distancia", formato: function (valor) { return valor + " UA"; } },
    { id: "diametro", salida: "valor_diametro", formato: function (valor) { return valor + " km"; } },
    { id: "albedo", salida: "valor_albedo", formato: function (valor) { return valor.toFixed(2); } },
  ];

  function numero(id) {
    return Number(document.getElementById(id).value);
  }

  function escribir(id, texto) {
    var elemento = document.getElementById(id);
    if (elemento) {
      elemento.textContent = texto;
    }
  }

  function actualizar(detectores) {
    var valores = {};
    DESLIZADORES.forEach(function (deslizador) {
      valores[deslizador.id] = numero(deslizador.id);
      escribir(deslizador.salida, deslizador.formato(valores[deslizador.id]));
    });

    var medida = FisicaPlaneta.calcular(valores.distancia, valores.diametro, valores.albedo);
    var veredicto = Veredicto.evaluar(medida, detectores);

    escribir("magnitud", medida.magnitud_aparente.toFixed(1));
    escribir("temperatura", medida.temperatura_k.toFixed(1));
    escribir("pico", medida.pico_wien_micras.toFixed(0));

    var caja = document.getElementById("veredicto");
    if (caja) {
      caja.textContent = veredicto.etiqueta;
      caja.dataset.detectable = String(veredicto.detectable);
    }
    escribir("motivo", veredicto.motivo);
  }

  function conectar(detectores) {
    DESLIZADORES.forEach(function (deslizador) {
      document.getElementById(deslizador.id).addEventListener("input", function () {
        actualizar(detectores);
      });
    });
    actualizar(detectores);
  }

  function iniciar() {
    fetch("sensibilidad_spherex.json")
      .then(function (respuesta) {
        if (!respuesta.ok) {
          throw new Error("HTTP " + respuesta.status);
        }
        return respuesta.json();
      })
      .then(function (datos) {
        conectar(datos.detectores);
      })
      .catch(function (error) {
        escribir(
          "motivo",
          "No se pudo leer sensibilidad_spherex.json (" +
            error.message +
            "). Sirve la carpeta por HTTP: python -m http.server desde la raíz del repositorio."
        );
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
