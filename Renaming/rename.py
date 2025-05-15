import os
import json

# Cargar archivo JSON
with open("nombres_sugeridos.json", "r", encoding="utf-8") as f:
    nombres = json.load(f)

# Crear diccionario para acceso rápido
mapa_renombrado = {item["nombre_actual"]: item["nombre_nuevo"] for item in nombres}

# Carpeta base donde buscar las imágenes
carpeta_base = "/Users/adrianvidal/Library/CloudStorage/OneDrive-Personal/vCloudDocuments/Multimedia/Photos/0_Raw Photos for Edition"
renombrados = []
no_encontrados = []

# Buscar y renombrar
for root, _, files in os.walk(carpeta_base):
    for file in files:
        if file in mapa_renombrado:
            path_original = os.path.join(root, file)
            extension = os.path.splitext(file)[1]
            nuevo_nombre = mapa_renombrado[file] + extension
            path_nuevo = os.path.join(root, nuevo_nombre)
            try:
                os.rename(path_original, path_nuevo)
                renombrados.append((file, nuevo_nombre))
                print(f"✅ Renombrado: {file} → {nuevo_nombre}")
            except Exception as e:
                print(f"❌ Error renombrando {file}: {e}")
        else:
            no_encontrados.append(file)

# Resumen
print(f"\n📄 Total renombrados: {len(renombrados)}")
print(f"🔍 Archivos en JSON que no se encontraron: {len(mapa_renombrado) - len(renombrados)}")