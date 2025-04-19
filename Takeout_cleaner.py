import os
import shutil
import hashlib

ruta_base = "/home/adrian/Descargas/Takeouts Google/"
ruta_destino_json = os.path.join(ruta_base, "json_files")

def hash_archivo(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

if not os.path.isdir(ruta_base):
    print("ERROR: La ruta indicada no existe.")
    exit(1)

print(f"Creando carpeta destino en: {ruta_destino_json}")
os.makedirs(ruta_destino_json, exist_ok=True)

hashes_existentes = {}

# Carga de hashes ya existentes
for f in os.listdir(ruta_destino_json):
    path_f = os.path.join(ruta_destino_json, f)
    if os.path.isfile(path_f):
        hashes_existentes[hash_archivo(path_f)] = f

print(f"Iniciando limpieza en: {ruta_base}")

for root, dirs, files in os.walk(ruta_base):
    for file in files:
        origen = os.path.join(root, file)
        if file.lower().endswith('.json'):
            h = hash_archivo(origen)
            if h in hashes_existentes:
                print(f"Duplicado detectado y eliminado: {origen}")
                os.remove(origen)
                continue
            destino = os.path.join(ruta_destino_json, file)
            contador = 1
            while os.path.exists(destino):
                base, ext = os.path.splitext(file)
                nuevo_nombre = f"{base}_{contador}{ext}"
                destino = os.path.join(ruta_destino_json, nuevo_nombre)
                contador += 1
            print(f"Moviendo JSON: {origen} -> {destino}")
            shutil.move(origen, destino)
            hashes_existentes[h] = os.path.basename(destino)
        else:
            print(f"Eliminando: {origen}")
            os.remove(origen)

print("Limpieza completada. Solo quedan los .json únicos en json_files")


