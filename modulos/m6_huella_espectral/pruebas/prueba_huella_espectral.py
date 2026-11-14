# ============================================================================
# ARCHIVO: modulos/m6_huella_espectral/pruebas/prueba_huella_espectral.py
# MODULO: m6_huella_espectral (Lote C)
# ROL: Comprueba el ajuste espectral sobre espectros sintéticos.
# LEE: Espectros sintéticos creados en memoria; recortes FITS sintéticos; esquemas/espectros.schema.json.
# PRODUCE: El veredicto de pytest.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de prueba: cuerpo negro de 300 K, espectro con pico en 4,26 micras.
#   1. Ejecutar comparación, ajuste de Planck  ->  tipo, temperatura
#   2. Comparar con cometa, con el intervalo de 270 a 330 K  ->  veredicto
#   Entrega a pytest: veredicto.
# VERIFICACION: Es el propio verificador: pasa cuando se cumplen los criterios de aceptación del módulo.
# USO: python -m pytest modulos/m6_huella_espectral/pruebas -q
# ESTRUCTURA: un bloque por archivo del módulo. El campo sintético (fixture `campo`) tiene tres
#             estrellas fijas y un objeto móvil de espectro plano conocido, en siete exposiciones.
# ESTADO: Parte 2 de 4 del Lote C. Cubre trayectoria.py y fotometria.py.
# ============================================================================
import json
from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area

from modulos.m6_huella_espectral import fotometria, trayectoria

MODULO = Path(__file__).resolve().parents[1]
LADO = 118
ESCALA_GRADOS = 6.15 / 3600
RUIDO = 0.01  # MJy/sr
ESTRELLAS = [(30.3, 25.7, 3.0), (85.6, 40.2, 2.0), (50.1, 95.4, 4.0)]
PIXEL_A, PIXEL_B = (64.4, 70.8), (69.4, 72.8)  # el objeto en la rejilla de referencia
MJD_A, MJD_B = 60900.0, 60900.25
FLUJO_MJY = 2.0  # espectro plano del objeto
BANDAS = {1: (0.75, 1.09), 2: (1.10, 1.62), 3: (1.63, 2.41), 4: (2.42, 3.82), 5: (3.83, 4.41), 6: (4.42, 5.00)}
# (id, papel, mjd, detector, desplazamiento del WCS en píxeles)
EXPOSICIONES = [("exp_a", "epoca_a", MJD_A, 3, (0.0, 0.0)),
                ("exp_b", "epoca_b", MJD_B, 3, (0.0, 0.0)),
                ("exp_t", "plantilla", 60720.0, 3, (0.0, 0.0)),
                ("exp_s1", "serie_espectral", 60900.04, 1, (0.0, 0.0)),
                ("exp_s2", "serie_espectral", 60900.10, 2, (2.3, -1.2)),
                ("exp_s5", "serie_espectral", 60900.16, 5, (0.0, 0.0)),
                ("exp_s6", "serie_espectral", 60900.22, 6, (-0.8, 0.5))]


def wcs_desplazado(dx, dy):
    w = WCS(naxis=2)
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    w.wcs.crval = [150.0, 2.0]
    w.wcs.crpix = [LADO / 2 + dx, LADO / 2 + dy]
    w.wcs.cdelt = [-ESCALA_GRADOS, ESCALA_GRADOS]
    return w


WCS_REFERENCIA = wcs_desplazado(0, 0)
A_MJY = 2 * np.pi * fotometria.SIGMA_PIXELES ** 2 * float(proj_plane_pixel_area(WCS_REFERENCIA)) * (np.pi / 180) ** 2 * 1e9


def cielo(pixel):
    ra, dec = WCS_REFERENCIA.pixel_to_world_values(*pixel)
    return float(ra), float(dec)


def gaussiana(x, y, pico):
    filas, columnas = np.indices((LADO, LADO))
    return pico * np.exp(-((columnas - x) ** 2 + (filas - y) ** 2) / (2 * fotometria.SIGMA_PIXELES ** 2))


