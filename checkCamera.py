import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        print("Kích thước khung hình:", frame.shape)
        print(f"Camera index {i} is available.")
        cap.release()