import uiautomator2 as u2
import cv2

device="emulator-5554" # Replace with your device ID if needed
d = u2.connect()

def screenshot():
    d.screenshot("screen.png")
    img = cv2.imread("screen.png")
    return img

screenshot()