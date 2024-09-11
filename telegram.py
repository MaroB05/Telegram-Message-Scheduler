import cv2 as cv
import pyautogui
import pandas as pd
from time import sleep
from datetime import datetime
from matplotlib import pyplot as plt 

#43, 82, 120


def match(a, b, threshold=0.7):
    try:
        a_grey = cv.cvtColor(a.copy(), cv.COLOR_BGR2GRAY)
        b_grey = cv.cvtColor(b.copy(), cv.COLOR_BGR2GRAY)
    except:
        print(a)
    result = cv.matchTemplate(a_grey, b_grey, cv.TM_CCOEFF_NORMED)
    _ , max_val, _ , max_loc = cv.minMaxLoc(result)
    if max_val >= threshold:
        return (True, max_loc)
    
    return (False, None)

def position():
    pass


def set_date(screen, day, month):

    template = cv.imread(f"Figures\\{day}.png")
    mon = cv.imread(f"Months\\{month}.png")

    # screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    # template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    # mon_gray = cv.cvtColor(mon, cv.COLOR_BGR2GRAY)


    found, _ = match(screen, mon)
    while not found:
        pyautogui.press("down")
        pyautogui.screenshot('screen.png')
        screen = cv.imread("screen.png")
        screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
        found, _ = match(screen, mon)

    found, max_loc = match(screen, template)


    # Define a threshold for matching
    threshold = 0.7

    if found:
        # Draw rectangle around the matched region
        top_left = max_loc
        h, w = template.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)

        center = (top_left[0] + w//2, top_left[1] + h//2)
        
        # Move the mouse to the top-left position
        pyautogui.moveTo(center[0], center[1])

        # Perform a click
        pyautogui.click()

        # Display the result
        # plt.figure(figsize=(10, 5))
        # plt.subplot(121), plt.imshow(cv.cvtColor(screen, cv.COLOR_BGR2RGB))
        # plt.title('Detected Point'), plt.axis('off')
        # plt.subplot(122), plt.imshow(cv.cvtColor(template, cv.COLOR_BGR2RGB))
        # plt.title('Template'), plt.axis('off')
        # plt.show()

def set_time(hour, minute):
    pyautogui.press("backspace")
    pyautogui.press("backspace")
    pyautogui.press("left")
    pyautogui.press("backspace")
    pyautogui.press("backspace")
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
        # print(screen)
        found, _ = match(screen.copy(), waiting)
    


    pyautogui.typewrite(sentence)
    pyautogui.press("enter")
    sleep(0.3)
    pyautogui.press("tab")
    sleep(0.3)
    screen = cv.imread("screen.png")
    set_date(screen.copy(), day, month)
    sleep(0.2)
    set_time(hour, minute)
