import os
import json
import shutil
import subprocess
from tqdm import tqdm

# Huella del dispositivo
referencia = {
    "ImageWidth": 640,
    "ImageHeight": 480,
    "ExifVersion": "0210",
    "ComponentsConfiguration": "1 2 3 0",
    "Compression": 6,
    "ResolutionUnit": 2,
    "XResolution": 72,
    "YResolution": 72,
    "ColorSpace": 1,
    "BitsPerSample": 8,
    "YCbCrSubSampling": "2 2"
}

def extraer_metadatos(foto_path):
    try:
        resultado = subprocess.run(
            ["exiftool", "-j", "-n", "-G", foto_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode != 0:
            return None
        datos = json.loads(resultado.stdout)
        return datos[0] if datos else None
    except Exception as e:
        print(f"❌ Error extrayendo metadatos de {foto_path}: {e}")
        return None

def coincide_con_referencia(meta):
    return all(str(meta.get(f"EXIF:{k}", meta.get(f"File:{k}", meta.get(k)))) == str(v)
               for k, v in referencia.items())

def escanear_y_copiar(carpeta_origen, carpeta_destino):
    os.makedirs(carpeta_destino, exist_ok=True)
    coincidencias = []

    for root, _, files in os.walk(carpeta_origen):
        for nombre in files:
            if nombre.lower().endswith((".jpg", ".jpeg", ".heic", ".png")):
                ruta = os.path.join(root, nombre)
                metadatos = extraer_metadatos(ruta)
                if metadatos and coincide_con_referencia(metadatos):
                    destino = os.path.join(carpeta_destino, nombre)
                    try:
                        shutil.copy2(ruta, destino)
                        coincidencias.append(ruta)
                        print(f"✅ Copiado: {nombre}")
                    except Exception as e:
                        print(f"❌ Error copiando {ruta}: {e}")

    with open("coincidencias_motorolaV15.json", "w", encoding="utf-8") as f:
        json.dump(coincidencias, f, indent=2, ensure_ascii=False)

    print(f"\n📁 Finalizado. Total copiados: {len(coincidencias)}")
    print(f"📄 Log en: coincidencias_motorolaV15.json")

# USO: cambia esta línea por la ruta real
escanear_y_copiar("/Users/adrianvidal/Desktop/", "/Users/adrianvidal/Desktop/MotorolaV15")
