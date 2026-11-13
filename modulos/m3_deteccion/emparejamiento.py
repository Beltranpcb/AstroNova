# ============================================================================
# ARCHIVO: modulos/m3_deteccion/emparejamiento.py
# MODULO: m3_deteccion (Lote B)
# ROL: Separa las fuentes estacionarias de las fuentes huérfanas.
# LEE: detecciones.json.
# PRODUCE: datos/m3_deteccion/<campo>/situaciones.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de deteccion_fuentes.py: detecciones.json.
#   1. Emparejar por posición en el cielo entre A, B, plantilla  ->  coincidencias
#   2. Marcar estacionaria toda fuente fija en las tres imágenes  ->  fuentes estacionarias
#   3. Marcar huérfana toda fuente sin coincidencia  ->  situaciones.json
#   Entrega a propuesta_parejas.py: situaciones.json.
# VERIFICACION: Toda fuente recibe una situacion; ninguna fuente presente a menos de 1 píxel en las tres imágenes queda como huérfana.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
