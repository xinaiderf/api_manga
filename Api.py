from fastapi import FastAPI, File, UploadFile, Query
import cv2
import numpy as np
import os
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/generate_video/")
async def generate_video(file: UploadFile = File(...), duration: int=Query(15,description="duração do video")):
    # Salva a imagem temporariamente
    image_path = f"temp_{file.filename}"
    with open(image_path, "wb") as img_file:
        img_file.write(file.file.read())

    # Carregar a imagem
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Definições do vídeo
    video_fps = 60
    video_duration = duration  # Tempo total do vídeo em segundos
    num_frames = video_fps * video_duration
    frame_height = 720  # Altura do vídeo de saída
    frame_width = width  # Mantém a mesma largura da imagem

    # Criar frames simulando o scroll
    frames = []
    for i in range(num_frames):
        y_offset = int((height - frame_height) * (i / (num_frames - 1)))
        cropped_frame = image[y_offset:y_offset+frame_height, :]
        frames.append(cropped_frame)

    # Criar o vídeo
    video_path = "output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, video_fps, (frame_width, frame_height))

    for frame in frames:
        out.write(frame)

    out.release()
    os.remove(image_path)  # Remover imagem temporária

    return FileResponse(video_path, media_type="video/mp4", filename="output.mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)