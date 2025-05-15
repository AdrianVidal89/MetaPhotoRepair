import os
import json
import requests
import time
import re
from tqdm import tqdm

def dms_a_decimal(dms_str, ref):
    """Convierte '43 deg 17' 47.91"' y 'North' a 43.29664"""
    match = re.match(r"(\d+)\D+(\d+)\D+([\d.]+)", dms_str)
    if not match:
        return None
    grados, minutos, segundos = map(float, match.groups())
    decimal = grados + minutos / 60 + segundos / 3600
    if ref in ("S", "South", "W", "West"):
        decimal = -decimal
    return decimal

def obtener_ubicacion(lat, lon):
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "json",
            "lat": lat,
            "lon": lon,
            "zoom": 10,
            "addressdetails": 1
        }
        headers = {"User-Agent": "MiScriptGeo/1.0"}
        respuesta = requests.get(url, params=params, headers=headers)
        if respuesta.status_code == 200:
            data = respuesta.json()
            return data.get("display_name", "").split(",")[0]
        else:
            print(f"❌ Error HTTP {respuesta.status_code} en {lat}, {lon}")
            return "SinUbicacion"
    except Exception as e:
        print(f"❌ Excepción obteniendo ubicación para {lat},{lon}: {e}")
        return "SinUbicacion"

def generar_nombres_sugeridos(path_json):
    with open(path_json, "r", encoding="utf-8") as f:
        fotos = json.load(f)

    sugerencias = []

    for foto in tqdm(fotos, desc="Procesando fotos", unit="foto"):
        ruta = foto.get("ruta") or foto.get("SourceFile")
        if not ruta:
            print("⚠️ Sin campo 'ruta', se omite:", foto)
            continue

        nombre_actual = os.path.basename(ruta)
        fecha = foto.get("fecha") or foto.get("EXIF:DateTimeOriginal", "SinFecha")

        lat_dms = foto.get("EXIF:GPSLatitude")
        lat_ref = foto.get("EXIF:GPSLatitudeRef")
        lon_dms = foto.get("EXIF:GPSLongitude")
        lon_ref = foto.get("EXIF:GPSLongitudeRef")

        print(f"📸 Procesando: {nombre_actual}")
        print(f"   Fecha: {fecha}")
        print(f"   Coordenadas EXIF: {lat_dms} {lat_ref}, {lon_dms} {lon_ref}")

        if lat_dms and lat_ref and lon_dms and lon_ref:
            lat = dms_a_decimal(lat_dms, lat_ref)
            lon = dms_a_decimal(lon_dms, lon_ref)
            if lat is not None and lon is not None:
                ubicacion = obtener_ubicacion(lat, lon)
                time.sleep(1)
            else:
                print("⚠️ Coordenadas inválidas tras conversión.")
                ubicacion = "SinUbicacion"
        else:
            ubicacion = "SinUbicacion"

        nombre_nuevo = f"{ubicacion}_{fecha.replace(':', '-')}".strip()

        sugerencias.append({
            "nombre_actual": nombre_actual,
            "nombre_nuevo": nombre_nuevo
        })

        print(f"✅ {nombre_actual} → {nombre_nuevo}\n")

    with open("nombres_sugeridos.json", "w", encoding="utf-8") as f:
        json.dump(sugerencias, f, indent=2, ensure_ascii=False)

    print("\n📄 Archivo generado: nombres_sugeridos.json")

# Ejecutar
generar_nombres_sugeridos("metadatos_obtenidos.json")