def recorte(id_exposicion, mjd, detector, desplazamiento, flujo_objeto, semilla):
    """Recorte crudo con las seis extensiones; el objeto va en su posición prevista para esa fecha."""
    dx, dy = desplazamiento
    w = wcs_desplazado(dx, dy)
    azar = np.random.default_rng(semilla)
    zodi = 0.3 + 0.001 * np.indices((LADO, LADO))[1]
    imagen = zodi + azar.normal(0.0, RUIDO, (LADO, LADO))
    for x, y, pico in ESTRELLAS:
        imagen += gaussiana(x + dx, y + dy, pico)
    a, b = ({"ra_grados": r, "dec_grados": d} for r, d in (cielo(PIXEL_A), cielo(PIXEL_B)))
    ra, dec, _ = trayectoria.posicion_en(mjd, a, b, MJD_A, MJD_B)
    x, y = w.world_to_pixel_values(ra, dec)
    if flujo_objeto:
        imagen += gaussiana(float(x), float(y), flujo_objeto / A_MJY)
    lo, hi = BANDAS[detector]
    onda = np.linspace(lo, hi, LADO)[:, None] * np.ones((LADO, LADO))  # longitud de onda por fila
    cabecera = w.to_header()
    return fits.HDUList([fits.PrimaryHDU(),
                         fits.ImageHDU(imagen, cabecera, name="IMAGE"),
                         fits.ImageHDU(np.zeros((LADO, LADO), dtype=np.int32), cabecera, name="FLAGS"),
                         fits.ImageHDU(np.full((LADO, LADO), RUIDO ** 2), cabecera, name="VARIANCE"),
                         fits.ImageHDU(zodi, cabecera, name="ZODI"),
                         fits.ImageHDU(np.ones((5, 5)) / 25.0, name="PSF"),
                         fits.ImageHDU(onda, cabecera, name="WCS-WAVE")])


def escribir_campo(raiz, flujo_objeto=FLUJO_MJY):
    """Deja en raiz/ los datos de m1, m3 y m4 que m6 necesita para campo_prueba."""
    entrada = raiz / "m1_adquisicion" / "campo_prueba"
    (entrada / "recortes").mkdir(parents=True)
    exposiciones = []
    for semilla, (ide, papel, mjd, det, despl) in enumerate(EXPOSICIONES, 10):
        recorte(ide, mjd, det, despl, flujo_objeto, semilla).writeto(entrada / "recortes" / (ide + ".fits"))
        exposiciones.append({"id_exposicion": ide, "papel": papel, "mjd": mjd, "detector": det, "coleccion": "spherex_qr3",
                             "url_acceso": "https://ejemplo.invalid/%s.fits" % ide, "archivo_recorte": ide + ".fits"})
    (entrada / "seleccion.json").write_text(json.dumps({
        "version_contrato": "1", "campo": "campo_prueba", "nombre": "Campo de prueba",
        "centro": {"ra_grados": 150.0, "dec_grados": 2.0}, "radio_grados": 0.1, "exposiciones": exposiciones}), encoding="utf-8")

    def fuente(idf, epoca, pixel):
        ra, dec = cielo(pixel)
        return {"id_fuente": idf, "epoca": epoca, "ra_grados": ra, "dec_grados": dec, "x": pixel[0], "y": pixel[1],
                "flujo_mjy": FLUJO_MJY, "senal_ruido": 30.0, "incertidumbre_posicion_segarc": 0.5, "situacion": "huerfana"}
    (raiz / "m3_deteccion" / "campo_prueba").mkdir(parents=True)
    (raiz / "m3_deteccion" / "campo_prueba" / "fuentes.json").write_text(json.dumps({
        "version_contrato": "1", "campo": "campo_prueba",
        "epocas": {"epoca_a": {"mjd": MJD_A}, "epoca_b": {"mjd": MJD_B}, "plantilla": {"mjd": 60720.0}},
        "fuentes": [fuente("a001", "epoca_a", PIXEL_A), fuente("b001", "epoca_b", PIXEL_B),
                    fuente("a002", "epoca_a", (20.0, 20.0)), fuente("b002", "epoca_b", (20.3, 20.1))],
        "parejas": [{"id_pareja": "p001", "id_fuente_a": "a001", "id_fuente_b": "b001"},
                    {"id_pareja": "p002", "id_fuente_a": "a002", "id_fuente_b": "b002"}]}), encoding="utf-8")
    (raiz / "m4_movimiento" / "campo_prueba").mkdir(parents=True)
    (raiz / "m4_movimiento" / "campo_prueba" / "movimiento.json").write_text(json.dumps({
        "version_contrato": "1", "campo": "campo_prueba",
        "parejas": [{"id_pareja": "p001", "separacion_segarc": 33.1, "horas_transcurridas": 6.0, "velocidad_segarc_por_hora": 5.5,
                     "incertidumbre_velocidad": 0.12, "significancia": 46.8, "clase": "candidata"},
                    {"id_pareja": "p002", "separacion_segarc": 1.9, "horas_transcurridas": 6.0, "velocidad_segarc_por_hora": 0.3,
                     "incertidumbre_velocidad": 0.12, "significancia": 2.7, "clase": "no_concluyente"}]}), encoding="utf-8")
    return raiz


