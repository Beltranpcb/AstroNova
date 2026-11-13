# ============================================================================
# ARCHIVO: modulos/m4_movimiento/clasificacion.py
# MODULO: m4_movimiento (Lote C)
# ROL: Asigna a cada pareja su clase de movimiento.
# LEE: cinematica.json; significancia.json.
# PRODUCE: datos/m4_movimiento/<campo>/movimiento.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de incertidumbre.py: significancia.json.
#   1. Leer la velocidad de cinematica.json  ->  medidas por pareja
#   2. Aplicar los umbrales de significancia  ->  clase por pareja
#   3. Escribir el resultado  ->  movimiento.json
#   Entrega a m5, m6, m7: movimiento.json.
# VERIFICACION: Significancia menor que 2 da estacionaria, entre 2 y 5 da no_concluyente, 5 o más da candidata; el archivo valida contra su esquema.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
