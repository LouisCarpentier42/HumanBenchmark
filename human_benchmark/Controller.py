
import threading
import keyboard


class Controller:
    start_key: str
    stop_key: str
    stop_event: threading.Event

    def __init__(self, start_key: str, stop_key: str):
        self.start_key = start_key
        self.stop_key = stop_key
        self.stop_event = threading.Event()

    def start(self) -> None:
        self.stop_event.clear()
        while not self.should_stop():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == self.stop_key:
                self.stop()
                return
            if event.event_type == keyboard.KEY_UP and event.name == self.start_key:
                return

    def stop(self) -> None:
        self.stop_event.set()

    def should_stop(self) -> bool:
        if keyboard.is_pressed(self.stop_key):
            self.stop()
        return self.stop_event.is_set()
