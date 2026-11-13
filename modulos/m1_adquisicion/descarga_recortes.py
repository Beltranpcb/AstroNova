# ============================================================================
# ARCHIVO: modulos/m1_adquisicion/descarga_recortes.py
# MODULO: m1_adquisicion (Lote A)
# ROL: Descarga el recorte FITS de cada exposición seleccionada.
# LEE: seleccion.json; servicio de recortes de IRSA.
# PRODUCE: datos/m1_adquisicion/<campo>/recortes/<id_exposicion>.fits.
# FUNCIONAMIENTO PREVISTO:
#   Recibe de seleccion_epocas.py: seleccion.json.
#   1. Añadir center, size a cada url_acceso  ->  URL de recorte
#   2. Pedir el recorte a IRSA  ->  bytes FITS
#   3. Guardar con el nombre archivo_recorte  ->  recortes FITS crudos
#   Entrega a m2, m6: recortes FITS crudos.
# VERIFICACION: Existe un FITS por exposición de seleccion.json; cada uno cumple contratos/recortes_fits.md.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
