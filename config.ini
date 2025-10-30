import pyautogui
import cv2
import numpy as np

target_image = r"C:\Users\Administrator\macro\T1.jpg"

print("화면에서 이미지 탐색 중...")

try:
    location = pyautogui.locateOnScreen(target_image, confidence=0.6)
    if location:
        print("이미지 발견:", location)
    else:
        print("이미지를 찾지 못했습니다.")
except pyautogui.ImageNotFoundException as e:
    print("화면에서 이미지를 찾지 못함:", e)
