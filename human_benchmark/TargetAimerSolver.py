
import pyautogui
import pyscreeze
import time
import mss
import numpy as np

from human_benchmark.Solver import Solver
from human_benchmark.Controller import Controller


class TargetAimerSolver(Solver):
    nb_targets: int
    target_size: int
    quantile: float
    click_pause: float
    TARGET_COLOR: np.array = np.array([232, 195, 149])

    def __init__(self, nb_targets: int, target_size: int, quantile: float, click_pause: float):
        self.nb_targets = nb_targets
        self.target_size = target_size
        self.quantile = quantile
        self.click_pause = click_pause

    def solve(self, controller: Controller, benchmark_region: pyscreeze.Box) -> None:

        screenshot_region = {'left': benchmark_region[0], 'top': benchmark_region[1], 'width': benchmark_region[2], 'height': benchmark_region[3]}
        pyautogui.click(*pyautogui.center(benchmark_region))
        time.sleep(self.click_pause)

        with mss.mss() as sct:

            nb_clicks = 0
            while not controller.should_stop() and nb_clicks < self.nb_targets:

                # Find the target
                target_pixels = np.array([])
                while target_pixels.shape[0] < self.target_size:
                    image = np.array(sct.grab(screenshot_region))[:, :, :-1]
                    target_pixels = np.argwhere(np.all(image == self.TARGET_COLOR, axis=2))

                # Identify the pixel to click
                pixel_to_click = target_pixels[int(target_pixels.shape[0] * self.quantile)]
                pyautogui.click(pixel_to_click[1] + benchmark_region[0], pixel_to_click[0] + benchmark_region[1])

                # Setup next loop
                nb_clicks += 1
                time.sleep(self.click_pause)
