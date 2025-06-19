import numpy as np
import uiautomator2 as u2
import random
import math

d = u2.connect()
w, h = d.window_size()

CLASS_ID = {
    "career_btn": 0,
    "close_btn": 1,
    "continu_btn": 2,
    "continue_green_btn": 3,
    "disconect_touch": 4,
    "live1_btn": 5,
    "live2_btn": 6,
    "ok_btn": 7,
    "play_btn": 8,
    "playnow_btn": 9,
    "resume_btn": 10,
    "retry_btn": 11,
    "start_new_devision": 12,
    "start_new_live": 13,

}


INGAME_ID = {
    "ball": 0,
    "goal": 1,
    "goal_left": 2,
    "goal_right": 3,
    "my_goal": 4,
    "my_goalkeper": 5,
    "my_player": 6,
    "opponent_player": 7,
    "player_now": 8,
    "r_live": 9,
    "replay_btn": 10,
    "switch_player": 11
}


BUTTONS = {
    "tap_skill": [1800, 400],
    "joystick_center": [480,730],
}


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def joystick_target(center_joy, angle_deg, strength=1.0, radius=150, extend=50):
    angle_rad = math.radians(angle_deg)
    total_radius = radius * strength + extend
    x = center_joy[0] + total_radius * math.cos(angle_rad)
    y = center_joy[1] + total_radius * math.sin(angle_rad)
    return (x, y)

def calculate_angle(center, point):
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360  # Đảm bảo kết quả trong [0, 360)

def center_of(box):
    x1, y1, x2, y2 = box.xyxy[0]
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return np.array([cx, cy])

def decide_action_career(detections):


    actions = []

    for box in detections.boxes:
        cls_id = int(box.cls[0])
        x, y = center_of(box)

        if cls_id == CLASS_ID["career_btn"]:
            actions.append(("career", x, y))
        elif cls_id == CLASS_ID["close_btn"]:
            actions.append(("close", x, y))
        elif cls_id == CLASS_ID["continu_btn"]:
            actions.append(("continu", x, y))
        elif cls_id == CLASS_ID["continue_green_btn"]:
            actions.append(("continue_green", x, y))
        elif cls_id == CLASS_ID["disconect_touch"]:
            actions.append(("disconect_touch", x, y))
        elif cls_id == CLASS_ID["playnow_btn"]:
            actions.append(("play_now", x, y))
        elif cls_id == CLASS_ID["play_btn"]:
            actions.append(("play", x, y))
        elif cls_id == CLASS_ID["resume_btn"]:
            actions.append(("resume", x, y))
        elif cls_id == CLASS_ID["ok_btn"]:
            actions.append(("ok", x, y))
        elif cls_id == CLASS_ID["retry_btn"]:
            actions.append(("retry", x, y))
        elif cls_id == CLASS_ID["start_new_devision"]:
            actions.append(("start_new_devision", x, y))
        
    return actions

def decide_action_live(detections):

    actions = []

    for box in detections.boxes:
        cls_id = int(box.cls[0])
        x, y = center_of(box)

        if cls_id == CLASS_ID["live1_btn"]:
            actions.append(("live1", x, y))
        elif cls_id == CLASS_ID["live2_btn"]:
            actions.append(("live2", x, y))
        elif cls_id == CLASS_ID["resume_btn"]:
            actions.append(("resume", x, y))
        elif cls_id == CLASS_ID["disconect_touch"]:
            actions.append(("disconect_touch", x, y))
        elif cls_id == CLASS_ID["continu_btn"]:
            actions.append(("continu", x, y))
        elif cls_id == CLASS_ID["continue_green_btn"]:
            actions.append(("continue_green", x, y))
        elif cls_id == CLASS_ID["close_btn"]:
            actions.append(("close", x, y))
        elif cls_id == CLASS_ID["ok_btn"]:
            actions.append(("ok", x, y))
        elif cls_id == CLASS_ID["start_new_live"]:
            actions.append(("start_new_live", x, y))


    return actions

