
import keyboard
import pyautogui


class Controller:
    key_to_stop: str

    def __init__(self, key_to_stop: str):
        # TODO execute in separate thread (+ then start the controller as well in main)
        self.key_to_stop = key_to_stop

    def should_stop(self):
        pyautogui.failSafeCheck()  # Fail safe
        return keyboard.is_pressed(self.key_to_stop)
