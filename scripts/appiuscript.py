import uiautomator2 as u2
import time
d = u2.connect() 
w, h = d.window_size()
while True:
  x = int(input("x: "))
  y = int(input("y: "))
  # d(text="Settings").gesture((x, y), (1800, 980), (x, y), (1800, 980), steps=100)
  d.swipe(x, y, x,y, duration=1)