# ============================================================================
# ARCHIVO: modulos/m1_adquisicion/seleccion_epocas.py
# MODULO: m1_adquisicion (Lote A)
# ROL: Elige qué exposiciones cumplen cada papel del contrato de selección.
# LEE: listado_exposiciones.json.
# PRODUCE: datos/m1_adquisicion/<campo>/seleccion.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de consulta_sia.py: listado_exposiciones.json.
#   1. Agrupar por detector  ->  grupos por detector
#   2. Elegir época A, época B separadas horas o días  ->  pareja A-B
#   3. Elegir la plantilla de la otra pasada  ->  trío del mismo detector
#   4. Añadir la serie espectral de todos los detectores  ->  seleccion.json
#   Entrega a descarga_recortes.py, m2, m6: seleccion.json.
# VERIFICACION: El archivo valida contra contratos/seleccion.schema.json con un único epoca_a, un único epoca_b, una única plantilla.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
