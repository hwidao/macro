import time
import keyboard
import threading
import random  # 랜덤 딜레이용

toggle = False
macro_thread = None
cycle_count = 0
horizontal_moves = 2

# 자동 키 설정
auto_keys = {
    "d": {"interval": 5, "count": 1},   # 10초 → 5초 (자연스럽게 더 자주)
    "2": {"interval": 125, "count": 3},
    "3": {"interval": 150, "count": 3}
}

def move_ctrl(direction):
    """Ctrl + 방향키 이동"""
    keyboard.press("ctrl")
    keyboard.press(direction)
    time.sleep(0.05)
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
    """8번 키로 버프 사용"""
    time.sleep(0.5)
    keyboard.press("8")
    time.sleep(0.2)
    keyboard.release("8")
    print("[버프 사용됨]")
    time.sleep(0.5)

def key_loop(key, interval, count):
    """각 키 전용 스레드 루프"""
    global toggle
    while toggle:
        # "d"만 랜덤하게 눌리게 설정 (±30% 오차)
        if key == "d":
            random_delay = interval * random.uniform(0.7, 1.3)
            time.sleep(random_delay)
        else:
            time.sleep(interval)

        for _ in range(count):
            if not toggle:
                return
            time.sleep(0.3)
            keyboard.press_and_release(key)
            print(f"[{key.upper()} 자동 사용됨]")
            time.sleep(0.2)

def loop_macro():
    """메인 이동/공격 루프"""
    global toggle, cycle_count, horizontal_moves
    while toggle:
        # 위 이동 4번
        for _ in range(4):
            if not toggle: return
            move_ctrl("up")
            attack_shift(2)
            time.sleep(0.2)

        # 오른쪽 이동
        for _ in range(horizontal_moves):
            if not toggle: return
            move_ctrl("right")
            attack_shift(2)
            time.sleep(0.2)

        # 아래 이동 4번
        for _ in range(4):
            if not toggle: return
            move_ctrl("down")
            attack_shift(2)
            time.sleep(0.2)

        # 왼쪽 이동
        for _ in range(horizontal_moves):
            if not toggle: return
            move_ctrl("left")
            attack_shift(2)
            time.sleep(0.2)

        cycle_count += 1
        print(f"사이클 {cycle_count} 완료 (좌우 이동 {horizontal_moves}번)")

        # 버프 사용 (10사이클마다)
        if cycle_count % 10 == 0:
            use_buff()

        # 좌우 이동 횟수 토글
        horizontal_moves = 1 if horizontal_moves == 2 else 2

def toggle_macro():
    """매크로 시작/정지"""
    global toggle, macro_thread
    toggle = not toggle
    if toggle:
        print("매크로 작동 시작")
        # 메인 루프
        macro_thread = threading.Thread(target=loop_macro)
        macro_thread.start()
        # 자동 키 루프
        for key, info in auto_keys.items():
            threading.Thread(target=key_loop, args=(key, info["interval"], info["count"]), daemon=True).start()
    else:
        print("매크로 중지")
        stop_all()

def stop_all():
    """모든 키 릴리즈 및 루프 완전 중단"""
    global toggle
    toggle = False
    for key in ["ctrl","shift","up","down","left","right","d","2","3","8"]:
        keyboard.release(key)
    print("루프 완전 중단")

# 단축키 설정
keyboard.add_hotkey("f8", toggle_macro)  # F8: 매크로 시작/정지
keyboard.add_hotkey("f10", stop_all)     # F10: 완전 종료

print("매크로 대기중... (F8: 시작/정지, F10: 종료)")
keyboard.wait()
