<!--
  ARCHIVO: contratos/recortes_fits.md
  ROL: Fija las extensiones que debe traer cada recorte crudo.
  LEE: Nada.
  PRODUCE: La regla que cumplen productor con consumidores.
  VERIFICACION: Descrita en el último apartado de este archivo.
-->
# Contrato: recortes FITS crudos

| Dato | Valor |
|---|---|
| Productor | `m1_adquisicion/descarga_recortes.py` |
| Consumidores | `m2_alineacion`, `m6_huella_espectral` |
| Ruta | `datos/m1_adquisicion/<campo>/recortes/<id_exposicion>.fits` |
| En git | No. `.gitignore` excluye todo `*.fits`. |

## Forma obligatoria

- Un archivo por cada exposición de `seleccion.json`, con el nombre de su `archivo_recorte`.
- Recorte de imagen espectral de nivel 2 de SPHEREx, pedido con `center` y `size` al servicio de recortes de IRSA.
- Escala nativa de 6,15 segundos de arco por píxel.
- Extensiones presentes, con estos nombres:

| Extensión | Contenido | Unidad |
|---|---|---|
| `IMAGE` | Brillo superficial | MJy/sr |
| `FLAGS` | Máscara de píxeles, valores enteros | sin unidad |
| `VARIANCE` | Varianza de `IMAGE` | (MJy/sr)² |
| `ZODI` | Modelo de luz zodiacal | MJy/sr |
| `PSF` | Función de dispersión de punto | sin unidad |
| `WCS-WAVE` | Longitud de onda de cada píxel | micras |

Los nombres exactos de las extensiones `PSF` y `WCS-WAVE` se confirman contra la cabecera del primer recorte real en la hora 0. Si difieren, se corrige este contrato en un PR propio.

## Verificación

Abrir cada archivo con `astropy.io.fits` y comprobar que la lista de extensiones contiene las seis de la tabla.
