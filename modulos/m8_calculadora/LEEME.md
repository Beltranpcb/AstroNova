<!--
  ARCHIVO: modulos/m8_calculadora/LEEME.md
  ROL: Describe el módulo junto a su comando de verificación.
  LEE: Nada.
  PRODUCE: La ficha que consulta quien desarrolla o revisa el módulo.
  VERIFICACION: Cada archivo citado aquí existe en el directorio del módulo.
-->

# m8_calculadora

**Lote C** · 3 horas estimadas · capa 0 del grafo

Mostrar si SPHEREx podría detectar un planeta hipotético elegido por el visitante.

## Entradas

- Ninguna de otro módulo: solo los tres deslizadores del visitante
- contratos/guia_visual.md

## Salidas

- La página modulos/m8_calculadora/calculadora.html, enlazada desde m9_sitio

## Depende de

Ningún otro módulo.

## Archivos

| Archivo | Responsabilidad única |
|---|---|
| `LEEME.md` | Describe el módulo junto a su comando de verificación. |
| `calculadora.html` | Define la página con los tres deslizadores del planeta hipotético. |
| `estilo.css` | Aplica la guía visual a la página de la calculadora. |
| `fisica_planeta.js` | Evalúa las fórmulas de brillo del planeta hipotético. |
| `sensibilidad_spherex.json` | Contiene el límite de detección de SPHEREx por detector. |
| `veredicto.js` | Decide si el planeta calculado supera el límite de SPHEREx. |
| `interfaz.js` | Refleja en pantalla el resultado de cada movimiento de deslizador. |
| `pruebas/prueba_calculadora.js` | Comprueba las fórmulas con el ejemplo numérico de la propuesta. |

## Verificación en aislamiento

```bash
node --test modulos/m8_calculadora/pruebas/prueba_calculadora.js
```

Criterio de aceptación: el comando termina con código 0 solo si se cumple todo lo siguiente.

1. Con diámetro 25 000 km, albedo 0,4, distancia 500 UA, la magnitud aparente vale 21,6 con un margen de 0,1.
2. Con esos mismos datos la temperatura vale 12,4 K con un margen de 0,1 K.
3. Con esos mismos datos el máximo de emisión cae en 233 micras con un margen de 5 micras.
4. Con esos mismos datos el veredicto es no detectable.

La verificación no ejecuta ningún otro módulo: usa datos sintéticos o los ejemplos de `contratos/ejemplos/`.

## Nota

Página autónoma: abre sin ningún dato del pipeline. Los valores de sensibilidad_spherex.json se toman de la documentación de IRSA, nunca se inventan.

## Estado

Implementado. La página funciona sola y la verificación pasa con
`node --test modulos/m8_calculadora/pruebas/prueba_calculadora.js`.

Los límites de `sensibilidad_spherex.json` son 5σ para fuente puntual del sondeo
de todo el cielo (19,5–19,9 AB entre 0,75 y 3,8 µm; 17,8–18,8 AB entre 3,8 y
5,0 µm), tomados de la bibliografía de la misión y de la documentación de IRSA.
