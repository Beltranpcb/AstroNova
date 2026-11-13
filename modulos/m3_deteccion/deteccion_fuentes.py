# ============================================================================
# ARCHIVO: modulos/m3_deteccion/deteccion_fuentes.py
# MODULO: m3_deteccion (Lote B)
# ROL: Detecta las fuentes puntuales de cada imagen alineada.
# LEE: epoca_a.fits, epoca_b.fits, plantilla.fits.
# PRODUCE: datos/m3_deteccion/<campo>/detecciones.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m2_alineacion: FITS alineados.
#   1. Enmascarar los píxeles marcados en FLAGS  ->  imagen enmascarada
#   2. Estimar el fondo local  ->  imagen sin fondo
#   3. Buscar picos sobre 5 veces el ruido  ->  posiciones x, y
#   4. Calcular señal/ruido con VARIANCE  ->  detecciones.json
#   Entrega a emparejamiento.py: detecciones.json.
# VERIFICACION: Cada detección tiene señal/ruido mayor o igual que 5; su incertidumbre de posición nunca baja de 0,5 segundos de arco.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
