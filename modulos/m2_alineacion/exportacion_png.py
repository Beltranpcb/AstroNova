# ============================================================================
# ARCHIVO: modulos/m2_alineacion/exportacion_png.py
# MODULO: m2_alineacion (Lote A)
# ROL: Exporta las imágenes PNG que la web muestra.
# LEE: FITS alineados.
# PRODUCE: epoca_a.png, epoca_b.png, diferencia.png en datos/m2_alineacion/<campo>/.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de reproyeccion.py: FITS alineados.
#   1. Calcular límites ZScale sobre la época A  ->  límites de contraste
#   2. Aplicar el mismo estirado asinh a las épocas A, B  ->  epoca_a.png, epoca_b.png
#   3. Restar B menos A con un mapa de dos tonos  ->  diferencia.png
#   Entrega a m7: diferencia.png.
# VERIFICACION: Los tres PNG miden 600 x 600 píxeles; las estrellas fijas no saltan al alternar epoca_a.png con epoca_b.png.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
