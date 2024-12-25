
import pyautogui
import numpy as np
import time
import mss

from human_benchmark.Controller import Controller


class ReactionTimeSolver:

    nb_clicks: int
    screenshot_width: int
    screenshot_height: int
    auto_continue: bool
    click_pause: float

    def __init__(self,
                 nb_clicks: int,
                 screenshot_width: int,
                 screenshot_height: int,
                 auto_continue: bool,
                 click_pause: float):
        self.nb_clicks = nb_clicks
        self.screenshot_width = screenshot_width
        self.screenshot_height = screenshot_height
        self.auto_continue = auto_continue
        self.click_pause = click_pause

    def solve(self, controller: Controller, start_screen_region):

        # Define the region for the screenshot
        screenshot_region = {
            'left': int(pyautogui.center(start_screen_region).x) - self.screenshot_width // 2,
            'top': int(start_screen_region[1]),
            'width': self.screenshot_width,
            'height': self.screenshot_height
        }
        click_position = pyautogui.center(tuple(screenshot_region.values()))

        # Do a first click if auto clicking is on
        if self.auto_continue:
            pyautogui.click(*click_position)

        # Initialize an object to take screenshots
        with mss.mss() as sct:

            # Do the benchmark
            nb_clicks = 0
            while not controller.should_stop():

                # Fail safe
                pyautogui.failSafeCheck()

                # Take screenshot and convert to numpy array
                image = np.array(sct.grab(screenshot_region))

                # Get the mean rgb values from the image
                (red, green, blue) = [np.mean(image[:, :, i]) for i in range(3)]

                # Click if the screen is green
                if green > red and green > blue:
                    pyautogui.click(*click_position)
                    nb_clicks += 1
                    time.sleep(self.click_pause)

                    # Check if all clicks have been done
                    if nb_clicks >= self.nb_clicks:
                        return

                    # Check if automatic continue is on
                    if self.auto_continue:
                        pyautogui.click(*click_position)
