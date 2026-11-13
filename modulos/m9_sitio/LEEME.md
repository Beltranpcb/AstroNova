<!--
  ARCHIVO: modulos/m9_sitio/LEEME.md
  ROL: Describe el módulo junto a su comando de verificación.
  LEE: Nada.
  PRODUCE: La ficha que consulta quien desarrolla o revisa el módulo.
  VERIFICACION: Cada archivo citado aquí existe en el directorio del módulo.
-->

# m9_sitio

**Lote D** · 18 horas estimadas · capa 6 del grafo

Mostrar al público qué se mueve en cada campo, con la naturaleza de cada objeto.

## Entradas

- datos/m7_publicacion/campos.json
- datos/m7_publicacion/&lt;campo&gt;/meta.json, candidatos.json, espectros.json, epoca_a.png, epoca_b.png, diferencia.png
- La URL de modulos/m8_calculadora/calculadora.html
- contratos/guia_visual.md

## Salidas

- La web pública servida desde modulos/m9_sitio/index.html

## Depende de

`m7_publicacion`, `m8_calculadora` (solo a través de sus archivos de datos).

## Archivos

| Archivo | Responsabilidad única |
|---|---|
| `LEEME.md` | Describe el módulo junto a su comando de verificación. |
| `index.html` | Define la portada con los contenedores de cada vista. |
| `estilo.css` | Aplica la guía visual con diseño adaptable a móvil. |
| `estado_seleccion.js` | Mantiene la selección actual de campo con su candidato. |
| `carga_datos.js` | Lee los archivos publicados de un campo. |
| `selector_campo.js` | Dibuja la lista de campos disponibles. |
| `visor.js` | Dibuja las dos épocas en el lienzo según el modo elegido. |
| `superposicion.js` | Dibuja sobre el visor la trayectoria de cada candidato. |
| `tabla.js` | Muestra la tabla ordenable de candidatos. |
| `ficha.js` | Muestra la ficha del candidato seleccionado. |
| `espectro.js` | Dibuja la huella espectral del candidato seleccionado. |
| `pruebas/prueba_sitio.js` | Comprueba la lectura de datos sobre los ejemplos de los contratos. |
| `pruebas/lista_visual.md` | Enumera las comprobaciones manuales de la web en navegador. |

## Verificación en aislamiento

```bash
node --test modulos/m9_sitio/pruebas/prueba_sitio.js
```

Criterio de aceptación: el comando termina con código 0 solo si se cumple todo lo siguiente.

1. La lectura de contratos/ejemplos devuelve un campo con dos candidatos.
2. Un archivo con version_contrato distinta de 1 produce un error con el nombre del archivo.
3. Seleccionar un candidato avisa a todas las vistas suscritas una sola vez.
4. Las ocho comprobaciones de pruebas/lista_visual.md quedan marcadas tras revisarlas en navegador.

La verificación no ejecuta ningún otro módulo: usa datos sintéticos o los ejemplos de `contratos/ejemplos/`.

## Nota

Modo prueba: index.html?datos=ejemplos lee contratos/ejemplos/ en lugar de datos/m7_publicacion/. La web se sirve desde la raíz del repositorio para que la ruta ../../datos/ exista.

## Estado

Esqueleto sin código: el comando de verificación falla hasta que el lote implemente el módulo.
