# ============================================================================
# ARCHIVO: modulos/m7_publicacion/copia_publicable.py
# MODULO: m7_publicacion (Lote A)
# ROL: Copia al directorio publicado los archivos que la web lee sin cambios.
# LEE: meta.json, epoca_a.png, epoca_b.png, diferencia.png de m2; espectros.json de m6.
# PRODUCE: Los mismos cinco archivos en datos/m7_publicacion/<campo>/.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de m2, m6: meta.json, tres PNG, espectros.json.
#   1. Localizar los cinco archivos del campo  ->  rutas de origen
#   2. Copiar a datos/m7_publicacion/campo  ->  archivos publicados
#   Entrega a control_publicacion.py, m9: archivos publicados.
# VERIFICACION: Cada copia es idéntica byte a byte a su original.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
