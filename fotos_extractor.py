import os
import shutil
from tqdm import tqdm

# CONFIGURACIÓN
archivo_txt = "coincidencias_misma_camara.txt"
carpeta_origen = "/Multimedia/Fotos/Photos backup/year_until 2022"  # CAMBIA ESTO
carpeta_destino = "/Multimedia/Fotos/Photos backup/MotorolaV15"   # CAMBIA ESTO

# Leer nombres del archivo
with open(archivo_txt, "r") as f:
    nombres = set(line.strip() for line in f if line.strip())

# Buscar y copiar archivos
copiados = 0
for root, _, files in os.walk(carpeta_origen):
    for file in tqdm(files, desc=f"Buscando y copiando", total=len(files), leave=False):
        if file in nombres:
            origen = os.path.join(root, file)
            destino = os.path.join(carpeta_destino, file)
            os.makedirs(carpeta_destino, exist_ok=True)
            shutil.copy2(origen, destino)
            copiados += 1
            nombres.discard(file)  # Evita copiar duplicados

print(f"Total copiados: {copiados}")
