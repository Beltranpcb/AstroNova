# ============================================================================
# ARCHIVO: modulos/m2_alineacion/pruebas/prueba_alineacion.py
# MODULO: m2_alineacion (Lote A)
# ROL: Comprueba la alineación sobre imágenes sintéticas con estrellas desplazadas.
# LEE: Dos imágenes sintéticas creadas en memoria; contratos/meta.schema.json.
# PRODUCE: El veredicto de pytest.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de prueba: recortes sintéticos con WCS desplazado.
#   1. Ejecutar la reproyección  ->  FITS alineados temporales
#   2. Medir los centroides de las estrellas  ->  desviación en píxeles
#   3. Comparar con 0,2 píxeles  ->  veredicto
#   Entrega a pytest: veredicto.
# VERIFICACION: Es el propio verificador: pasa cuando se cumplen los criterios de aceptación del módulo.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