@pytest.fixture
def campo(tmp_path):
    return escribir_campo(tmp_path)


# ---------------------------------------------------------------- trayectoria
def prueba_la_posicion_prevista_coincide_con_a_y_con_b(campo):
    ruta = trayectoria.prever_campo("campo_prueba", raiz_datos=campo)
    objetos = json.loads(ruta.read_text(encoding="utf-8"))["objetos"]
    assert [o["id_pareja"] for o in objetos] == ["p001"]  # p002 es no_concluyente: no se mide
    por_id = {e["id_exposicion"]: e for e in objetos[0]["exposiciones"]}
    ra_a, dec_a = cielo(PIXEL_A)
    ra_b, dec_b = cielo(PIXEL_B)
    assert por_id["exp_a"]["ra_grados"] == pytest.approx(ra_a, abs=1e-6) and por_id["exp_a"]["dec_grados"] == pytest.approx(dec_a, abs=1e-6)
    assert por_id["exp_b"]["ra_grados"] == pytest.approx(ra_b, abs=1e-6) and por_id["exp_b"]["dec_grados"] == pytest.approx(dec_b, abs=1e-6)


def prueba_interpola_en_el_tiempo_y_descarta_la_plantilla(campo):
    objetos = json.loads(trayectoria.prever_campo("campo_prueba", raiz_datos=campo).read_text(encoding="utf-8"))["objetos"]
    ids = [e["id_exposicion"] for e in objetos[0]["exposiciones"]]
    assert ids == ["exp_a", "exp_s1", "exp_s2", "exp_s5", "exp_s6", "exp_b"]  # ordenadas por fecha
    assert objetos[0]["descartadas"] == [{"id_exposicion": "exp_t", "motivo": "fuera_del_intervalo"}]
    mitad = next(e for e in objetos[0]["exposiciones"] if e["id_exposicion"] == "exp_s2")  # mjd a 0,4 del intervalo
    ra_a, dec_a = cielo(PIXEL_A)
    ra_b, dec_b = cielo(PIXEL_B)
    assert mitad["dec_grados"] == pytest.approx(dec_a + 0.4 * (dec_b - dec_a), abs=1e-6)


def prueba_ascension_recta_no_salta_en_el_meridiano_cero():
    a, b = {"ra_grados": 359.99, "dec_grados": 0.0}, {"ra_grados": 0.01, "dec_grados": 0.0}
    ra, _, _ = trayectoria.posicion_en(0.5, a, b, 0.0, 1.0)
    assert ra == pytest.approx(0.0, abs=1e-9)
    assert trayectoria.diferencia_ra(0.01, 359.99) == pytest.approx(0.02)


def prueba_fuera_del_recorte_se_descarta():
    centro = {"ra_grados": 150.0, "dec_grados": 2.0}
    assert trayectoria.dentro_del_recorte(150.05, 2.05, centro, 0.1)
    assert not trayectoria.dentro_del_recorte(150.0, 2.11, centro, 0.1)
    seleccion = {"centro": centro, "radio_grados": 0.1, "exposiciones": [
        {"id_exposicion": "lejos", "archivo_recorte": "l.fits", "mjd": 1.9, "detector": 1}]}
    fuentes = {"epocas": {"epoca_a": {"mjd": 0.0}, "epoca_b": {"mjd": 1.0}},
               "fuentes": [{"id_fuente": "a001", "ra_grados": 150.0, "dec_grados": 2.0},
                           {"id_fuente": "b001", "ra_grados": 150.0, "dec_grados": 2.08}],
               "parejas": [{"id_pareja": "p001", "id_fuente_a": "a001", "id_fuente_b": "b001"}]}
    movimiento = {"parejas": [{"id_pareja": "p001", "clase": "candidata"}]}
    objeto = trayectoria.prever(seleccion, fuentes, movimiento)[0]
    assert objeto["exposiciones"] == []
    assert objeto["descartadas"][0]["motivo"] == "fuera_del_recorte"


