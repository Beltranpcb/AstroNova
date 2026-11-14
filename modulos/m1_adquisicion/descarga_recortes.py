# ============================================================================
# ARCHIVO: modulos/m1_adquisicion/descarga_recortes.py
# MODULO: m1_adquisicion (Lote A)
# ROL: Descarga el recorte FITS de cada exposición seleccionada.
# LEE: seleccion.json; servicio de recortes de IRSA.
# PRODUCE: datos/m1_adquisicion/<campo>/recortes/<id_exposicion>.fits.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de seleccion_epocas.py: seleccion.json.
#   1. Añadir center, size a cada url_acceso  ->  URL de recorte
#   2. Pedir el recorte a IRSA  ->  bytes FITS
#   3. Guardar con el nombre archivo_recorte  ->  recortes FITS crudos
#   Entrega a m2, m6: recortes FITS crudos.
# VERIFICACION: Existe un FITS por exposición de seleccion.json; cada uno cumple contratos/recortes_fits.md.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from modulos.m1_adquisicion.consulta_sia import DIR_DATOS

# Extensiones que exige contratos/recortes_fits.md
EXTENSIONES_OBLIGATORIAS = ("IMAGE", "FLAGS", "VARIANCE", "ZODI", "PSF", "WCS-WAVE")


class RecorteInvalido(ValueError):
    """El archivo descargado no es un FITS o le faltan extensiones del contrato."""


def url_recorte(url_acceso: str, ra_grados: float, dec_grados: float, radio_grados: float) -> str:
    """Añade center y size a la URL. `radio_grados` es el semilado, así que size (lado completo) es el doble."""
    base = url_acceso.split("?")[0]
    return f"{base}?center={ra_grados:.8f},{dec_grados:.8f}&size={2 * radio_grados:.6g}"


def obtener_bytes(url: str, reintentos: int = 3, espera_s: float = 2.0, timeout_s: float = 300.0) -> bytes:
    """Descarga una URL con reintentos. Se puede sustituir en pruebas."""
    import requests

    ultimo_error: Exception | None = None
    for intento in range(1, reintentos + 1):
        try:
            respuesta = requests.get(url, timeout=timeout_s)
            respuesta.raise_for_status()
            return respuesta.content
        except requests.RequestException as error:
            ultimo_error = error
            if intento < reintentos:
                time.sleep(espera_s * intento)
    raise RuntimeError(f"No se pudo descargar {url} tras {reintentos} intentos: {ultimo_error}")


def extensiones_que_faltan(ruta: Path) -> list[str]:
    """Extensiones del contrato ausentes en el FITS. Lanza RecorteInvalido si no se puede abrir como FITS."""
    from astropy.io import fits

    try:
        with fits.open(ruta, memmap=False) as hdus:
            presentes = {h.name.upper() for h in hdus}
    except (OSError, ValueError) as error:
        raise RecorteInvalido(f"{ruta.name} no es un FITS legible: {error}") from error
    return [e for e in EXTENSIONES_OBLIGATORIAS if e not in presentes]


def _nombre_seguro(nombre: str) -> str:
    if Path(nombre).name != nombre or not nombre.endswith(".fits"):
        raise ValueError(f"archivo_recorte no válido: {nombre!r}")
    return nombre


def descargar_campo(campo: str, dir_datos: Path = DIR_DATOS, obtener=obtener_bytes,
                    forzar: bool = False) -> list[Path]:
    """Descarga y valida un recorte por exposición de seleccion.json. Devuelve las rutas de los FITS.

    Un recorte que falla no detiene a los demás: al final se lanza un único error que los lista.
    """
    ruta_seleccion = dir_datos / campo / "seleccion.json"
    with open(ruta_seleccion, encoding="utf-8") as f:
        seleccion = json.load(f)
    ra, dec = seleccion["centro"]["ra_grados"], seleccion["centro"]["dec_grados"]
    radio = seleccion["radio_grados"]

    carpeta = dir_datos / campo / "recortes"
    carpeta.mkdir(parents=True, exist_ok=True)

    listos: list[Path] = []
    fallos: list[str] = []
    for exposicion in seleccion["exposiciones"]:
        destino = carpeta / _nombre_seguro(exposicion["archivo_recorte"])
        if destino.exists() and not forzar:
            try:
                if not extensiones_que_faltan(destino):
                    listos.append(destino)
                    continue
            except RecorteInvalido:
                pass  # archivo anterior corrupto: se vuelve a descargar
        url = url_recorte(exposicion["url_acceso"], ra, dec, radio)
        parcial = destino.with_name(destino.name + ".parte")
        try:
            parcial.write_bytes(obtener(url))
            faltan = extensiones_que_faltan(parcial)
            if faltan:
                raise RecorteInvalido(
                    f"{destino.name} no trae las extensiones {faltan}. "
                    "Si IRSA las nombra distinto, corrige contratos/recortes_fits.md en un PR propio."
                )
            os.replace(parcial, destino)  # solo un FITS completo y válido ocupa el nombre final
            listos.append(destino)
        except (RecorteInvalido, RuntimeError, OSError) as error:
            parcial.unlink(missing_ok=True)
            fallos.append(f"{exposicion['id_exposicion']}: {error}")

    if fallos:
        raise RuntimeError(f"{len(fallos)} de {len(seleccion['exposiciones'])} recortes fallaron:\n  " + "\n  ".join(fallos))
    return listos


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Descarga los recortes FITS de las exposiciones seleccionadas.")
    parser.add_argument("campo", help="identificador del campo")
    parser.add_argument("--forzar", action="store_true", help="volver a descargar aunque el recorte ya exista y sea válido")
    args = parser.parse_args(argv)
    try:
        rutas = descargar_campo(args.campo, forzar=args.forzar)
    except FileNotFoundError:
        print(f"ERROR: falta datos/m1_adquisicion/{args.campo}/seleccion.json. Ejecuta antes seleccion_epocas.", file=sys.stderr)
        return 1
    except (RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"{len(rutas)} recortes en {rutas[0].parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())