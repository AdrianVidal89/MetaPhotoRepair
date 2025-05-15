import os
import subprocess
import json
from tqdm import tqdm

# Metadatos relevantes para identificar una cámara
CAMPOS_CLAVE = {
    "File:ImageWidth",
    "File:ImageHeight",
    "File:BitsPerSample",
    "File:ColorComponents",
    "File:YCbCrSubSampling",
    "EXIF:XResolution",
    "EXIF:YResolution",
    "EXIF:ResolutionUnit",
    "EXIF:ExifVersion",
    "EXIF:ComponentsConfiguration",
    "EXIF:ColorSpace",
    "EXIF:Compression",
    "Composite:ImageSize",
    "Composite:Megapixels"
}

def extraer_metadatos(foto_path):
    try:
        resultado = subprocess.run(
            ["exiftool", "-j", "-G", "-n", foto_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode != 0:
            return None
        datos = json.loads(resultado.stdout)
        if not datos:
            return None

        entrada = datos[0]
        filtro = {k: v for k, v in entrada.items() if k in CAMPOS_CLAVE}
        filtro["nombre_archivo"] = os.path.basename(foto_path)
        return filtro

    except Exception as e:
        print(f"❌ Error en {foto_path}: {e}")
        return None

def escanear_y_guardar(carpeta_raiz, salida_json):
    metadatos_lista = []

    rutas = []
    for root, _, files in os.walk(carpeta_raiz):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
                rutas.append(os.path.join(root, f))

    for ruta in tqdm(rutas, desc="Procesando imágenes", unit="img"):
        datos = extraer_metadatos(ruta)
        if datos:
            metadatos_lista.append(datos)

    with open(salida_json, "w", encoding="utf-8") as f:
        json.dump(metadatos_lista, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Archivo generado: {salida_json}")

# Ejecutar
if __name__ == "__main__":
    escanear_y_guardar("/Multimedia/Fotos/Photos backup/year_until 2022", "/Multimedia/Fotos/identificadores_camara.json")
