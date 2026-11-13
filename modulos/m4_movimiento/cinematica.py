# ============================================================================
# ARCHIVO: modulos/m4_movimiento/cinematica.py
# MODULO: m4_movimiento (Lote C)
# ROL: Calcula la velocidad angular de cada pareja propuesta.
# LEE: fuentes.json.
# PRODUCE: datos/m4_movimiento/<campo>/cinematica.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m3_deteccion: fuentes.json.
#   1. Leer posiciones, fechas de cada pareja  ->  coordenadas, MJD
#   2. Calcular la separación angular sobre la esfera  ->  separación en segundos de arco
#   3. Dividir por las horas transcurridas  ->  cinematica.json
#   Entrega a incertidumbre.py, clasificacion.py: cinematica.json.
# VERIFICACION: La separación se mide sobre la esfera; la velocidad es separación entre horas transcurridas.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
