import os
import cv2
import subprocess

# --- SUPERRESOLUCIÓN CON EDSR ---

def mejorar_con_EDSR(input_path, output_path, modelo_pb="EDSR_x4.pb"):
    print("🔧 [EDSR] Cargando modelo...")
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(modelo_pb)
    sr.setModel("edsr", 4)

    print(f"🖼️ [EDSR] Escalando imagen: {input_path}")
    img = cv2.imread(input_path)
    result = sr.upsample(img)
    cv2.imwrite(output_path, result)
    print(f"✅ [EDSR] Imagen guardada: {output_path}")

# --- MEJORA VISUAL CON CODEFORMER ---

def mejorar_con_CodeFormer(input_path, output_dir="output_codeformer"):
    os.makedirs(output_dir, exist_ok=True)

    comando = [
        "python", "inference_codeformer.py",
        "-i", input_path,
        "-o", output_dir,
        "-w", "0.7",
        "--face_upsample"
    ]

    print("🧠 [CodeFormer] Ejecutando mejora IA...")
    subprocess.run(comando, cwd="CodeFormer")
    print("✅ [CodeFormer] Mejora completada.")

# --- EJECUCIÓN PRINCIPAL ---

if __name__ == "__main__":
    entrada = "/Users/adrianvidal/Desktop/02-05-06_1649.jpg"
    salida_escalada = "/Users/adrianvidal/Desktop/foto_mejorada_2.jpg"

    print("🎬 Iniciando pipeline de mejora...\n")
    mejorar_con_EDSR(entrada, salida_escalada)
    mejorar_con_CodeFormer(salida_escalada)
    print("\n🏁 Proceso finalizado con éxito.")
