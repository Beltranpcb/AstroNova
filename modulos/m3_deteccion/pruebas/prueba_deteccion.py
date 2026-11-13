# ============================================================================
# ARCHIVO: modulos/m3_deteccion/pruebas/prueba_deteccion.py
# MODULO: m3_deteccion (Lote B)
# ROL: Comprueba la detección sobre imágenes de ruido con fuentes inyectadas.
# LEE: Tres imágenes sintéticas creadas en memoria; contratos/fuentes.schema.json.
# PRODUCE: El veredicto de pytest.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de prueba: FITS sintéticos con una fuente desplazada.
#   1. Ejecutar detección, emparejamiento, propuesta  ->  fuentes.json temporal
#   2. Comparar con las posiciones inyectadas  ->  error en píxeles
#   3. Validar contra fuentes.schema.json  ->  veredicto
#   Entrega a pytest: veredicto.
# VERIFICACION: Es el propio verificador: pasa cuando se cumplen los criterios de aceptación del módulo.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
