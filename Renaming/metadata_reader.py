import os
import json
import subprocess

EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.heic', '.arw', '.cr2', '.nef', '.rw2', '.orf', '.dng')

def extraer_metadatos(path_imagen):
    try:
        resultado = subprocess.run(
            ["exiftool", "-j", "-G", path_imagen],
            capture_output=True, text=True, check=True
        )
        datos = json.loads(resultado.stdout)
        return datos[0] if datos else {}
    except Exception as e:
        print(f"⚠️ Error leyendo {path_imagen}: {e}")
        return {}

def procesar_directorio(carpeta_base):
    metadatos_todos = []

    for root, _, files in os.walk(carpeta_base):
        for file in files:
            if file.lower().endswith(EXTENSIONES_VALIDAS):
                path_imagen = os.path.join(root, file)
                metadatos = extraer_metadatos(path_imagen)
                if metadatos:
                    metadatos_todos.append(metadatos)
                    print(f"✅ Metadatos leídos: {path_imagen}")

    # Guardar en archivo único en la carpeta del script
    path_salida = os.path.join(os.path.dirname(__file__), "metadatos_obtenidos.json")
    with open(path_salida, "w", encoding="utf-8") as f:
        json.dump(metadatos_todos, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Todos los metadatos guardados en: {path_salida}")

# Ejecutar
carpeta = "/Users/adrianvidal/Library/CloudStorage/OneDrive-Personal/vCloudDocuments/Multimedia/Photos/0_Raw Photos for Edition"
procesar_directorio(carpeta)