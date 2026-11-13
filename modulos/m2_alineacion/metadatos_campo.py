# ============================================================================
# ARCHIVO: modulos/m2_alineacion/metadatos_campo.py
# MODULO: m2_alineacion (Lote A)
# ROL: Escribe meta.json con los datos del campo alineado.
# LEE: Cabeceras de los FITS alineados; seleccion.json.
# PRODUCE: datos/m2_alineacion/<campo>/meta.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de reproyeccion.py: FITS alineados.
#   1. Leer fechas MJD, detector, tamaño de las cabeceras  ->  datos de las épocas
#   2. Leer nombre, centro de seleccion.json  ->  identidad del campo
#   3. Calcular las horas entre A, B  ->  meta.json
#   Entrega a m3, m7: meta.json.
# VERIFICACION: El archivo valida contra contratos/meta.schema.json; horas_entre_a_b coincide con la resta de las dos fechas MJD.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
