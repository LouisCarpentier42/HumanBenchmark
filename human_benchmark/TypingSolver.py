import keyboard
import pyautogui
import pyscreeze
from pytesseract import pytesseract
import time

from human_benchmark.Solver import Solver
from human_benchmark.Controller import Controller


class TypingSolver(Solver):
    delay_start: float
    delay_key_press: float
    text_height: int
    path_to_tesseract: str

    def __init__(self, delay_start: float, delay_key_press: float, text_height: int, path_to_tesseract: str):
        self.delay_start = delay_start
        self.delay_key_press = delay_key_press
        self.text_height = text_height
        self.path_to_tesseract = path_to_tesseract

    def solve(self, controller: Controller, benchmark_region: pyscreeze.Box) -> None:

        # Set the start time
        start_time = time.time()

        # Define where the text is
        screenshot_region = (
            # Same left as the start screen
            int(benchmark_region.left),
            # Start below where the screenshot was taken
            int(benchmark_region.top + benchmark_region.height),
            # Same width as the start screen
            int(benchmark_region.width),
            # Height is defined by the user
            self.text_height
        )

        # Opening the image & storing it in an image object
        image = pyautogui.screenshot(region=screenshot_region)

        # Set the location of the tesseract.exe
        pytesseract.tesseract_cmd = self.path_to_tesseract

        # Extract the text from the image
        text = pytesseract.image_to_string(image)

        # Click once to make sure you are in the correct position
        pyautogui.click(pyautogui.center(screenshot_region))

        # Format the text
        formatted_text = text.strip('\n|[]').replace('\n', ' ').replace('|', 'I').replace('  ', ' ')

        # Remaining time before starting
        time.sleep(max([0, self.delay_start - (time.time() - start_time)]))

        # Write the text
        keyboard.write(formatted_text, delay=self.delay_key_press)
