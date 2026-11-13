# ============================================================================
# ARCHIVO: modulos/m6_huella_espectral/comparacion_plantillas.py
# MODULO: m6_huella_espectral (Lote C)
# ROL: Asigna al espectro medido el tipo de la plantilla más parecida.
# LEE: espectro_medido.json; plantillas.json.
# PRODUCE: datos/m6_huella_espectral/<campo>/tipo_espectral.json (intermedio interno).
# FUNCIONAMIENTO PREVISTO:
#   Recibe de fotometria.py: espectro_medido.json.
#   1. Leer las cuatro curvas de plantillas.json  ->  plantillas remuestreadas
#   2. Escalar cada plantilla por mínimos cuadrados  ->  chi cuadrado reducido por tipo
#   3. Elegir el menor  ->  tipo_espectral.json
#   Entrega a escritura_espectros.py: tipo_espectral.json.
# VERIFICACION: Cada objeto recibe un chi cuadrado reducido por plantilla; el tipo es el del menor, o indeterminado si ninguno baja del umbral.
# ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
# ============================================================================
