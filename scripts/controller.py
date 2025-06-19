import uiautomator2 as u2
import random

BUTTONS ={
    'move_up': [480, 550],
    'move_up_left': [430, 550],
    'move_up_right': [530, 550],

    'move_down': [480, 960],
    'move_down_left': [420, 960],
    'move_down_right': [530, 960],

    'move_left': [300, 730],
    'move_left_up': [300, 630],
    'move_left_down': [300, 830],

    'move_right': [660, 730],
    'move_right_up': [700, 630],
    'move_right_down': [700, 830],

    'skill': [1800, 500],

    'shoot': [2000, 980],
    'pass_up': [2000, 880],
    'pass': [1800, 980],

    "joystick_center": [480,500],

    'pressing': [1800, 900],
    "keeper_rush": [2000, 750]
}

d = u2.connect()
w, h = d.window_size()

def tap(x, y):
    d.click(float(x), float(y))  # hoặc int(x), int(y) nếu bạn chỉ dùng tọa độ nguyên

def hold(x, y, time=0.5):
    d.long_click(float(x), float(y), float(time))  # duration in milliseconds

def swipe(x1, y1, x2, y2, time=0.5):
    d.swipe(float(x1), float(y1), float(x2), float(y2), float(time))

def play_action(x1, y1, x2, y2, steps=10):
    d(text="Settings").gesture(
        (float(x1), float(y1)),
        (float(x2), float(y2)),
        (float(x1), float(y1)),
        (float(x2), float(y2)),
        steps=steps
    )

def move_joystick(d, start, end, duration=0.2):
    d.swipe(start[0], start[1], end[0], end[1], duration=duration)


def send_action_career(action, x=None, y=None):
    if action == "career":
        tap(x, y)
    elif action == "play_now":
        tap(x, y)
    elif action == "play":
        tap(x, y)
    elif action == "resume":
        tap(x, y)
    elif action == "disconect_touch":
        tap(x, y)
    elif action == "continue_green_btn":
        tap(x, y)
    elif action == "continu":
        tap(x, y)
    elif action == "ok":
        tap(x, y)
    elif action == "close":
        tap(x, y)
    elif action == "retry":
        tap(x, y)
    elif action == "start_new_devision":
        tap(x, y)
    elif action == "none":
        print("[ℹ️] Không có hành động nào được xác định.")

        

def send_action_live(action, x=None, y=None):
    if action == "live1":
        tap(x, y)
    elif action == "live2":
        tap(x, y)
    elif action == "resume":
        tap(x, y)
    elif action == "continu":
        tap(x, y)
    elif action == "disconect_touch":
        tap(x, y)
    elif action == "continue_green_btn":
        tap(x, y)
    elif action == "ok":
        tap(x, y)
    elif action == "close":
        tap(x, y)
    elif action == "start_new_live":
        tap(x, y)
    elif action == "none":
        print("[ℹ️] Không có hành động nào được xác định.")


def send_action_ingame(action, x=None, y=None):  
    if( action == "pass"):
        play_action(x, y, BUTTONS['pass'][0], BUTTONS['pass'][1], 30)

    
    if( action == "pass_small"):
        play_action(x, y, BUTTONS['pass'][0], BUTTONS['pass'][1], 15)
        play_action(BUTTONS["move_up"][0], BUTTONS["move_up"][1], BUTTONS['skill'][0], BUTTONS['skill'][1], 20)


    if( action == "shoot"):
        k = random.randint(0, 1)
        if k == 0:
            play_action(BUTTONS["move_up"][0]+15, BUTTONS["move_up"][1], BUTTONS['shoot'][0], BUTTONS['shoot'][1], 8)
        else:
            play_action(BUTTONS["move_up"][0]-15, BUTTONS["move_up"][1], BUTTONS['shoot'][0], BUTTONS['shoot'][1], 8)

    if( action == "pass_up"):
        play_action(x, y, BUTTONS['pass_up'][0], BUTTONS['pass_up'][1], 25)
    
    if( action == "shoot_up"):
        hold(BUTTONS['shoot'][0], BUTTONS['shoot'][1], 0.42)
        play_action(BUTTONS["move_up"][0], BUTTONS["move_up"][1], BUTTONS['shoot'][0], BUTTONS['shoot'][1], 50)

    if (action == "r_live"):
        tap(BUTTONS["skill"][0], BUTTONS["skill"][1])
    
    if (action == "replay"):
        tap(BUTTONS["skill"][0], BUTTONS["skill"][1])

    if (action == "search_ball"):
        move_joystick(d, BUTTONS["joystick_center"], (x, y))
    
    if (action == "run_to_ball"):
        hold(x, y, 1)


    if (action == "switch_player"):
        tap(x, y)
    
    if (action == "skill"):
        hold(BUTTONS['move_up'][0], BUTTONS['move_up'][1], 1)
        tap(BUTTONS['skill'][0], BUTTONS['skill'][1])
        tap(BUTTONS['skill'][0], BUTTONS['skill'][1])
    
    if (action == "move_ball"):
        hold(x, y)
    
    if (action == "pressing"):
        play_action(x, y, BUTTONS['pressing'][0], BUTTONS['pressing'][1], 150)
    
    if (action == "default_move"):
        print("[ℹ️] Default move action")
        k = random.randint(0, 10)

        if (k > 1 ):
            play_action(BUTTONS["move_up"][0], BUTTONS["move_up"][1], BUTTONS['skill'][0], BUTTONS['skill'][1], 15)
            hold(BUTTONS['move_up'][0], BUTTONS['move_up'][1], 3)
        elif (k == 6):
            play_action(BUTTONS["move_up_left"][0]-20, BUTTONS["move_up_left"][1], BUTTONS['skill'][0], BUTTONS['skill'][1], 15)
            hold(BUTTONS['move_up_left'][0], BUTTONS['move_up_left'][1], 3)
        elif (k == 8):
            play_action(BUTTONS["move_up_right"][0]+20, BUTTONS["move_up_right"][1], BUTTONS['skill'][0], BUTTONS['skill'][1], 15)
            hold(BUTTONS['move_up_right'][0], BUTTONS['move_up_right'][1], 3)
        elif (k == 5 or k == 7 or k == 9):
            play_action(BUTTONS['move_up_left'][0], BUTTONS['move_up_left'][1], BUTTONS['pass'][0], BUTTONS['pass'][1], 15)
            hold(BUTTONS['move_up_right'][0], BUTTONS['move_up_right'][1], 1)
            hold(BUTTONS['move_up_left'][0], BUTTONS['move_up_left'][1], 1)

        else:
            play_action(BUTTONS["move_up"][0], BUTTONS["move_up"][1], BUTTONS['skill'][0], BUTTONS['skill'][1], 15)
            hold(BUTTONS['move_up'][0], BUTTONS['move_up'][1], 3)



    if (action == "move_slow"):
         hold(BUTTONS['move_up'][0], BUTTONS['move_up'][1], 1)
    
    if (action == "keeper_rush"):
        k =random.randint(0, 1)
        if k == 0:
            play_action(BUTTONS["move_up_left"][0]-50, BUTTONS["move_up_left"][1], BUTTONS['keeper_rush'][0], BUTTONS['keeper_rush'][1], 100)
        else:
            play_action(BUTTONS["move_up_right"][0]+20, BUTTONS["move_up_right"][1], BUTTONS['keeper_rush'][0], BUTTONS['keeper_rush'][1], 100)




    