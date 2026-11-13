# ============================================================================
# ARCHIVO: modulos/m6_huella_espectral/trayectoria.py
# MODULO: m6_huella_espectral (Lote C)
# ROL: Predice dónde está el objeto en el instante de cada exposición.
# LEE: seleccion.json; fuentes.json; movimiento.json.
# PRODUCE: datos/m6_huella_espectral/<campo>/posiciones_previstas.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m1, m3, m4: seleccion.json, fuentes.json, movimiento.json.
#   1. Leer las posiciones A, B de cada pareja candidata  ->  dos puntos con fecha
#   2. Interpolar linealmente en el tiempo  ->  posición por exposición
#   3. Descartar las exposiciones sin el objeto dentro del recorte  ->  posiciones_previstas.json
#   Entrega a fotometria.py: posiciones_previstas.json.
# VERIFICACION: La posición prevista en la fecha de la época A coincide con la observada en A, igual que en B.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
