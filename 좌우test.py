import time
import keyboard
import threading

toggle = False
macro_thread = None
buff_interval = 12  # 버프 주기 (사이클 단위)
cycle_count = 0
horizontal_moves = 2  # 좌우 이동 횟수 초기값
vertical_moves = 4    # 위아래 이동 횟수 초기값

# 각 키별 사용 주기 (초)
key_intervals = {
    "d": 11,
    "2": 125,
    "3": 140
}

# 마지막 사용 시각 기록
last_used = {key: 0 for key in key_intervals.keys()}


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


def use_skills_d23():
    """정지 상태에서 d,2,3 키를 주기적으로 사용"""
    global last_used
    now = time.time()

    for key, interval in key_intervals.items():
        if now - last_used[key] >= interval:
            time.sleep(0.3)
            keyboard.press_and_release(key)
            last_used[key] = now
            print(f"[{key.upper()} 사용됨 - 주기 {interval}s]")


def loop_macro():
    """메인 루프 매크로"""
    global toggle, cycle_count, horizontal_moves, vertical_moves
    while toggle:
        # 위 이동
        for _ in range(vertical_moves):
            if not toggle:
                return
            move_ctrl("up")
            attack_shift(2)
            time.sleep(0.2)

        # 오른쪽 이동
        for _ in range(horizontal_moves):
            if not toggle:
                return
            move_ctrl("right")
            attack_shift(2)
            time.sleep(0.2)

        # 아래 이동
        for _ in range(vertical_moves):
            if not toggle:
                return
            move_ctrl("down")
            attack_shift(2)
            time.sleep(0.2)

        # 왼쪽 이동
        for _ in range(horizontal_moves):
            if not toggle:
                return
            move_ctrl("left")
            attack_shift(2)
            time.sleep(0.2)

        # 1사이클 완료
        cycle_count += 1
        print(f"사이클 {cycle_count} 완료 (좌우 이동 {horizontal_moves}번 / 위아래 이동 {vertical_moves}번)")

        # 정지 상태에서 d,2,3 키 주기 확인 후 사용
        use_skills_d23()

        # 버프 주기 도달 시 버프 사용
        if cycle_count % buff_interval == 0:
            use_buff()


def toggle_macro():
    """F8로 매크로 시작/정지"""
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
    """매크로 완전 정지"""
    global toggle
    toggle = False
    for key in ["ctrl", "shift", "up", "down", "left", "right", "d", "2", "3", "8"]:
        keyboard.release(key)
    print("루프 완전 중단")


# 🔧 좌우 이동 횟수 조정
def increase_horizontal_moves():
    global horizontal_moves
    horizontal_moves += 1
    print(f"[좌우 이동 횟수 증가: {horizontal_moves}회]")


def decrease_horizontal_moves():
    global horizontal_moves
    if horizontal_moves > 1:
        horizontal_moves -= 1
        print(f"[좌우 이동 횟수 감소: {horizontal_moves}회]")
    else:
        print("[최소 1회 이상이어야 합니다]")


# 🔧 위아래 이동 설정
def disable_vertical_moves():
    global vertical_moves
    vertical_moves = 0
    print("[위아래 이동 비활성화됨 (0회)]")


def enable_vertical_moves():
    global vertical_moves
    vertical_moves = 4
    print("[위아래 이동 복원됨 (4회)]")


# 단축키 설정
keyboard.add_hotkey("f8", toggle_macro)             # 매크로 시작/정지
keyboard.add_hotkey("f10", stop_all)                # 완전 종료
keyboard.add_hotkey("f9", increase_horizontal_moves)  # 좌우 이동 +
keyboard.add_hotkey("f7", decrease_horizontal_moves)  # 좌우 이동 -
keyboard.add_hotkey("f6", disable_vertical_moves)     # 위아래 0회
keyboard.add_hotkey("f5", enable_vertical_moves)      # 위아래 복원

print("매크로 대기중... (F8: 시작/정지, F10: 종료, F9: 좌우+, F7: 좌우-, F6: 위아래 0, F5: 위아래 복원)")
keyboard.wait()
  