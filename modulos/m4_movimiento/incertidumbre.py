# ============================================================================
# ARCHIVO: modulos/m4_movimiento/incertidumbre.py
# MODULO: m4_movimiento (Lote C)
# ROL: Propaga la incertidumbre de posición hasta la velocidad.
# LEE: fuentes.json; cinematica.json.
# PRODUCE: datos/m4_movimiento/<campo>/significancia.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de cinematica.py: cinematica.json.
#   1. Leer las incertidumbres de posición de fuentes.json  ->  sigma de A, sigma de B
#   2. Combinar en cuadratura  ->  sigma de la separación
#   3. Dividir la separación entre su sigma  ->  significancia.json
#   Entrega a clasificacion.py: significancia.json.
# VERIFICACION: La incertidumbre de la separación es la suma en cuadratura de las dos incertidumbres de posición.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
