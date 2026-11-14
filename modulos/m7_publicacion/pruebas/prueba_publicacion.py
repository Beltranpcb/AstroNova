# ============================================================================
# ARCHIVO: modulos/m7_publicacion/pruebas/prueba_publicacion.py
# MODULO: m7_publicacion (Lote A)
# ROL: Comprueba la unión sobre los ejemplos de los contratos.
# LEE: Los siete JSON de modulos/m7_publicacion/ejemplos/.
# PRODUCE: El veredicto de pytest.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de prueba: ejemplos de los contratos.
#   1. Ejecutar unión, índice, control en un directorio temporal  ->  publicación temporal
#   2. Comparar con candidatos.json, campos.json de ejemplo  ->  veredicto
#   Entrega a pytest: veredicto.
# VERIFICACION: Es el propio verificador: pasa cuando se cumplen los criterios
#   de aceptación del módulo.
# USO: python -m pytest modulos/m7_publicacion/pruebas -q
# ============================================================================
"""Pruebas de m7_publicacion contra los ejemplos escritos a mano de contratos/.

El árbol de datos se monta en un directorio temporal: nunca se toca datos/ del
repositorio. Los ejemplos son la referencia de aceptación, de modo que si un
contrato cambia y estos archivos se actualizan, la prueba sigue el cambio.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[3]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from modulos.m7_publicacion.control_publicacion import validar  # noqa: E402
from modulos.m7_publicacion.copia_publicable import copiar_campo  # noqa: E402
from modulos.m7_publicacion.indice_campos import escribir_campos  # noqa: E402
from modulos.m7_publicacion.union_candidatos import unir_campo  # noqa: E402

CAMPO = "campo_ejemplo"
EJEMPLOS = RAIZ / "modulos" / "m7_publicacion" / "ejemplos"
CONTRATOS = RAIZ / "modulos" / "m7_publicacion" / "esquemas"

# (directorio de datos, archivo del ejemplo que se copia tal cual)
TABLAS_DE_ENTRADA = (
    ("m2_alineacion", "meta.json"),
    ("m3_deteccion", "fuentes.json"),
    ("m4_movimiento", "movimiento.json"),
    ("m5_identificacion", "identificacion.json"),
    ("m6_huella_espectral", "espectros.json"),
)

PNG_DE_EJEMPLO = b"\x89PNG\r\n\x1a\n" + b"m7_publicacion_prueba" * 4


def leer_json(ruta):
    """Lee un JSON en UTF-8."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def escribir_json(ruta, contenido):
    """Escribe un JSON en UTF-8."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=2)


def sin_comentario(documento):
    """Quita el comentario libre: no forma parte del contrato."""
    return {clave: valor for clave, valor in documento.items() if clave != "_comentario"}


def resumen(ruta):
    """Huella de un archivo, para comparar copias byte a byte."""
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


@pytest.fixture
def raiz_datos(tmp_path):
    """Monta un datos/ temporal con los ejemplos de los contratos."""
    raiz = tmp_path / "datos"
    origen = EJEMPLOS / CAMPO

    for directorio, archivo in TABLAS_DE_ENTRADA:
        destino = raiz / directorio / CAMPO / archivo
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen / archivo, destino)

    # m2 también produce los tres PNG; aquí basta con que existan y sean pequeños.
    for nombre in ("epoca_a.png", "epoca_b.png", "diferencia.png"):
        (raiz / "m2_alineacion" / CAMPO / nombre).write_bytes(PNG_DE_EJEMPLO)

    return raiz


@pytest.fixture
def publicado(raiz_datos):
    """Deja el campo ejemplo publicado (copia, unión e índice)."""
    copiar_campo(CAMPO, str(raiz_datos))
    unir_campo(CAMPO, str(raiz_datos))
    escribir_campos(str(raiz_datos))
    return raiz_datos


def prueba_union_coincide_con_el_ejemplo(raiz_datos):
    unir_campo(CAMPO, str(raiz_datos))
    obtenido = leer_json(raiz_datos / "m7_publicacion" / CAMPO / "candidatos.json")
    esperado = leer_json(EJEMPLOS / CAMPO / "candidatos.json")
    assert sin_comentario(obtenido) == sin_comentario(esperado)


def prueba_indice_coincide_con_el_ejemplo(publicado):
    obtenido = leer_json(publicado / "m7_publicacion" / "campos.json")
    esperado = leer_json(EJEMPLOS / "campos.json")
    assert sin_comentario(obtenido) == sin_comentario(esperado)


def prueba_copia_es_identica_byte_a_byte(raiz_datos):
    copiar_campo(CAMPO, str(raiz_datos))
    for directorio, nombre in (
        *(("m2_alineacion", n) for n in ("meta.json", "epoca_a.png", "epoca_b.png", "diferencia.png")),
        ("m6_huella_espectral", "espectros.json"),
    ):
        origen = raiz_datos / directorio / CAMPO / nombre
        destino = raiz_datos / "m7_publicacion" / CAMPO / nombre
        assert destino.is_file(), "no se copió %s" % nombre
        assert resumen(destino) == resumen(origen), "la copia de %s difiere" % nombre


def prueba_control_aprueba_la_publicacion(publicado):
    assert validar(str(publicado), str(CONTRATOS)) == []


def prueba_union_omite_las_parejas_estacionarias(raiz_datos):
    ruta = raiz_datos / "m4_movimiento" / CAMPO / "movimiento.json"
    movimiento = leer_json(ruta)
    movimiento["parejas"].append(
        {
            "id_pareja": "p003",
            "separacion_segarc": 0.3,
            "horas_transcurridas": 6.0,
            "velocidad_segarc_por_hora": 0.05,
            "incertidumbre_velocidad": 0.2,
            "significancia": 0.25,
            "clase": "estacionaria",
        }
    )
    escribir_json(ruta, movimiento)

    unir_campo(CAMPO, str(raiz_datos))
    candidatos = leer_json(raiz_datos / "m7_publicacion" / CAMPO / "candidatos.json")["candidatos"]
    assert [c["id_candidato"] for c in candidatos] == ["p001", "p002"]
    assert all(c["clase_movimiento"] != "estacionaria" for c in candidatos)


def prueba_union_falla_si_falta_una_identificacion(raiz_datos):
    ruta = raiz_datos / "m5_identificacion" / CAMPO / "identificacion.json"
    identificacion = leer_json(ruta)
    identificacion["identificaciones"] = [
        i for i in identificacion["identificaciones"] if i["id_pareja"] != "p002"
    ]
    escribir_json(ruta, identificacion)

    with pytest.raises(ValueError) as error:
        unir_campo(CAMPO, str(raiz_datos))
    assert "p002" in str(error.value)


def prueba_union_falla_si_el_campo_no_coincide(raiz_datos):
    ruta = raiz_datos / "m3_deteccion" / CAMPO / "fuentes.json"
    fuentes = leer_json(ruta)
    fuentes["campo"] = "otro_campo"
    escribir_json(ruta, fuentes)

    with pytest.raises(ValueError) as error:
        unir_campo(CAMPO, str(raiz_datos))
    assert "otro_campo" in str(error.value)


def prueba_control_rechaza_un_candidato_fuera_de_contrato(publicado):
    ruta = publicado / "m7_publicacion" / CAMPO / "candidatos.json"
    candidatos = leer_json(ruta)
    candidatos["candidatos"][0]["estado"] = "dudoso"
    escribir_json(ruta, candidatos)

    problemas = validar(str(publicado), str(CONTRATOS))
    assert problemas
    assert any("estado" in problema for problema in problemas)


def prueba_control_rechaza_un_archivo_de_mas_de_un_megabyte(publicado):
    (publicado / "m7_publicacion" / CAMPO / "sobrante.bin").write_bytes(b"0" * (1024 * 1024 + 1))

    problemas = validar(str(publicado), str(CONTRATOS))
    assert any("1 MB" in problema for problema in problemas)


def prueba_control_rechaza_un_campo_incompleto(publicado):
    (publicado / "m7_publicacion" / CAMPO / "espectros.json").unlink()

    problemas = validar(str(publicado), str(CONTRATOS))
    assert any("falta espectros.json" in problema for problema in problemas)


def prueba_control_rechaza_un_indice_desfasado(publicado):
    ruta = publicado / "m7_publicacion" / "campos.json"
    indice = leer_json(ruta)
    indice["campos"][0]["numero_candidatos"] = 99
    escribir_json(ruta, indice)

    problemas = validar(str(publicado), str(CONTRATOS))
    assert any("99" in problema for problema in problemas)


def prueba_control_rechaza_un_json_ilegible(publicado):
    (publicado / "m7_publicacion" / CAMPO / "meta.json").write_text("{ no es json", encoding="utf-8")

    problemas = validar(str(publicado), str(CONTRATOS))
    assert any("JSON ilegible" in problema for problema in problemas)


def prueba_control_sale_con_codigo_cero_por_linea_de_ordenes(publicado, tmp_path):
    """La orden documentada debe poder ejecutarse tal cual, sin argumentos.

    Se ejecuta desde un directorio ajeno al repositorio y sin `contratos/`:
    el control debe encontrar por sí solo los esquemas que viajan con el módulo.
    """

    entorno = dict(os.environ)
    entorno["PYTHONPATH"] = str(RAIZ)
    proceso = subprocess.run(
        [sys.executable, "-m", "modulos.m7_publicacion.control_publicacion"],
        cwd=str(tmp_path),
        env=entorno,
        capture_output=True,
        text=True,
    )
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    assert "Publicación válida" in proceso.stdout
