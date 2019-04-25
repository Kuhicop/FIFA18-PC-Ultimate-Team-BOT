import pyautogui
import os
import time
import win32gui
from tkinter import *
from threading import Thread
from pynput import keyboard

started = False
running = False
loop = True
x = 0
y = 0

class WindowMgr:
    # FOCUS GAME
    def __init__ (self):
        self._handle = None

    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        win32gui.SetForegroundWindow(self._handle)


def console(lbltext):
    # CREATE CONSOLE
    window = Tk()
    window.overrideredirect(1)
    window.wm_attributes("-topmost", 1)
    window.title("Welcome")
    lbl = Label(window, text=lbltext)
    lbl.config(font=("arial", 10))
    lbl.grid(column=0, row=0)
    window.mainloop()


# SPAWN CONSOLE
def spawn(text):
    print(text)
    threads = list()
    t = Thread(target=console, args=(text,))
    threads.append(t)
    t.start()


# CREATE KEYS
COMBINATION1 = [
    {keyboard.Key.ctrl, keyboard.Key.home},
    {keyboard.Key.shift, keyboard.Key.home}
    ]
COMBINATION2 = [
    {keyboard.Key.ctrl, keyboard.Key.end},
    {keyboard.Key.shift, keyboard.Key.end}
    ]

current = set()


def execute1():
    print("executed1")
    global running
    running = True


def execute2():
    print("executed2")
    os._exit(1)


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATION1]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATION1):
            execute1()
    if any([key in COMBO for COMBO in COMBINATION2]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATION2):
            execute2()


def on_release(key):
    pass


def listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


threads = list()
lt = Thread(target=listen)
threads.append(lt)
lt.start()


def findimage(image):
    image = image + ".png"
    try:
        global x
        global y
        x, y = pyautogui.locateCenterOnScreen(image, tolerance=0.5)
        print("Returning true for " + image)
        return True
    except TypeError:
        print("Returning false for " + image)
        return False

# ==========================================================================

# CHANGE DIR
spawn("Changing dir")
try:
    os.chdir("images")
except FileNotFoundError:
    spawn("Images folder not found, please download latest update.")

# FOCUS GAME
w = WindowMgr()
w.find_window_wildcard(".*FIFA.*")
w.set_foreground()
spawn("Ready, SHIFT + HOME(start) / SHIFT + END(quit)")

# ---------
# MAIN LOOP
# ---------
while loop:
    if running:
        # ULTIMATE TEAM
        # image1
        if not started:
            try:
                while findimage("start1"):
                    print(str(x) + " / " + str(y))
                    pyautogui.click(x, y, 1, 0.4)
                    started = True
            except TypeError:
                spawn("Image1 not found, testing with Image2.")
            except FileNotFoundError:
                spawn("start1.png not found, bot will close.")
                time.sleep(3)
                os._exit(1)

        # image2
        if not started:
            try:
                while findimage("start2"):
                    print(str(x) + " / " + str(y))
                    pyautogui.click(x, y, 1, 0.4)
                    started = True
            except TypeError:
                spawn("Image2 not found, bot will close.")
                time.sleep(3)
                os._exit(1)
            except FileNotFoundError:
                spawn("start2.png not found, bot will close.")
                time.sleep(3)
                os._exit(1)

        # SINGLE PLAYER
        if not started:
            spawn("Single player")
            while not findimage("singleplayer"):
                time.sleep(0.5)
            pyautogui.click(x, y, 1, 0.4)
            started = True

        # SEASON
        spawn("Season")
        while not findimage("season"):
            time.sleep(0.5)
        pyautogui.click(x, y, 1, 0.4)

        # PLAY MATCH
        spawn("Play match")
        while not findimage("playmatch"):
            time.sleep(0.5)
        pyautogui.click(x, y, 1, 0.4)

        # READYTOPLAY
        spawn("Checking status")
        i = 0
        while i <= 10:
            if not findimage("abletoplay"):
                time.sleep(1)
                i = i + 1

        # DETECTING RARE STATUS
        if i >= 10:
            spawn("Something happens")
            os._exit(1)

        # CONTINUE
        spawn("Continue")
        if not findimage("continue1"):
            findimage("continue2")
        pyautogui.click(x, y, 1, 0.4)

        # SIDE
        spawn("Selecting side")
        while not findimage("side"):
            time.sleep(0.5)

        # START
        spawn("Starting match")
        while not (findimage("matchstart1") or findimage("matchstart2")):
            pyautogui.press("enter")
            time.sleep(0.5)
        pyautogui.click(x, y, 1, 0.4)
        spawn("Sleeping 10 seconds")
        time.sleep(10)

        # SKIP MINIGAME
        spawn("Skipping minigame")
        pyautogui.press("esc")
        time.sleep(3)

        # SKIP ANIMATION
        spawn("Skipping animation")
        i = 0
        while i <= 5:
            pyautogui.click(x, y, 1, 0.2)
            time.sleep(1)
            i = i + 1

        # WAIT MATCH HALF
        i = 0
        while not findimage("half"):
            spawn("Waiting for " + str(i) + " seconds")
            pyautogui.click(x, y, 1, 0.2)
            time.sleep(0.8)
            i = i + 1
        pyautogui.press("enter")
        while not (findimage("resume1") or findimage("resume2")):
            time.sleep(0.5)
        pyautogui.click(x, y, 1, 0.4)

        # WAIT MATCH END
        i = 0
        while not findimage("end"):
            spawn("Waiting for " + str(i) + " seconds")
            pyautogui.click(x, y, 1, 0.2)
            time.sleep(0.8)
            i = i + 1

        spawn("Taking reward")
        while not (findimage("repeat1") or findimage("repeat2")):
            pyautogui.press("enter")
            time.sleep(1000)
        pyautogui.click(x, y, 1, 0.4)

        spawn("Skipping stats")
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.press("enter")

        spawn("Checking requirements")
        time.sleep(3)
        if findimage("requirements"):
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
            if findimage("accept1") or findimage("accept2"):
                pyautogui.click(x, y, 1, 0.4)

    time.sleep(3)