def decide_action_ingame(detections):
    actions = []
    my_players= []
    player_now = []
    goal = []
    opponent_goalkeeper = []
    opponent_players = []
    my_goal = []
    ball = []

    center = np.array([w // 2, h // 2]) 
    center_screen = np.array([w // 2, h // 2])
    for box in detections.boxes:
        cls_id = int(box.cls[0])

        if(cls_id == INGAME_ID['r_live']):
            x, y = center_of(box)
            actions.append(("r_live", x, y))
            return actions

        if(cls_id == INGAME_ID['replay_btn']):
            x, y = center_of(box)
            actions.append(("replay", x, y))
            return actions

        if(cls_id == INGAME_ID['switch_player']):
            x, y = center_of(box)
            actions.append(("switch_player", x, y))
            return actions
        
        if(cls_id == INGAME_ID['goal_left']) or (cls_id == INGAME_ID['goal_right']):
            actions.append(("shoot_up", 0, 0))
            return actions

        if(cls_id == INGAME_ID['my_player']):
            player_pos = center_of(box)
            my_players.append(player_pos)
        elif(cls_id == INGAME_ID['player_now']):
            player_now.append(center_of(box))
        elif(cls_id == INGAME_ID['my_goal']):
            my_goal.append(center_of(box))
        elif(cls_id == INGAME_ID['ball']):
            ball.append(center_of(box))
        elif(cls_id == INGAME_ID['goal']):
            goal.append(center_of(box))
        elif(cls_id == INGAME_ID['opponent_player']):
            opponent_players.append(center_of(box))
        elif(cls_id == INGAME_ID['ball']):
            ball.append(center_of(box))

    if player_now:
         center = player_now[0]
    
    if my_goal:
        my_goal_pos = my_goal[0]
        dist = np.linalg.norm(center_screen - my_goal_pos)
        if dist < 400:
            angle = calculate_angle(my_goal_pos, center_screen)
            target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
            actions.append(("keeper_rush", target[0], target[1]))
            return actions

    # Nếu không có đồng đội gần nhưng có đối thủ gần -> chuyền cho đồng đội tốt nhất
    # if opponent_players:
    # opponent_near = [op for op in opponent_players if np.linalg.norm(center - op) < 100]

    # print(f"[ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️] Số lượng đối thủ gần: {len(opponent_near)}")
    # if opponent_near and  my_players:
    #     # Tìm đồng đội ở phía trước (hoặc mọi người nếu không lọc)
    #     candidates = [p for p in my_players if p[1] < center[1]]
    #     if not candidates:
    #         candidates = my_players  # fallback nếu không ai ở phía trước

    #     best_pass = min(candidates, key=lambda p: np.linalg.norm(p - center))
    #     angle = calculate_angle(center, best_pass)
    #     target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=30)
    #     actions.append(("pass", target[0], target[1]))
    #     return actions
    
 # Nếu có bóng nhưng đang ở xa thì chạy về hướng bóng
    if ball:
        ball_pos = ball[0]
        distance_to_ball = np.linalg.norm(center - ball_pos)
        if distance_to_ball >= 400:
            angle = calculate_angle(center, ball_pos)
            target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
            actions.append(("run_to_ball", target[0], target[1]))
            return actions

    # Nếu có opponent gần bóng hơn player_now thì pressing
    if  ball and opponent_players:
        ball_pos = ball[0]
        player_now_dist = np.linalg.norm(center - ball_pos)

        for opponent in opponent_players:
            opponent_dist = np.linalg.norm(opponent - ball_pos)
            if opponent_dist < player_now_dist:
                angle = calculate_angle(center, opponent)
                target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
                actions.append(("pressing", target[0], target[1]))
                return actions
    

   

    # Nếu gần khung thành thì sút
    if goal:
        dist_to_goal = np.linalg.norm(center_screen - goal[0])
        print(f"[ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️] Distance to goal: {dist_to_goal}")
        if dist_to_goal < 340:
            angle = calculate_angle(center_screen, goal[0])
            target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
            actions.append(("shoot", target[0], target[1]))
            return actions
        else:
            if dist_to_goal < 420:
                angle = calculate_angle(center_screen, goal[0])
                target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
                actions.append(("move_slow", target[0], target[1]))
                return actions
            else:
                actions.append(("default_move", BUTTONS['joystick_center'][0], BUTTONS['joystick_center'][1]))
                return actions


    # Nếu bóng ở dưới player_now thì pressing
    if ball and player_now and opponent_players:
        ball_pos = ball[0]
        player_pos = player_now[0]
        if ball_pos[1] > player_pos[1]:
            angle = calculate_angle(player_pos, ball_pos)
            target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
            actions.append(("pressing", target[0], target[1]))
            return actions

    # Nếu bóng ở phía trên player_now và gần opponent hơn thì pressing
    if ball and player_now and opponent_players:
        ball_pos = ball[0]
        player_pos = player_now[0]

        # Bóng ở trên cầu thủ
        if ball_pos[1] < player_pos[1]:
            opponent_nearest = min(opponent_players, key=lambda o: np.linalg.norm(ball_pos - o))
            dist_opp = np.linalg.norm(ball_pos - opponent_nearest)
            dist_me = np.linalg.norm(ball_pos - center)

            if dist_opp < dist_me:
                angle = calculate_angle(center, ball_pos)
                target = joystick_target(BUTTONS['joystick_center'], angle, strength=1.0, radius=150, extend=40)
                actions.append(("pressing", target[0], target[1]))
                return actions

    if my_players or player_now:
        actions.append(("default_move", BUTTONS['joystick_center'][0], BUTTONS['joystick_center'][1]))
        return actions

