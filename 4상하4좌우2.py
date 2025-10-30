import time
import keyboard
import threading

toggle = False
macro_thread = None
buff_interval = 15  # 버프를 사용할 주기 (몇 사이클마다 버프를 쓸지)
cycle_count = 0

def move_ctrl(direction):
    """Ctrl + 방향키 이동"""
    keyboard.press("ctrl")
    keyboard.press(direction)
    time.sleep(0.15)
    keyboard.release(direction)
    keyboard.release("ctrl")

def attack_shift(times):
    """Shift 공격 지정 횟수만큼"""
    for _ in range(times):
        time.sleep(0.05)
        keyboard.press("shift")
        time.sleep(0.05)
        keyboard.release("shift")
        time.sleep(0.05)

def use_buff():
    """8번 키로 버프 한번 사용"""
    keyboard.press_and_release("8")
    print("[버프 사용됨]")
    time.sleep(0.5)

def loop_macro():
    global toggle, cycle_count
    while toggle:
        # 네모 모양 이동: 위(4번) → 오른쪽(2번) → 아래(4번) → 왼쪽(2번)
        
        # 위 이동
        for _ in range(4):
            if not toggle:
                return
            move_ctrl("up")
            attack_shift(2)
            time.sleep(0.2)

        # 오른쪽 이동 2번
        for _ in range(2):
            if not toggle:
                return
            move_ctrl("right")
            attack_shift(2)
            time.sleep(0.2)

        # 아래 이동
        for _ in range(4):
            if not toggle:
                return
            move_ctrl("down")
            attack_shift(2)
            time.sleep(0.2)

        # 왼쪽 이동 2번
        for _ in range(2):
            if not toggle:
                return
            move_ctrl("left")
            attack_shift(2)
            time.sleep(0.2)

        cycle_count += 1
        print(f"사이클 {cycle_count} 완료")

        # 일정 횟수마다 버프 사용
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
    # 모든 키 릴리즈
    for key in ["ctrl", "shift", "up", "down", "left", "right"]:
        keyboard.release(key)
    print("루프 완전 중단")

# 단축키 설정
keyboard.add_hotkey("f8", toggle_macro)  # 시작/정지
keyboard.add_hotkey("f10", stop_all)     # 완전 종료

print("매크로 대기중... (F8: 시작/정지, F10: 종료)")
keyboard.wait()
