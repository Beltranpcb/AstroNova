/* ============================================================================
   ARCHIVO: modulos/m9_sitio/carga_datos.js
   MODULO: m9_sitio (Lote D)
   ROL: Lee los archivos publicados de un campo.
   LEE: campos.json, meta.json, candidatos.json, espectros.json de datos/m7_publicacion/ (o de contratos/ejemplos/ en modo prueba).
   PRODUCE: Los datos del campo en memoria para las vistas.
   FUNCIONAMIENTO PREVISTO:
     Recibe de m7_publicacion: campos.json, meta.json, candidatos.json, espectros.json.
     1. Leer campos.json  ->  lista de campos
     2. Leer los tres JSON del campo elegido  ->  datos sin comprobar
     3. Comprobar version_contrato  ->  datos del campo en memoria
     Entrega a vistas: datos del campo en memoria.
   VERIFICACION: Con contratos/ejemplos devuelve dos candidatos; con otra version_contrato falla nombrando el archivo.
   ESTADO: Esqueleto sin código. Este archivo solo documenta el trabajo pendiente.
   ============================================================================ */
