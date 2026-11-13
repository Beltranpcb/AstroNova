# ============================================================================
# ARCHIVO: modulos/m2_alineacion/resta_zodiacal.py
# MODULO: m2_alineacion (Lote A)
# ROL: Resta la luz zodiacal de cada recorte crudo.
# LEE: seleccion.json; recortes FITS crudos con papel epoca_a, epoca_b, plantilla.
# PRODUCE: datos/m2_alineacion/<campo>/sin_zodiacal/*.fits (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m1_adquisicion: seleccion.json, recortes FITS crudos.
#   1. Abrir las extensiones IMAGE, ZODI  ->  dos matrices en MJy/sr
#   2. Calcular IMAGE menos ZODI  ->  imagen sin zodiacal
#   3. Guardar junto a VARIANCE, FLAGS  ->  recortes sin zodiacal
#   Entrega a reproyeccion.py: recortes sin zodiacal.
# VERIFICACION: La mediana de cada imagen resultante queda más cerca de cero que la mediana de IMAGE.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
