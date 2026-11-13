# ============================================================================
# ARCHIVO: modulos/m6_huella_espectral/escritura_espectros.py
# MODULO: m6_huella_espectral (Lote C)
# ROL: Reúne medida, tipo, temperatura en el archivo del contrato.
# LEE: espectro_medido.json; tipo_espectral.json; temperatura.json.
# PRODUCE: datos/m6_huella_espectral/<campo>/espectros.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de comparacion_plantillas.py, ajuste_planck.py: tipo_espectral.json, temperatura.json.
#   1. Leer espectro_medido.json  ->  puntos por objeto
#   2. Unir por id_pareja  ->  registro por objeto
#   3. Escribir según el contrato  ->  espectros.json
#   Entrega a m7: espectros.json.
# VERIFICACION: El archivo valida contra contratos/espectros.schema.json; hay un espectro por pareja candidata medida.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
