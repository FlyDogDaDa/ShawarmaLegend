import pygetwindow as gw
import pyautogui
import time
from PIL import Image
import cv2
import numpy as np


def capture_window_content(window: gw.Window) -> Image:

    screenshot = pyautogui.screenshot(
        region=(window.left, window.top, window.width, window.height)
    )
    return screenshot  # 回傳Pillow圖片


def find_window(window_title) -> gw.Window:
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        return window
    except IndexError:
        raise ValueError(f"找不到指定的視窗，請檢查視窗標題：{window_title}")


class CheckPoint:
    def __init__(self, x: float, y: float, threshold: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.threshold = threshold


def debug_plot_check_point(screenshot: Image, check_point: CheckPoint):
    x = int(screenshot.width * check_point.x)
    y = int(screenshot.height * check_point.y)
    array = np.array(screenshot)
    array = cv2.circle(
        array,
        (x, y),
        radius=1,
        color=(0, 255, 0),  # RGB
        thickness=-1,
    )
    screenshot = Image.fromarray(array)
    screenshot.show()  # 顯示圖片，標示出檢測點的位置
    cv2.waitKey(0)  # 按下任意按鍵繼續


def check_point(screenshot: Image, check_point: CheckPoint) -> bool:
    x = int(screenshot.width * check_point.x)
    y = int(screenshot.height * check_point.y)
    pixel = screenshot.getpixel((x, y))
    c = map(lambda a, b: a >= b, pixel, check_point.threshold)
    return all(c)


if __name__ == "__main__":
    # 這是一個很粗糙的程式，我很抱歉。
    # 如果你想改進這個程式，歡迎提交到Github。
    # 有空看到的話，我會將你的程式碼加到這個程式中。
    # 謝謝你。

    window_title = "【沙威瑪傳奇／初見歡迎】沒錯一大清早就來吃沙威瑪吧🌯雖然說實在薄巧好像沒有吃過🤔【薄荷巧克力🌱🍫】"
    check_points = [
        CheckPoint(0.6014, 0.798, (150, 0, 0)),
        CheckPoint(0.6095, 0.798, (150, 0, 0)),
        CheckPoint(0.6170, 0.798, (150, 0, 0)),
    ]

    window = find_window(window_title)

    ## 偵測點對準
    # screenshot = capture_window_content(window)
    # for point in check_points:
    #     debug_plot_check_point(screenshot, point)

    window.activate()
    print("開始偵測")
    Shawarma_count = 0  # 沙威瑪數量
    states = [tuple(False for _ in check_points)] * 10
    while True:
        try:
            screenshot = capture_window_content(window)
            state = tuple(check_point(screenshot, point) for point in check_points)
            states.append(state)
            t = list(zip(*states[-10:]))  # 轉置
            for lit in t:
                count = all((*lit[0:-1], not lit[-1]))  # 前面全部是True，最後是False
                if count:  # 沙威瑪起鍋
                    Shawarma_count += 1
                    print(f"沙威瑪數量：{Shawarma_count}")
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
    print("結束偵測")
    print(f"沙威瑪數量：{Shawarma_count}")

# TODO:更方便的檢測點對準方法(或是自動化對準)
# TODO:自動化遊戲開始偵測
# TODO:自動化結束偵測


quit()
"""
None:
66 14 14
83 15 22
84 22 36

On1True:
161 12 14
113 15 15
88 23 34

On2True:
94 11 16
176 3 23
107 17 18

On3True:
71 16 29
97 16 26
161 8 23
"""
