# ============================================================================
# ARCHIVO: modulos/m2_alineacion/reproyeccion.py
# MODULO: m2_alineacion (Lote A)
# ROL: Reproyecta cada imagen sobre la rejilla de la época A.
# LEE: Recortes sin zodiacal.
# PRODUCE: epoca_a.fits, epoca_b.fits, plantilla.fits en datos/m2_alineacion/<campo>/.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de resta_zodiacal.py: recortes sin zodiacal.
#   1. Leer el WCS de la época A  ->  rejilla de referencia
#   2. Interpolar IMAGE, VARIANCE  ->  matrices alineadas
#   3. Reproyectar FLAGS por vecino más cercano  ->  máscara alineada
#   4. Guardar los tres archivos  ->  FITS alineados
#   Entrega a metadatos_campo.py, exportacion_png.py, m3: FITS alineados.
# VERIFICACION: Los tres FITS comparten forma de matriz con WCS idéntico; cumplen contratos/alineados_fits.md.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
