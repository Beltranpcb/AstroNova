# ============================================================================
# ARCHIVO: modulos/m5_identificacion/consulta_catalogos.py
# MODULO: m5_identificacion (Lote B)
# ROL: Obtiene la respuesta del catálogo de cuerpos menores para cada pareja en movimiento.
# LEE: fuentes.json; movimiento.json; datos/m5_identificacion/cache/; API sb_ident de JPL.
# PRODUCE: Un archivo de respuesta por pareja en datos/m5_identificacion/cache/.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m3_deteccion, m4_movimiento: fuentes.json, movimiento.json.
#   1. Leer posición, fecha de cada pareja no estacionaria  ->  consultas pendientes
#   2. Buscar cada respuesta en la caché  ->  consultas sin respuesta guardada
#   3. Preguntar a JPL sb_ident, con MPChecker de alternativa  ->  respuesta nueva
#   4. Guardar la respuesta  ->  respuestas en cache/
#   Entrega a cruce_posicional.py: respuestas en cache/.
# VERIFICACION: Una segunda ejecución sobre el mismo campo no abre ninguna conexión de red.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
