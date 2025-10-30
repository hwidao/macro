import cv2
import numpy as np
import pytesseract
import mss
import time

# 🔹 Tesseract 설치 경로 (Windows라면 아래 경로 확인 후 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 감지할 단어
TARGET_TEXT = "안녕"

# 🔹 화면 캡처 영역 (x, y, width, height)
monitor = {"top": 300, "left": 500, "width": 400, "height": 150}

def capture_and_detect():
    with mss.mss() as sct:
        while True:
            # 화면 캡처
            img = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 대비 향상 (조금 기울어진 글씨 보정에 도움)
            gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # 🔹 Tesseract OCR 수행
            text = pytesseract.image_to_string(gray, lang="eng")

            # 감지된 텍스트 출력 (디버그용)
            print(f"감지된 텍스트: {text.strip()}")

            # 🔹 특정 단어 감지
            if TARGET_TEXT.lower() in text.lower():
                print(f"[감지됨] 화면에서 '{TARGET_TEXT}' 텍스트 발견!")

            time.sleep(1)  # 1초마다 감시 (원하면 더 짧게 가능)

if __name__ == "__main__":
    print("화면 감시 시작...")
    capture_and_detect()
