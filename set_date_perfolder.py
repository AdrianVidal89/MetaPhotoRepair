import os
import re
import subprocess
from tqdm import tqdm

## re-escribe los metadatos de fecha, basandose en la carpeta contenedora
## siguiendo una estructura apple - "3 de abril de 2002"
# Diccionario de meses en español

MESES = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

# Extensiones compatibles
EXTS = ('.jpg', '.jpeg', '.png', '.heic', '.cr2', '.nef', '.arw', '.dng', '.raf')

def extraer_fecha(nombre):
    nombre = nombre.lower()
    patron = r'(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})'
    match = re.search(patron, nombre)
    if not match:
        patron_alt = r'(\d{1,2})\s+([a-záéíóú]+)\s+(\d{4})'
        match = re.search(patron_alt, nombre)
    if match:
        dia, mes, anio = match.groups()
        mes_num = MESES.get(mes.strip(), "01")
        return f"{anio}:{mes_num}:{dia.zfill(2)} 00:00:00"
    return None

def escribir_fecha_exif(ruta, fecha):
    try:
        subprocess.run([
            "exiftool",
            f"-overwrite_original",
            f"-DateTimeOriginal={fecha}",
            f"-CreateDate={fecha}",
            f"-ModifyDate={fecha}",
            ruta
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        return False

def procesar_carpeta(carpeta):
    fecha = extraer_fecha(os.path.basename(carpeta))
    if not fecha:
        print(f"⚠️  No se detectó fecha en: {carpeta}")
        return 0, 0, 0

    fotos = [f for f in os.listdir(carpeta) if f.lower().endswith(EXTS)]
    total, ok, fail = 0, 0, 0

    for foto in tqdm(fotos, desc=f"📷 {os.path.basename(carpeta)}", leave=False):
        ruta_foto = os.path.join(carpeta, foto)
        total += 1
        if escribir_fecha_exif(ruta_foto, fecha):
            ok += 1
        else:
            fail += 1

    return total, ok, fail

def main(ruta_base):
    total, correctas, fallidas = 0, 0, 0
    for root, dirs, _ in os.walk(ruta_base):
        for carpeta in dirs:
            path = os.path.join(root, carpeta)
            t, o, f = procesar_carpeta(path)
            total += t
            correctas += o
            fallidas += f

    print("\n✅ Proceso finalizado:")
    print(f"   Total fotos encontradas: {total}")
    print(f"   Fotos corregidas: {correctas}")
    print(f"   Errores: {fallidas}")

    with open("log_resultados.txt", "w", encoding="utf-8") as f:
        f.write(f"Total fotos: {total}\n")
        f.write(f"Correctas: {correctas}\n")
        f.write(f"Fallidas: {fallidas}\n")

if __name__ == "__main__":
    main("/data")  # Cambiar si la ruta del volumen es diferente
