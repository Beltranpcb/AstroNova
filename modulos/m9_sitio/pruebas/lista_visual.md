<!--
  ARCHIVO: modulos/m9_sitio/pruebas/lista_visual.md
  ROL: Lista de comprobaciones manuales de la web.
  LEE: La web servida en local.
  PRODUCE: El veredicto de quien revisa el módulo.
  VERIFICACION: Cada punto se marca tras observarlo en pantalla.
-->

# Lista visual de m9_sitio

Servir el repositorio desde la raíz y abrir
`http://127.0.0.1:8765/modulos/m9_sitio/index.html`.

## Portada

- [ ] Se lee el título **HUELLA X** con degradado.
- [ ] Hay dos botones: **Explorar** y **Jugar**.
- [ ] Aparecen tres botones de campo: Slipher, 3I/ATLAS y Luhman 16.
- [ ] Pulsar un campo abre la aplicación en ese campo.

## Visor

- [ ] El lienzo muestra el campo y las fechas de A y B debajo.
- [ ] **Parpadeo**: las dos épocas se alternan cada 450 ms.
- [ ] **Cortina**: aparece una línea vertical; arrastrar sobre el lienzo la mueve.
- [ ] **Diferencia**: lo que aparece se ve en verde y lo que desaparece en rojo.
- [ ] La rueda del ratón hace zoom y el arrastre desplaza la imagen.
- [ ] **Centrar** devuelve el zoom a 1 y la imagen al origen.
- [ ] **Pausa** detiene el parpadeo y **Reproducir** lo reanuda.
- [ ] Cada candidato tiene un círculo en A y una flecha hacia B.
- [ ] Pulsar sobre un círculo selecciona ese candidato.

## Tabla

- [ ] Hay una fila por candidato, con separación, velocidad, significancia y clase.
- [ ] Pulsar una cabecera ordena; pulsar otra vez invierte el orden.
- [ ] Los filtros dejan solo las filas del estado elegido.
- [ ] Pulsar una fila selecciona el candidato y centra el visor.
- [ ] El botón **CSV** descarga la vista actual.

## Ficha

- [ ] Muestra posición, separación, velocidad, significancia y clase.
- [ ] La nota de **candidato** está siempre visible.
- [ ] El mapa aparece centrado en la posición del candidato.
- [ ] El espectro se dibuja con los puntos de `espectros.json`.
- [ ] Cambiar de candidato actualiza el espectro.

## Móvil (ancho menor de 900 px)

- [ ] El visor queda encima y la tabla debajo.
- [ ] No hay desplazamiento horizontal de la página.
- [ ] Los botones siguen siendo pulsables.

## Juego

- [ ] El botón **Jugar** abre `juego/game.html`.
- [ ] Cada ronda dura 30 s y hay cinco rondas.
- [ ] A los 15 s se habilita **Pista** y la puntuación se reduce a la mitad.
- [ ] Acertar revela la ficha del objeto y su mini espectro.
- [ ] Fallar resta 20 puntos.
- [ ] Al terminar se muestra la puntuación y un rango.
