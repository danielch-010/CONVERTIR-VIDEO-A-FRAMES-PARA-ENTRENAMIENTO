import cv2
import os
import sys
from tkinter import Tk, filedialog
from pathlib import Path

def extraer_frames(video_path, output_dir, skip_frames=30):
    """
    Extrae frames de un video cada 'skip_frames' cuadros y los guarda
    en una subcarpeta con el nombre del video dentro de 'output_dir'.
    """
    video_name = Path(video_path).stem
    output_folder = os.path.join(output_dir, video_name)
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ No se pudo abrir el video: {video_path}")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps else 0

    print(f"\n🎥 Video seleccionado: {video_name}")
    print(f"➡ Total de frames: {total_frames}")
    print(f"➡ FPS: {fps:.2f}")
    print(f"➡ Duración: {duration:.2f} segundos")
    print(f"➡ Saltando cada {skip_frames} frames (≈ {skip_frames/fps:.2f} segundos entre imágenes)\n")

    count, saved = 0, 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % skip_frames == 0:
            filename = os.path.join(output_folder, f"frame_{saved:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
        count += 1

    cap.release()
    print(f"✅ {saved} frames extraídos y guardados en: {output_folder}\n")
    return output_folder


def seleccionar_video():
    """Abre el explorador para seleccionar un video."""
    Tk().withdraw()
    video_path = filedialog.askopenfilename(
        title="Selecciona un video",
        filetypes=[
            ("Archivos de video", "*.mp4 *.avi *.mov *.wmv *.mkv *.flv *.mpeg *.mpg"),
            ("Todos los archivos", "*.*")
        ]
    )
    return video_path


def seleccionar_carpeta_destino():
    """Abre el explorador para seleccionar dónde guardar los frames."""
    Tk().withdraw()
    folder_path = filedialog.askdirectory(
        title="Selecciona la carpeta donde se guardarán los frames"
    )
    return folder_path


def main():
    print("🎬 Selecciona el video del cual deseas extraer frames...")
    video_path = seleccionar_video()

    if not video_path:
        print("⚠ No seleccionaste ningún video. Saliendo...")
        return

    print("\n📁 Ahora selecciona la carpeta donde quieres guardar los frames...")
    output_dir = seleccionar_carpeta_destino()

    if not output_dir:
        print("⚠ No seleccionaste carpeta de destino. Saliendo...")
        return

    # Puedes ajustar la cantidad de frames que se saltan (30 ≈ 1 frame por segundo en 30 FPS)
    skip_frames = 30

    carpeta_resultado = extraer_frames(video_path, output_dir, skip_frames=skip_frames)

    # Si se generaron frames, abrir la carpeta automáticamente (solo Windows)
    if carpeta_resultado and sys.platform.startswith("win"):
        os.startfile(carpeta_resultado)
    elif carpeta_resultado:
        print(f"📂 Abre manualmente la carpeta: {carpeta_resultado}")


if __name__ == "__main__":
    main()