# ----------------------------------------------------------------- fotometria
def prueba_recupera_el_flujo_y_la_longitud_de_onda(campo):
    trayectoria.prever_campo("campo_prueba", raiz_datos=campo)
    ruta = fotometria.medir_campo("campo_prueba", raiz_datos=campo)
    espectros = json.loads(ruta.read_text(encoding="utf-8"))["espectros"]
    assert len(espectros) == 1 and espectros[0]["agrupacion"] == "banda"
    puntos = espectros[0]["puntos"]
    assert [p["id_exposicion"] for p in puntos] == ["exp_a", "exp_s1", "exp_s2", "exp_s5", "exp_s6", "exp_b"]
    for p in puntos:
        assert abs(p["flujo_mjy"] - FLUJO_MJY) / FLUJO_MJY < 0.10, p
        assert p["error_mjy"] > 0 and p["senal_ruido"] > 5
        lo, hi = BANDAS[p["detector"]]
        assert lo <= p["longitud_onda_micras"] <= hi, p
        assert 0.75 <= p["longitud_onda_micras"] <= 5.0
    assert [p["mjd"] for p in puntos] == sorted(p["mjd"] for p in puntos)


def prueba_el_ajuste_sigue_al_objeto_en_un_wcs_desplazado(campo):
    """exp_s2 tiene el WCS desplazado (2,3, -1,2) píxeles: el centro ajustado debe caer donde está el objeto."""
    objetos = json.loads(trayectoria.prever_campo("campo_prueba", raiz_datos=campo).read_text(encoding="utf-8"))["objetos"]
    e = next(x for x in objetos[0]["exposiciones"] if x["id_exposicion"] == "exp_s2")
    with fits.open(campo / "m1_adquisicion" / "campo_prueba" / "recortes" / "exp_s2.fits") as hdul:
        medida = fotometria.medir_en_recorte(hdul, e["ra_grados"], e["dec_grados"])
        esperado = WCS(hdul["IMAGE"].header).world_to_pixel_values(e["ra_grados"], e["dec_grados"])
    assert medida is not None
    assert np.hypot(medida["x"] - float(esperado[0]), medida["y"] - float(esperado[1])) < 0.2


def prueba_senal_ruido_baja_promedia_por_detector(tmp_path):
    escribir_campo(tmp_path, flujo_objeto=0.04)  # unas 1,5 sigmas por banda
    trayectoria.prever_campo("campo_prueba", raiz_datos=tmp_path)
    espectros = json.loads(fotometria.medir_campo("campo_prueba", raiz_datos=tmp_path).read_text(encoding="utf-8"))["espectros"]
    e = espectros[0]
    assert e["agrupacion"] == "detector"
    detectores = [p["detector"] for p in e["puntos"]]
    assert len(detectores) == len(set(detectores)) <= 6
    assert next(p for p in e["puntos"] if p["detector"] == 3)["exposiciones_promediadas"] == 2  # exp_a y exp_b
    assert all(p["error_mjy"] > 0 for p in e["puntos"])


def prueba_sin_wcs_wave_falla_y_fuera_de_la_imagen_no_mide():
    hdul = recorte("x", MJD_A, 3, (0.0, 0.0), FLUJO_MJY, 1)
    ra, dec = WCS_REFERENCIA.pixel_to_world_values(1.0, 1.0)
    assert fotometria.medir_en_recorte(hdul, float(ra), float(dec)) is None  # en el borde no cabe la ventana
    del hdul["WCS-WAVE"]
    ra, dec = cielo(PIXEL_A)
    with pytest.raises(ValueError, match="WCS-WAVE"):
        fotometria.medir_en_recorte(hdul, ra, dec)
