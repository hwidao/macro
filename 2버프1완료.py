import time
import keyboard
import threading

toggle = False
macro_thread = None
buff_interval = 5  # 버프를 사용할 주기 (몇 사이클마다 버프를 쓸지)
cycle_count = 0

def move_ctrl(direction):
    if direction == "up":
        keyboard.press("ctrl")
        keyboard.press("up")
        time.sleep(0.15)
        keyboard.release("up")
        keyboard.release("ctrl")
    elif direction == "down":
        time.sleep(0.05)
        keyboard.press("ctrl")
        keyboard.press("down")
        time.sleep(0.15)
        keyboard.release("down")
        keyboard.release("ctrl")
        time.sleep(0.05)

def attack_shift(times):
    for _ in range(times):
        time.sleep(0.05)
        keyboard.press("shift")
        time.sleep(0.05)
        keyboard.release("shift")
        time.sleep(0.05)

def use_buff():
    """8번 키로 버프 한번만 사용"""
    keyboard.press_and_release("8")
    print("[버프 사용됨]")
    time.sleep(0.5)

def loop_macro():
    global toggle, cycle_count
    while toggle:
        # 위로 이동 루프
        for _ in range(4):
            if not toggle:
                return
            move_ctrl("up")
            attack_shift(2)
            time.sleep(0.2)

        # 아래로 이동 루프
        for _ in range(4):
            if not toggle:
                return
            move_ctrl("down")
            attack_shift(2)
            time.sleep(0.2)

        cycle_count += 1
        print(f"사이클 {cycle_count} 완료")

        # === 일정 횟수마다 버프 한 번 사용 ===
        if cycle_count % buff_interval == 0:
            use_buff()

def toggle_macro():
    global toggle, macro_thread
    toggle = not toggle
    if toggle:
        print("매크로 작동 시작")
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
    print("루프 완전 중단")

keyboard.add_hotkey("f8", toggle_macro)
keyboard.add_hotkey("f10", stop_all)

print("매크로 대기중... (F8: 시작/정지, F10: 종료)")
keyboard.wait()
