# ============================================================================
# ARCHIVO: modulos/m6_huella_espectral/ajuste_planck.py
# MODULO: m6_huella_espectral (Lote C)
# ROL: Estima la temperatura del objeto ajustando la ley de Planck.
# LEE: espectro_medido.json.
# PRODUCE: datos/m6_huella_espectral/<campo>/temperatura.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de fotometria.py: espectro_medido.json.
#   1. Separar los puntos del continuo  ->  puntos fuera de bandas
#   2. Ajustar Planck por mínimos cuadrados  ->  temperatura con incertidumbre
#   3. Aplicar la ley de Wien  ->  temperatura.json
#   Entrega a escritura_espectros.py: temperatura.json.
# VERIFICACION: El producto del pico de Wien por la temperatura vale 2898 micras kelvin con un error menor que 1.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
