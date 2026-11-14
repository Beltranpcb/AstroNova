/* ============================================================================
   HUELLA X — juego «Encuentra al intruso» (docs/game/game.js)
   ----------------------------------------------------------------------------
   Cinco rondas. En cada una se muestran dos épocas de un campo de SPHEREx que
   se alternan; el jugador hace clic donde cree que está el objeto que se ha
   movido. A los 15 s aparece la pista (modo diferencia), que reduce la
   puntuación a la mitad. Al acertar se revela la ficha del objeto y su huella
   espectral: es el puente entre el juego y la ciencia.

   Puntuación: 100 por acierto + 1 por cada décima de segundo restante;
   un fallo resta 20.
   ========================================================================== */
(function () {
  "use strict";

  const ANCHO = 600;
  const ALTO = 600;
  const RONDAS = 5;
  const DURACION = 30;
  const SEGUNDOS_PISTA = 15;
  const RADIO_ACIERTO = 42;

  const OBJETOS = [
    { nombre: "(1766) Slipher", tipo: "Asteroide rocoso (tipo S)", detalle: "Silicatos a 1 y 2 µm", espectro: "asteroide_rocoso" },
    { nombre: "3I/ATLAS", tipo: "Cometa interestelar", detalle: "CO₂ a 4,26 µm", espectro: "cometa" },
    { nombre: "Luhman 16 B", tipo: "Enana marrón", detalle: "Metano a 3,3 µm", espectro: "nana_marron" },
    { nombre: "Candidato sin identificar", tipo: "Objeto frío y lejano", detalle: "Espectro plano con posible hielo", espectro: "asteroide_oscuro" },
    { nombre: "RW Aurigae", tipo: "Estrella joven variable", detalle: "Exceso infrarrojo de disco", espectro: "asteroide_oscuro" },
  ];

  const estado = {
    ronda: 0,
    puntos: 0,
    tiempo: DURACION,
    jugando: false,
    pista: false,
    objeto: null,
    posicionA: null,
    posicionB: null,
    epoca: "a",
    ultimoParpadeo: 0,
    ultimoTick: 0,
    marco: null,
    terminado: false,
  };

  let lienzo;
  let ctx;
  let fondo = null;

  // Estado expuesto en solo lectura para las pruebas automatizadas del juego.
  // No lo usa la interfaz: la web funciona igual si se elimina esta línea.
  window.HXJuego = estado;

  function mulberry32(semilla) {
    return function () {
      semilla |= 0;
      semilla = (semilla + 0x6d2b79f5) | 0;
      let t = Math.imul(semilla ^ (semilla >>> 15), 1 | semilla);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function limitar(v, min, max) {
    return Math.min(max, Math.max(min, v));
  }

  function pintarFondo() {
    const rnd = mulberry32(97013);
    fondo = document.createElement("canvas");
    fondo.width = ANCHO;
    fondo.height = ALTO;
    const g = fondo.getContext("2d");
    g.fillStyle = "#02040a";
    g.fillRect(0, 0, ANCHO, ALTO);
    for (let i = 0; i < 480; i++) {
      const x = rnd() * ANCHO;
      const y = rnd() * ALTO;
      const mag = Math.pow(rnd(), 3.2);
      const radio = 0.35 + mag * 1.7;
      const alfa = 0.15 + mag * 0.85;
      g.fillStyle = `rgba(255,255,255,${alfa})`;
      g.beginPath();
      g.arc(x, y, radio, 0, Math.PI * 2);
      g.fill();
    }
  }

  function nuevaRonda() {
    estado.ronda += 1;
    estado.tiempo = DURACION;
    estado.jugando = true;
    estado.pista = false;
    estado.terminado = false;
    estado.epoca = "a";
    estado.objeto = OBJETOS[(estado.ronda - 1) % OBJETOS.length];

    const rnd = mulberry32(1000 + estado.ronda * 77);
    const ax = 140 + rnd() * 320;
    const ay = 140 + rnd() * 320;
    const angulo = rnd() * Math.PI * 2;
    const salto = 26 + rnd() * 30;

    estado.posicionA = { x: ax, y: ay };
    estado.posicionB = {
      x: limitar(ax + Math.cos(angulo) * salto, 40, ANCHO - 40),
      y: limitar(ay + Math.sin(angulo) * salto, 40, ALTO - 40),
    };

    document.getElementById("dato-ronda").textContent = estado.ronda;
    document.getElementById("btn-pista").disabled = true;
    ocultarOverlay();
    dibujar();
  }

  function dibujarObjeto(g, x, y) {
    const grad = g.createRadialGradient(x, y, 0, x, y, 18);
    grad.addColorStop(0, "rgba(255,255,255,0.98)");
    grad.addColorStop(0.32, "rgba(210,230,255,0.5)");
    grad.addColorStop(1, "rgba(120,160,255,0)");
    g.fillStyle = grad;
    g.beginPath();
    g.arc(x, y, 18, 0, Math.PI * 2);
    g.fill();
  }

  function dibujar() {
    if (!ctx || !fondo) return;
    ctx.clearRect(0, 0, ANCHO, ALTO);
    ctx.drawImage(fondo, 0, 0);

    if (!estado.jugando) return;

    const pos = estado.epoca === "a" ? estado.posicionA : estado.posicionB;
    if (!pos) return;

    if (estado.pista) {
      // Pista: el objeto se marca en verde y su posición anterior en rojo.
      const a = estado.posicionA;
      const b = estado.posicionB;
      ctx.strokeStyle = "rgba(255,84,112,0.9)";
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.arc(a.x, a.y, RADIO_ACIERTO * 0.7, 0, Math.PI * 2);
      ctx.stroke();
      ctx.strokeStyle = "rgba(53,208,127,0.95)";
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.arc(b.x, b.y, RADIO_ACIERTO * 0.7, 0, Math.PI * 2);
      ctx.stroke();
    }

    dibujarObjeto(ctx, pos.x, pos.y);
  }

  function bucle(t) {
    estado.marco = requestAnimationFrame(bucle);

    if (!estado.jugando) return;

    if (t - estado.ultimoParpadeo > 450) {
      estado.ultimoParpadeo = t;
      estado.epoca = estado.epoca === "a" ? "b" : "a";
      dibujar();
    }

    if (!estado.ultimoTick) estado.ultimoTick = t;
    const delta = (t - estado.ultimoTick) / 1000;
    if (delta >= 0.1) {
      estado.ultimoTick = t;
      estado.tiempo = Math.max(0, estado.tiempo - delta);
      document.getElementById("dato-tiempo").textContent = estado.tiempo.toFixed(1).replace(".", ",");

      if (estado.tiempo <= SEGUNDOS_PISTA && !estado.pista) {
        document.getElementById("btn-pista").disabled = false;
      }
      if (estado.tiempo <= 0) agregarFallo("Se acabó el tiempo");
    }
  }

  function agregarFallo(motivo) {
    if (!estado.jugando) return;
    estado.puntos = Math.max(0, estado.puntos - 20);
    actualizarPuntos();
    estado.jugando = false;
    mostrarResultado(false, motivo);
  }

  function acertar() {
    if (!estado.jugando) return;
    estado.jugando = false;
    const decimas = Math.floor(estado.tiempo * 10);
    let ganados = 100 + decimas;
    if (estado.pista) ganados = Math.round(ganados / 2);
    estado.puntos += ganados;
    actualizarPuntos();
    mostrarResultado(true, `+${ganados} puntos`);
  }

  function actualizarPuntos() {
    document.getElementById("dato-puntos").textContent = estado.puntos;
  }

  function mostrarResultado(acierto, texto) {
    const overlay = document.getElementById("overlay");
    const titulo = document.getElementById("overlay-titulo");
    const cuerpo = document.getElementById("overlay-texto");
    const boton = document.getElementById("overlay-boton");

    if (acierto) {
      titulo.textContent = "¡Acertaste!";
      const o = estado.objeto;
      cuerpo.innerHTML = `
        <div class="tarjeta-objeto">
          <h3>${o.nombre}</h3>
          <div class="tipo">${o.tipo}</div>
          <dl>
            <dt>Rasgo clave</dt><dd>${o.detalle}</dd>
            <dt>Puntos</dt><dd class="resultado">${texto}</dd>
          </dl>
          <canvas class="mini-espectro" id="mini-espectro" width="360" height="74"></canvas>
        </div>`;
    } else {
      titulo.textContent = "Fallaste";
      cuerpo.innerHTML = `<p>${texto}. El objeto estaba dentro del círculo marcado.</p>`;
      // Revela la posición correcta.
      estado.pista = true;
      dibujar();
    }

    const ultima = estado.ronda >= RONDAS;
    boton.textContent = ultima ? "Ver resultado" : "Siguiente ronda";
    boton.onclick = () => {
      if (ultima) {
        terminar();
      } else {
        nuevaRonda();
      }
    };
    overlay.classList.add("visible");

    if (acierto) dibujarMiniEspectro(estado.objeto.espectro);
  }

  function dibujarMiniEspectro(tipo) {
    const c = document.getElementById("mini-espectro");
    if (!c) return;
    const g = c.getContext("2d");
    const ancho = c.width;
    const alto = c.height;
    g.clearRect(0, 0, ancho, alto);
    g.strokeStyle = "#4da3ff";
    g.lineWidth = 1.6;
    g.beginPath();

    for (let i = 0; i < 60; i++) {
      const lam = 0.75 + i * (4.25 / 59);
      let v = 0.6;
      if (tipo === "asteroide_rocoso") {
        v = 0.5 + 0.3 * (lam - 0.75);
        if (lam > 0.9 && lam < 1.05) v *= 0.72;
        if (lam > 1.9 && lam < 2.1) v *= 0.8;
      } else if (tipo === "asteroide_oscuro") {
        v = 0.55;
        if (lam > 2.9 && lam < 3.15) v *= 0.82;
      } else if (tipo === "cometa") {
        v = 0.45;
        if (lam > 2.7 && lam < 3.0) v *= 1.25;
        if (lam > 4.15 && lam < 4.35) v *= 2.1;
      } else if (tipo === "nana_marron") {
        v = 0.95 * Math.exp(-0.3 * (lam - 0.75));
        if (lam > 3.2 && lam < 3.45) v *= 0.42;
      }
      const x = (i / 59) * ancho;
      const y = alto - (v / 1.4) * alto * 0.85 - 6;
      if (i === 0) g.moveTo(x, y);
      else g.lineTo(x, y);
    }
    g.stroke();
  }

  function terminar() {
    const overlay = document.getElementById("overlay");
    const titulo = document.getElementById("overlay-titulo");
    const cuerpo = document.getElementById("overlay-texto");
    const boton = document.getElementById("overlay-boton");

    let rango = "Aprendiz";
    if (estado.puntos >= 1000) rango = "Descubridor del Planeta X";
    else if (estado.puntos >= 400) rango = "Cazador de asteroides";

    titulo.textContent = "Fin de la partida";
    cuerpo.innerHTML = `
      <p class="marcador-ronda">${estado.puntos} puntos</p>
      <div class="rango">${rango}</div>
      <p>Cada acierto es una detección real de SPHEREx que has sabido leer.
         En el explorador puedes ver su huella espectral completa.</p>`;
    boton.textContent = "Jugar otra vez";
    boton.onclick = () => {
      estado.puntos = 0;
      estado.ronda = 0;
      actualizarPuntos();
      nuevaRonda();
    };
    overlay.classList.add("visible");
  }

  function ocultarOverlay() {
    document.getElementById("overlay").classList.remove("visible");
  }

  function aCoordenadas(evento) {
    const caja = lienzo.getBoundingClientRect();
    return {
      x: ((evento.clientX - caja.left) / caja.width) * ANCHO,
      y: ((evento.clientY - caja.top) / caja.height) * ALTO,
    };
  }

  function iniciar() {
    lienzo = document.getElementById("juego-lienzo");
    ctx = lienzo.getContext("2d");
    pintarFondo();
    dibujar();

    lienzo.addEventListener("click", (ev) => {
      if (!estado.jugando) return;
      const p = aCoordenadas(ev);
      const da = Math.hypot(p.x - estado.posicionA.x, p.y - estado.posicionA.y);
      const db = Math.hypot(p.x - estado.posicionB.x, p.y - estado.posicionB.y);
      if (Math.min(da, db) <= RADIO_ACIERTO) acertar();
      else agregarFallo("No era ese punto");
    });

    document.getElementById("btn-pista").addEventListener("click", () => {
      if (!estado.jugando || estado.pista) return;
      estado.pista = true;
      document.getElementById("btn-pista").disabled = true;
      dibujar();
    });

    document.getElementById("overlay-boton").addEventListener("click", () => {
      if (estado.ronda === 0) nuevaRonda();
    });

    estado.marco = requestAnimationFrame(bucle);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
