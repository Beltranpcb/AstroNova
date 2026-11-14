<!--
  ARCHIVO: modulos/m6_huella_espectral/LEEME.md
  ROL: Describe el módulo junto a su comando de verificación.
  LEE: Nada.
  PRODUCE: La ficha que consulta quien desarrolla o revisa el módulo.
  VERIFICACION: Cada archivo citado aquí existe en el directorio del módulo.
-->

# m6_huella_espectral

**Lote C** · 10 horas estimadas · capa 4 del grafo

Construir el espectro infrarrojo de cada objeto en movimiento para estimar su naturaleza.

## Entradas

- datos/m1_adquisicion/&lt;campo&gt;/seleccion.json
- datos/m1_adquisicion/&lt;campo&gt;/recortes/*.fits
- datos/m3_deteccion/&lt;campo&gt;/fuentes.json
- datos/m4_movimiento/&lt;campo&gt;/movimiento.json

## Salidas

- datos/m6_huella_espectral/&lt;campo&gt;/espectros.json (contrato espectros)

## Depende de

`m1_adquisicion`, `m3_deteccion`, `m4_movimiento` (solo a través de sus archivos de datos).

## Archivos

| Archivo | Responsabilidad única |
|---|---|
| `LEEME.md` | Describe el módulo junto a su comando de verificación. |
| `trayectoria.py` | Predice dónde está el objeto en el instante de cada exposición. |
| `fotometria.py` | Mide el flujo del objeto en cada exposición de la serie espectral. |
| `plantillas.json` | Contiene los espectros de referencia de los cuatro tipos de objeto. |
| `comparacion_plantillas.py` | Asigna al espectro medido el tipo de la plantilla más parecida. |
| `ajuste_planck.py` | Estima la temperatura del objeto ajustando la ley de Planck. |
| `escritura_espectros.py` | Reúne medida, tipo, temperatura en el archivo del contrato. |
| `pruebas/prueba_huella_espectral.py` | Comprueba el ajuste espectral sobre espectros sintéticos. |
| `esquemas/espectros.schema.json` | Copia del contrato `contratos/espectros.schema.json` para verificar el módulo suelto. |
| `ejemplos/campo_ejemplo/seleccion.json`, `fuentes.json`, `movimiento.json`, `espectros.json` | Copias de `contratos/ejemplos/campo_ejemplo/` para verificar el módulo suelto. |
| `pytest.ini` | Declara el nombrado en español de las pruebas cuando el módulo se ejecuta suelto. |

## Orden de ejecución

```bash
python -m modulos.m6_huella_espectral.trayectoria <campo>
python -m modulos.m6_huella_espectral.fotometria <campo>
python -m modulos.m6_huella_espectral.comparacion_plantillas <campo>
python -m modulos.m6_huella_espectral.ajuste_planck <campo>
python -m modulos.m6_huella_espectral.escritura_espectros <campo>
```

## Verificación en aislamiento

```bash
python -m pytest modulos/m6_huella_espectral/pruebas -q
```

Criterio de aceptación: el comando termina con código 0 solo si se cumple todo lo siguiente.

1. Un cuerpo negro sintético de 300 K se recupera con una temperatura entre 270 y 330 K.
2. Un espectro sintético con un pico de emisión en 4,26 micras recibe el tipo cometa.
3. Un espectro de ruido puro recibe el tipo indeterminado.
4. El espectros.json generado valida contra contratos/espectros.schema.json.

La verificación no ejecuta ningún otro módulo: usa datos sintéticos o los ejemplos de `contratos/ejemplos/`.

## Nota

Si el espectro de un objeto móvil sale ruidoso se publica con agrupacion igual a detector (6 puntos), dicho con transparencia en la web.

## Estado

Implementado. Los cinco comandos de arriba se ejecutan en orden y la verificación
pasa con `python -m pytest modulos/m6_huella_espectral/pruebas -q`.

Las curvas de `plantillas.json` son sintéticas: reproducen los rasgos de la
especificación (silicatos, hidratación, hielo de agua, CO₂, CO, metano), no son
espectros de referencia medidos. Sirven para comparar formas y deben sustituirse
por curvas de bibliografía antes de publicar.
