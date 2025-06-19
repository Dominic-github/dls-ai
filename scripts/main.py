import time
import cv2
import threading
import queue
from screenshot import screenshot
from ultralytics import YOLO
from logic import decide_action_career, decide_action_live, decide_action_ingame
from controller import send_action_career, send_action_live, send_action_ingame

# Load mô hình
model = YOLO('models/best.pt') 
model_ingame = YOLO('models/best_ingame.pt')  

# Cấu hình webcam ảo
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2400)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Hàng đợi chia sẻ hành động giữa luồng detect và luồng send
action_queue = queue.LifoQueue(maxsize=0)
stop_event = threading.Event()

# Biến mode được thiết lập ở main_loop
current_mode = None
continue_hold = False

def clear_action_queue():
    try:
        while True:
            action_queue.get_nowait()
    except queue.Empty:
        pass

def detect_thread():
    while not stop_event.is_set():
        mode = current_mode
        # ret, frame = cap.read()
        global continue_hold

        frame = screenshot()  # Sử dụng hàm screenshot để lấy ảnh từ webcam ảo

        if continue_hold:
            time.sleep(4)
            continue_hold = False
            frame = screenshot()  # Sử dụng hàm screenshot để lấy ảnh từ webcam ảo


        # if not ret:
        #     continue

        try:
            if mode == '1':  # Career
                results = model(frame, conf=0.4)[0]
                actions = decide_action_career(results)
                visualize_debug(results, frame, "debug_interface.jpg")

                if not actions:
                    results_ingame = model_ingame(frame, conf=0.5)[0]
                    actions = decide_action_ingame(results_ingame)
                    visualize_debug(results_ingame, frame, "debug_ingame.jpg")

                    if not actions:
                        print("[ℹ️] Không có hành động nào được xác định.")
                        continue

                    # Fallback sang ingame
                    for action in actions:
                        action_queue.put(("0", action))  # dùng mode "0"
                    continue
                else:
                    for action in actions:
                        action_queue.put(("1", action))

            elif mode == '2':  # Live
                frame = cv2.resize(frame, (2400, 1080))
                results = model(frame, conf=0.4)[0]
                actions = decide_action_live(results)
                # visualize_debug(results, frame, "debug_live.jpg")

                if not actions:
                    results_ingame = model_ingame(frame, conf=0.5)[0]
                    actions = decide_action_ingame(results_ingame)
                    # visualize_debug(results_ingame, frame, "debug_ingame.jpg")

                    if not actions:
                        print("[ℹ️] Không có hành động nào được xác định.")
                        continue

                    for action in actions:
                        action_queue.put(("0", action))
                    continue
                else:
                    for action in actions:
                        action_queue.put(("2", action))

        except Exception as e:
            print(f"[❌] Detect lỗi: {e}")

# Thread 2: xử lý gửi hành động
def action_thread():
    global continue_hold

    while not stop_event.is_set():
        try:
            print("[🚀] Đang chờ hành động từ hàng đợi...", action_queue.get())
            mode, (action, x, y) = action_queue.get()
            

            print(f"[🚀] Gửi action: {action} với tọa độ ({x}, {y})")
            if mode == '1':
                send_action_career(action, x, y)
                if(action == "continu"):
                    continue_hold = True
                    clear_action_queue()
                    time.sleep(3)
                    continue
                time.sleep(2)
            elif mode == '2':
                print(f"[🎮] Hành động: {action} tại tọa độ ({x}, {y})")
                send_action_live(action, x, y)
                if(action == "continu"):
                    continue_hold = True
                    clear_action_queue()
                    time.sleep(4)
                    continue
                time.sleep(2)
            else:
                send_action_ingame(action, x, y)
                clear_action_queue()
            

        except queue.Empty:
            continue
        except Exception as e:
            print(f"[❌] Gửi action lỗi: {e}")

# Vẽ khung và lưu ảnh debug

def visualize_debug(results, frame, file):
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = results.names[cls_id] if hasattr(results, 'names') else str(cls_id)

        xyxy = box.xyxy[0]
        if hasattr(xyxy, 'cpu'):
            xyxy = xyxy.cpu().numpy()
        x1, y1, x2, y2 = map(int, xyxy)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    cv2.imwrite(file, frame)


# Chọn chế độ chơi

def choose_mode():
    print("[🚀] Bắt đầu AI đá game DLS...")
    while not stop_event.is_set():
        print("\nChọn chế độ đá:")
        print("1. Chơi Career")
        print("2. Chơi Live")
        print("Ctrl + c. Thoát")

        mode = input("Nhập số tương ứng với chế độ bạn chọn (1/2) hoặc 'Ctrl + c' để thoát: ").strip()
        if mode in ['1', '2']:
            print(f"[ℹ️] Chế độ đã chọn: {'Career' if mode == '1' else 'Live'}")
            return mode
        elif mode.lower() == 'q':
            print("[👋] Đã thoát khỏi chương trình.")
            exit()
        else:
            print("[❌] Chế độ không hợp lệ. Vui lòng nhập lại.")

# Hàm chính khởi động luồng

def main_loop():
    global current_mode
    global continue_hold
    current_mode = choose_mode()

    t1 = threading.Thread(target=detect_thread)
    t2 = threading.Thread(target=action_thread)

    t1.start()
    t2.start()

    try:
        while not stop_event.is_set():
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n[🛑] Dừng chương trình...")
        stop_event.set()
    finally:
        print("[⏳] Đang dừng các tiến trình...")
        t1.join()
        t2.join()
        # cap.release()
        cv2.destroyAllWindows()
        print("[✅] Đã dừng sạch sẽ.")

if __name__ == "__main__":
    main_loop()