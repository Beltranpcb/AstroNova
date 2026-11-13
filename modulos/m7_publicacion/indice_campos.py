# ============================================================================
# ARCHIVO: modulos/m7_publicacion/indice_campos.py
# MODULO: m7_publicacion (Lote A)
# ROL: Escribe campos.json con la lista de campos publicados.
# LEE: Los directorios de datos/m7_publicacion/ con su meta.json, su candidatos.json.
# PRODUCE: datos/m7_publicacion/campos.json.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de union_candidatos.py, copia_publicable.py: candidatos.json, meta.json de cada campo.
#   1. Recorrer los campos publicados  ->  directorios de campo
#   2. Contar los candidatos de cada uno  ->  campos.json
#   Entrega a control_publicacion.py, m9: campos.json.
# VERIFICACION: El archivo valida contra contratos/campos.schema.json; numero_candidatos coincide con el recuento real.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
