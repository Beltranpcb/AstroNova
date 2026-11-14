<!--
  ARCHIVO: modulos/m9_sitio/LEEME.md
  ROL: Describe el módulo junto a su comando de verificación.
  LEE: Nada.
  PRODUCE: La ficha que consulta quien desarrolla o revisa el módulo.
  VERIFICACION: Cada archivo citado aquí existe en el directorio del módulo.
-->

# m9_sitio

**Lote D** · 18 h estimadas · capa 6 del grafo

Mostrar al público qué se mueve en cada campo, con la naturaleza de cada objeto.

## Entradas

- `datos/m7_publicacion/campos.json`
- `datos/m7_publicacion/<campo>/{meta,candidatos,espectros}.json`
- Opcionalmente `datos/m7_publicacion/<campo>/{epoca_a,epoca_b,diferencia}.png`
- Aladin Lite y Chart.js, cargados por CDN
- `contratos/guia_visual.md` (variables de color)

## Salidas

- La web pública servida desde `modulos/m9_sitio/index.html`

## Depende de

`m7_publicacion` (solo a través de sus archivos de datos). Ningún módulo importa
el código de otro.

## Archivos

| Archivo | Responsabilidad única |
|---|---|
| `LEEME.md` | Describe el módulo junto a su comando de verificación. |
| `index.html` | Define la portada, el visor, la ficha y la tabla. |
| `estilo.css` | Aplica la guía visual con diseño adaptable a móvil. |
| `estado_seleccion.js` | Mantiene el estado compartido y avisa de la selección. |
| `carga_datos.js` | Lee los archivos publicados por m7_publicacion. |
| `selector_campo.js` | Dibuja la lista de campos disponibles. |
| `espectro3d.html` | Página aparte con las huellas espectrales del campo en 3D. |
| `espectro3d.js` | Escena WebGL (three.js): un listón por candidata, ejes y unión opcional. |
| `visor.js` | Dibuja las dos épocas en el lienzo según el modo elegido. |
| `superposicion.js` | Dibuja sobre el visor la trayectoria de cada candidato. |
| `tabla.js` | Muestra la tabla ordenable de candidatos y exporta CSV. |
| `ficha.js` | Muestra la ficha del candidato y el mapa del cielo. |
| `espectro.js` | Dibuja la huella espectral del candidato seleccionado. |
| `ejemplos/generar_datos.py` | Genera datos de demostración conformes a los contratos. |
| `pruebas/lista_visual.md` | Comprobaciones manuales de la web. |

## Cómo se ejecuta

```bash
# 1. Servir el repositorio desde la raíz (no abrir con file://)
python3 -m http.server 8765

# 2. Abrir en el navegador
#    http://127.0.0.1:8765/modulos/m9_sitio/index.html
```

La web busca los datos en `datos/m7_publicacion/` probando tres rutas relativas,
de modo que funciona tanto servida desde la raíz como desde su propio directorio.

## Datos de demostración

Mientras el pipeline no produce datos reales:

```bash
python modulos/m9_sitio/ejemplos/generar_datos.py
```

Escribe en `datos/m7_publicacion/` tres campos (`slipher`, `atlas`, `luhman`) con
la misma forma que produce `m7_publicacion`. Los valores son ilustrativos.

## Verificación

```bash
# Los datos de demostración cumplen los contratos
check-jsonschema --schemafile contratos/campos.schema.json datos/m7_publicacion/campos.json

# La web arranca sin errores de recursos
python3 -m http.server 8765 &
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8765/modulos/m9_sitio/index.html
```

Comprobaciones manuales: `pruebas/lista_visual.md`.

## Límites conocidos

- **Los PNG no existen todavía.** Si falta `epoca_a.png`, el visor sintetiza dos
  fotogramas con los candidatos para que la interfaz sea demostrable. Cuando el
  pipeline entregue los PNG, se usan automáticamente y la síntesis no se ejecuta.
- **El campo `luhman` usa valores ilustrativos.** El movimiento propio real de
  una enana marrón (2,75 ″/año) no es detectable entre dos épocas de SPHEREx:
  en 6 meses supone 1,4 ″, una quinta parte de un píxel. El campo se conserva
  para mostrar la huella espectral, no como ejemplo de detección por movimiento.
- **El mapa del cielo depende de un servicio externo.** Si el servidor HiPS no
  responde en 2,5 s, la ficha dibuja un mapa de respaldo con la rejilla y la
  posición.
