import cv2 as cv
import pyautogui
import pandas as pd
from time import sleep
from datetime import datetime


def match(a, b, threshold=0.7):
    try:
        a_grey = cv.cvtColor(a.copy(), cv.COLOR_BGR2GRAY)
        b_grey = cv.cvtColor(b.copy(), cv.COLOR_BGR2GRAY)
    except:
        print(a)
    result = cv.matchTemplate(a_grey, b_grey, cv.TM_CCOEFF_NORMED)
    _ , max_val, _ , max_loc = cv.minMaxLoc(result)

    return (max_val >= threshold, max_loc)

def set_date(screen, day, month):

    template = cv.imread(f"Figures\\{day}.png")
    mon = cv.imread(f"Months\\{month}.png")

    # get to the target month
    found, _ = match(screen, mon)
    while not found:
        pyautogui.press("down")
        pyautogui.screenshot('screen.png')
        screen = cv.imread("screen.png")
        found, _ = match(screen, mon)

    found, max_loc = match(screen, template)

    # move the mouse to the center of the target and click
    if found:
        top_left = max_loc
        h, w = template.shape[:2]
        center = (top_left[0] + w//2, top_left[1] + h//2)
        pyautogui.moveTo(center[0], center[1])
        pyautogui.click()

def set_time(hour, minute):
    pyautogui.press("backspace", presses=2)
    pyautogui.press("left")
    pyautogui.press("backspace", presses=2)
    pyautogui.typewrite(f"{hour}")
    pyautogui.press("right")
    pyautogui.typewrite(f"{minute}")
    pyautogui.press("enter")






df = pd.read_excel('messages.xlsx', header=None, names=['Sentence', 'Date', 'Time'])
sleep(1)
for index, row in df.iterrows():
    date = df['Date'][index]
    day = date.day
    month = date.month
    year = date.year
    time = df['Time'][index]
    hour = time.hour
    minute = time.minute
    sentence = row['Sentence']
    found = False
    while not found:
        pyautogui.screenshot("screen.png")
        screen = cv.imread("screen.png")
        waiting = cv.imread("States\\scheduling.png")
        found, _ = match(screen.copy(), waiting)
    

    pyautogui.typewrite(sentence)
    pyautogui.press("enter")
    sleep(0.3)
    pyautogui.press("tab")
    sleep(0.3)
    screen = cv.imread("screen.png")
    set_date(screen, day, month)
    sleep(0.2)
    set_time(hour, minute)
