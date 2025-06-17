import cv2
import os

def extract_frames(video_path, output_dir, skip_frames=5):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    i = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if i % skip_frames == 0:
            filename = os.path.join(output_dir, f"frame_{saved:04d}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1

        i += 1
    cap.release()

extract_frames("video/gameplay1.mp4", "images/gameplay1/")
extract_frames("video/gameplay2.mp4", "images/gameplay2/")
