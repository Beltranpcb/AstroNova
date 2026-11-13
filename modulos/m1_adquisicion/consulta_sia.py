# ============================================================================
# ARCHIVO: modulos/m1_adquisicion/consulta_sia.py
# MODULO: m1_adquisicion (Lote A)
# ROL: Lista las exposiciones de SPHEREx que cubren un campo objetivo.
# LEE: campos_objetivo.json; servicio SIA2 de IRSA.
# PRODUCE: datos/m1_adquisicion/<campo>/listado_exposiciones.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de campos_objetivo.json: centro, radio del campo.
#   1. Consultar SIA2 en las colecciones de SPHEREx  ->  tabla de exposiciones
#   2. Ordenar por t_min  ->  listado_exposiciones.json
#   Entrega a seleccion_epocas.py: listado_exposiciones.json.
# VERIFICACION: El listado sale ordenado por t_min; cada fila tiene identificador, t_min, detector, access_url.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
