import os
import subprocess

def buscar_heic(carpeta_fotos):
    archivos_heic = []
    for root, _, files in os.walk(carpeta_fotos):
        for file in files:
            if file.lower().endswith('.heic'):
                archivos_heic.append(os.path.join(root, file))
    return archivos_heic

def convertir_heic_a_jpg_con_exif(archivos_heic):
    convertidas = []
    errores = []

    for path_heic in archivos_heic:
        root, file = os.path.split(path_heic)
        nombre, _ = os.path.splitext(file)
        path_jpg = os.path.join(root, f"{nombre}.jpg")

        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", path_heic,
                "-frames:v", "1", path_jpg
            ], check=True)

            subprocess.run([
                "exiftool",
                "-TagsFromFile", path_heic,
                "-all:all",
                "-overwrite_original",
                path_jpg
            ], check=True)

            os.remove(path_heic)
            print(f"🆗 Convertido y metadatos copiados: {file}")
            convertidas.append(path_heic)

        except subprocess.CalledProcessError as e:
            print(f"❌ Error con {file}: {e}")
            errores.append(f"{file} - {e}")

    with open("reporte_conversion_heic.txt", "w") as r:
        r.write("🆗 Convertidas:\n")
        for f in convertidas:
            r.write(f"{f}\n")
        r.write("\n❌ Errores:\n")
        for f in errores:
            r.write(f"{f}\n")

    print("📄 Reporte generado: reporte_conversion_heic.txt")

# Main
carpeta = "/Users/adrianvidal/Downloads/year_2023_2024_"
archivos_heic = buscar_heic(carpeta)
print(f"🔍 Se encontraron {len(archivos_heic)} archivos .heic.")

if archivos_heic:
    confirmacion = input("¿Deseas convertirlos a JPG y copiar metadatos? (y/n): ").strip().lower()
    if confirmacion == 'y':
        convertir_heic_a_jpg_con_exif(archivos_heic)
    else:
        print("❎ Conversión cancelada.")
else:
    print("✅ No se encontraron archivos .heic.")
