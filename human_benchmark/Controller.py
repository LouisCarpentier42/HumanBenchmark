
import keyboard


class Controller:
    key_to_stop: str

    def __init__(self, key_to_stop: str):
        # TODO execute in separate thread (+ then start the controller as well)
        self.key_to_stop = key_to_stop

    def should_stop(self):
        return keyboard.is_pressed(self.key_to_stop)
