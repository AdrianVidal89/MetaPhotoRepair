import json
from tqdm import tqdm

# Cargar el JSON
with open("/Users/adrianvidal/Desktop/identificadores_camara.json", "r") as f:
    fotos = json.load(f)

# Foto referencia (misma cámara)
foto_referencia = {
    "File:BitsPerSample": 8,
    "File:ColorComponents": 3,
    "File:YCbCrSubSampling": "2 2",
    "EXIF:XResolution": 72,
    "EXIF:YResolution": 72,
    "EXIF:ResolutionUnit": 2,
    "EXIF:ExifVersion": "0210",
    "EXIF:ComponentsConfiguration": "1 2 3 0",
    "EXIF:ColorSpace": 1,
    "EXIF:Compression": 6,
}

# Comparador de metadatos
def misma_camara(foto):
    for k, v in foto_referencia.items():
        if foto.get(k) != v:
            return False
    return True

# Procesar con barra de progreso
coincidentes = []
for foto in tqdm(fotos, desc="Comparando fotos"):
    if misma_camara(foto):
        coincidentes.append(foto["nombre_archivo"])

# Guardar resultados
with open("coincidencias_misma_camara.txt", "w") as out:
    for nombre in coincidentes:
        out.write(nombre + "\n")

print(f"Total coincidencias: {len(coincidentes)}")
