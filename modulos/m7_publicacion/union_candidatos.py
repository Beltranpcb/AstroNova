# ============================================================================
# ARCHIVO: modulos/m7_publicacion/union_candidatos.py
# MODULO: m7_publicacion (Lote A)
# ROL: Une los resultados de cada pareja en candidatos.json.
# LEE: fuentes.json; movimiento.json; identificacion.json; espectros.json.
# PRODUCE: datos/m7_publicacion/<campo>/candidatos.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m3, m4, m5, m6: fuentes, movimiento, identificacion, espectros.
#   1. Unir las cuatro tablas por id_pareja  ->  registro por pareja
#   2. Omitir las parejas estacionarias  ->  candidatos.json
#   Entrega a indice_campos.py, control_publicacion.py, m9: candidatos.json.
# VERIFICACION: El archivo valida contra contratos/candidatos.schema.json; no contiene ninguna pareja de clase estacionaria.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
