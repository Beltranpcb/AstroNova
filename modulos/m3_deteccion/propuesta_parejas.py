# ============================================================================
# ARCHIVO: modulos/m3_deteccion/propuesta_parejas.py
# MODULO: m3_deteccion (Lote B)
# ROL: Propone parejas A-B entre las fuentes huérfanas.
# LEE: situaciones.json; meta.json.
# PRODUCE: datos/m3_deteccion/<campo>/fuentes.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de emparejamiento.py: situaciones.json.
#   1. Leer las horas entre A, B de meta.json  ->  separación máxima admisible
#   2. Filtrar por separación, brillo parecido  ->  parejas compatibles
#   3. Escribir fuentes con parejas  ->  fuentes.json
#   Entrega a m4, m5, m6, m7: fuentes.json.
# VERIFICACION: El archivo valida contra contratos/fuentes.schema.json; toda pareja une una fuente de epoca_a con una de epoca_b.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
