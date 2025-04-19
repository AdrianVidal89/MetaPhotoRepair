import os
import subprocess
import json

extensiones_soportadas = ['.jpg', '.jpeg', '.png', '.heic', '.cr2', '.nef', '.arw', '.dng', '.raf']

def insertar_gps_manual(carpeta_json, carpeta_fotos):
    archivos_json = {f.lower(): f for f in os.listdir(carpeta_json)}

    for archivo_foto in os.listdir(carpeta_fotos):
        _, ext = os.path.splitext(archivo_foto)
        if ext.lower() not in extensiones_soportadas:
            continue

        archivo_json_esperado = f"{archivo_foto}.supplemental-metadata.json".lower()
        if archivo_json_esperado in archivos_json:
            archivo_json_real = archivos_json[archivo_json_esperado]
            ruta_json = os.path.join(carpeta_json, archivo_json_real)
            ruta_foto = os.path.join(carpeta_fotos, archivo_foto)

            with open(ruta_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
                lat = datos.get("geoData", {}).get("latitude")
                lon = datos.get("geoData", {}).get("longitude")

                if lat is not None and lon is not None:
                    print(f"✅ Insertando GPS en: {archivo_foto}")
                    subprocess.run([
                        "exiftool",
                        f"-GPSLatitude={lat}",
                        f"-GPSLongitude={lon}",
                        f"-GPSLatitudeRef={'N' if lat >= 0 else 'S'}",
                        f"-GPSLongitudeRef={'E' if lon >= 0 else 'W'}",
                        "-overwrite_original",
                        ruta_foto
                    ], check=True)
                    print(f"🗺️  GPS insertado: ({lat}, {lon})\n")
                else:
                    print(f"⚠️  El JSON no tiene datos GPS para: {archivo_foto}")
        else:
            print(f"🚫 Sin metadatos para: {archivo_foto}")

# Ejemplo de uso
insertar_gps_manual(
    carpeta_json="/home/adrian/Descargas/Takeouts Google/json_files",
    carpeta_fotos="/home/adrian/Imágenes/"
)
