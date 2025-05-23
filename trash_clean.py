import os
import time
from tqdm import tqdm

def es_archivo_basura(path):
    nombre = os.path.basename(path)
    return (
        "/.@" in path or
        "/." in path or
        nombre.startswith(".") or
        "thumb" in nombre.lower() or
        nombre.lower().endswith((".job_config", ".syncmeta")) or
        "foobar" in nombre
    )

def escanear_archivos(carpeta_base):
    print(f"Escaneando archivos en: {carpeta_base}...\n")
    todos_los_archivos = []
    for root, _, files in os.walk(carpeta_base):
        for file in files:
            full_path = os.path.join(root, file)
            todos_los_archivos.append(full_path)
    return todos_los_archivos

def clasificar_archivos(lista_archivos):
    basura = [f for f in lista_archivos if es_archivo_basura(f)]
    utiles = [f for f in lista_archivos if not es_archivo_basura(f)]
    return utiles, basura

def guardar_reporte_basura(basura):
    with open("reporte_basura.txt", "w") as r:
        r.write("🗑 Archivos marcados como basura:\n\n")
        for archivo in basura:
            r.write(f"{archivo}\n")
    print("📄 Reporte generado: reporte_basura.txt")

def eliminar_con_progreso(archivos):
    print("\n🗑 Borrando archivos basura...")
    for archivo in tqdm(archivos, desc="Progreso", unit="archivo"):
        try:
            os.remove(archivo)
        except Exception as e:
            print(f"⚠️ Error al borrar {archivo}: {e}")

def main():
    carpeta_objetivo = "/Multimedia/Fotos/"
    
    archivos = escanear_archivos(carpeta_objetivo)
    utiles, basura = clasificar_archivos(archivos)
    
    print("\n📊 Resumen del Escaneo:")
    print(f"Total de archivos: {len(archivos)}")
    print(f"Archivos útiles  : {len(utiles)}")
    print(f"Archivos basura  : {len(basura)}")

    if not basura:
        print("🎉 No hay archivos basura. Nada que borrar.")
        return

    guardar_reporte_basura(basura)

    decision = input("\n¿Deseas eliminar los archivos listados en 'reporte_basura.txt'? (y/n): ").strip().lower()
    if decision == "y":
        eliminar_con_progreso(basura)
        print("✅ Limpieza completada.")
    else:
        print("❌ Limpieza cancelada. No se borró nada.")

if __name__ == "__main__":
    main()
