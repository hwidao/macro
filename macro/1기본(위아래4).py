import time
import keyboard
import threading

toggle = False
macro_thread = None

def move_ctrl(direction):
    if direction == "up":
        keyboard.press("ctrl")
        keyboard.press("up")
        time.sleep(0.15)
        keyboard.release("up")
        keyboard.release("ctrl")
    elif direction == "down":
        keyboard.press("ctrl")
        keyboard.press("down")
        time.sleep(0.3)
        keyboard.release("down")
        keyboard.release("ctrl")

def attack_shift(times):
    for _ in range(times):
        time.sleep(0.05)
        keyboard.press("shift")
        time.sleep(0.05)
        keyboard.release("shift")
        time.sleep(0.05)

def loop_macro():
    global toggle
    while toggle:
        for _ in range(4):
            if not toggle:  # 즉시 중단 체크
                return
            move_ctrl("up")
            attack_shift(2)
            time.sleep(0.2)
        for _ in range(4):
            if not toggle:
                return
            move_ctrl("down")
            attack_shift(2)
            time.sleep(0.2)

def toggle_macro():
    global toggle, macro_thread
    toggle = not toggle
    if toggle:
        print("매크로 작동")
        # 스레드에서 루프 실행
        macro_thread = threading.Thread(target=loop_macro)
        macro_thread.start()
    else:
        print("매크로 중지")
        stop_all()

def stop_all():
    global toggle
    toggle = False
    keyboard.release("ctrl")
    keyboard.release("shift")
    keyboard.release("up")
    keyboard.release("down")
    print("루프 중단")

keyboard.add_hotkey("f8", toggle_macro)
keyboard.add_hotkey("f10", stop_all)

print("매크로 대기중... (F8: 시작/정지, F10: 종료)")
keyboard.wait()
