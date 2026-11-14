# ============================================================================
# ARCHIVO: modulos/m3_deteccion/propuesta_parejas.py
# MODULO: m3_deteccion (Lote B)
# ROL: Propone parejas A-B entre las fuentes huérfanas.
# LEE: situaciones.json; meta.json.
# PRODUCE: datos/m3_deteccion/<campo>/fuentes.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de emparejamiento.py: situaciones.json.
#   1. Leer las horas entre A, B de meta.json  ->  separación máxima admisible
#   2. Filtrar por separación, brillo parecido  ->  parejas compatibles
#   3. Escribir fuentes con parejas  ->  fuentes.json
#   Entrega a m4, m5, m6, m7: fuentes.json.
# VERIFICACION: El archivo valida contra contratos/fuentes.schema.json; toda pareja une una fuente de epoca_a con una de epoca_b.
# USO: python -m modulos.m3_deteccion.propuesta_parejas <campo>
# ============================================================================
import json
import math
import sys
from pathlib import Path

VELOCIDAD_MAXIMA_SEGARC_POR_HORA = 60.0  # el doble de un asteroide típico del cinturón principal
RAZON_MAXIMA_DE_BRILLO = 2.0  # el flujo de B entre el de A queda entre 1/2 y 2
CAMPOS_DE_FUENTE = ("id_fuente", "epoca", "ra_grados", "dec_grados", "x", "y", "flujo_mjy", "senal_ruido",
                    "incertidumbre_posicion_segarc", "situacion")


def separacion_maxima_pixeles(meta):
    """Píxeles que un objeto puede recorrer entre A y B a la velocidad máxima admisible."""
    return VELOCIDAD_MAXIMA_SEGARC_POR_HORA * meta["horas_entre_a_b"] / meta["escala_segarc_por_pixel"]


def brillo_parecido(fuente_a, fuente_b):
    fa, fb = fuente_a["flujo_mjy"], fuente_b["flujo_mjy"]
    if fa <= 0 or fb <= 0:
        return False
    return abs(math.log(fb / fa)) <= math.log(RAZON_MAXIMA_DE_BRILLO)


def proponer(fuentes, meta):
    """Devuelve la lista de parejas A-B entre fuentes huérfanas compatibles en separación y brillo.

    Cada fuente entra como mucho en una pareja: se asignan primero las más cercanas.
    """
    huerfanas_a = [f for f in fuentes if f["situacion"] == "huerfana" and f["epoca"] == "epoca_a"]
    huerfanas_b = [f for f in fuentes if f["situacion"] == "huerfana" and f["epoca"] == "epoca_b"]
    maxima = separacion_maxima_pixeles(meta)
    candidatas = []
    for a in huerfanas_a:
        for b in huerfanas_b:
            distancia = math.hypot(b["x"] - a["x"], b["y"] - a["y"])
            if distancia <= maxima and brillo_parecido(a, b):
                candidatas.append((distancia, a["id_fuente"], b["id_fuente"]))
    usadas, parejas = set(), []
    for _, ida, idb in sorted(candidatas):
        if ida in usadas or idb in usadas:
            continue
        usadas.update((ida, idb))
        parejas.append({"id_pareja": "p%03d" % (len(parejas) + 1), "id_fuente_a": ida, "id_fuente_b": idb})
    return parejas


def construir_fuentes_json(campo, fuentes, meta):
    """Monta el contenido de fuentes.json según contratos/fuentes.schema.json."""
    return {
        "_comentario": "Generado por m3_deteccion. Una pareja es una hipótesis, no un objeto confirmado.",
        "version_contrato": "1",
        "campo": campo,
        "epocas": {e: {"mjd": meta["epocas"][e]["mjd"]} for e in ("epoca_a", "epoca_b", "plantilla")},
        "fuentes": [{k: f[k] for k in CAMPOS_DE_FUENTE} for f in fuentes],
        "parejas": proponer(fuentes, meta),
    }


def proponer_campo(campo, raiz_datos="datos"):
    """Lee situaciones.json (m3) con meta.json (m2) y escribe fuentes.json. Devuelve su ruta."""
    raiz = Path(raiz_datos)
    directorio = raiz / "m3_deteccion" / campo
    situaciones = json.loads((directorio / "situaciones.json").read_text(encoding="utf-8"))
    meta = json.loads((raiz / "m2_alineacion" / campo / "meta.json").read_text(encoding="utf-8"))
    contenido = construir_fuentes_json(campo, situaciones["fuentes"], meta)
    ruta = directorio / "fuentes.json"
    ruta.write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python -m modulos.m3_deteccion.propuesta_parejas <campo>")
    ruta_escrita = proponer_campo(sys.argv[1])
    escrito = json.loads(ruta_escrita.read_text(encoding="utf-8"))
    print("%s: %d fuentes, %d parejas" % (ruta_escrita, len(escrito["fuentes"]), len(escrito["parejas"])))
