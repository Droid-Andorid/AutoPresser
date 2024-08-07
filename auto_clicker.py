from pyautogui import click, press
from pyautogui import PyAutoGUIException
from pynput.keyboard import Listener, KeyCode, HotKey
from PySide6.QtCore import QThread
from time import sleep


class AutoClicker(QThread):
    def __init__(self, button: str, delay: float, interval: float):
        super().__init__()
        self.delay = float(delay)
        self.interval = float(interval)
        self.btn_click = button.lower()
        self.running = False
        self.work_program = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def stop(self):
        self.stop_clicking()
        self.work_program = False

    def run(self):
        while self.work_program:
            while self.running:
                try:
                    click(button=self.btn_click, interval=self.interval)
                except PyAutoGUIException:
                    press(self.btn_click)
            sleep(self.delay)


async def start_one_key(start_key, button, *args):
    global app, listener

    delay = 0.0 if args[0] == "" or float(args[0]) < 0.0 else float(args[0])

    app = AutoClicker(button, delay, 0)
    app.start()

    def on_press(key):
        if key == KeyCode(char=start_key):
            if app.running:
                app.stop_clicking()
            else:
                app.start_clicking()

    with Listener(on_press=on_press) as listener:
        listener.join()


async def start_two_keys(start_key, start_two_key, button, *args):
    global app, listener

    delay = 0.0 if args[0][0] == "" or float(args[0][0]) < 0.0 else float(args[0][0])
    interval = 0.0 if args[0][1] == "" or float(args[0][1]) < 0.0 else float(args[0][1])

    app = AutoClicker(button, delay, interval)
    app.start()
    click = False

    def on_active():
        if click:
            app.start_clicking()
        else:
            app.stop_clicking()

    hotkey = HotKey((HotKey.parse(f"<{start_key}>+{start_two_key}")),
                    on_activate=on_active)

    def on_press(f):
        return lambda k: f(listener.canonical(k))

    with Listener(on_press=on_press(hotkey.press), on_release=on_press(hotkey.release)) as listener:
        listener.join()


async def stop():
    app.stop()
    listener.stop()