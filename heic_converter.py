import os
import subprocess

def convertir_heic_a_jpg_con_exif(carpeta_fotos):
    convertidas = []
    errores = []

    for root, _, files in os.walk(carpeta_fotos):
        for file in files:
            nombre, ext = os.path.splitext(file)
            if ext.lower() == '.heic':
                path_heic = os.path.join(root, file)
                path_jpg = os.path.join(root, f"{nombre}.jpg")

                try:
                    # Conversión con ffmpeg
                    subprocess.run([
                        "ffmpeg", "-y", "-i", path_heic,
                        "-frames:v", "1", path_jpg
                    ], check=True)

                    # Copiar metadatos con exiftool
                    subprocess.run([
                        "exiftool",
                        "-TagsFromFile", path_heic,
                        "-all:all",
                        "-overwrite_original",
                        path_jpg
                    ], check=True)

                    # Eliminar HEIC original
                    os.remove(path_heic)
                    print(f"🆗 Convertido y metadatos copiados: {file}")
                    convertidas.append(path_heic)

                except subprocess.CalledProcessError as e:
                    print(f"❌ Error con {file}: {e}")
                    errores.append(f"{file} - {e}")

    # Guardar reporte
    with open("reporte_conversion_heic.txt", "w") as r:
        r.write("🆗 Convertidas:\n")
        for f in convertidas:
            r.write(f"{f}\n")
        r.write("\n❌ Errores:\n")
        for f in errores:
            r.write(f"{f}\n")

    print("📄 Reporte generado: reporte_conversion_heic.txt")

# Ejecutar
convertir_heic_a_jpg_con_exif("/Users/adrianvidal/Downloads/year_2023_2024_")
