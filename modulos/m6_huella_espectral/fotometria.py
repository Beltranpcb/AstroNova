# ============================================================================
# ARCHIVO: modulos/m6_huella_espectral/fotometria.py
# MODULO: m6_huella_espectral (Lote C)
# ROL: Mide el flujo del objeto en cada exposición de la serie espectral.
# LEE: posiciones_previstas.json; recortes FITS crudos.
# PRODUCE: datos/m6_huella_espectral/<campo>/espectro_medido.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de trayectoria.py: posiciones_previstas.json.
#   1. Restar ZODI de IMAGE en cada recorte  ->  imagen sin zodiacal
#   2. Leer la longitud de onda del píxel en WCS-WAVE  ->  longitud de onda en micras
#   3. Ajustar la PSF en la posición prevista  ->  flujo con error
#   4. Promediar por detector cuando la señal/ruido es baja  ->  espectro_medido.json
#   Entrega a comparacion_plantillas.py, ajuste_planck.py, escritura_espectros.py: espectro_medido.json.
# VERIFICACION: Cada punto tiene longitud de onda entre 0,75 y 5,0 micras, flujo, error positivo, fecha MJD.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
