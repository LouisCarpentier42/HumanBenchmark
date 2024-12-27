
import pyautogui
import pyscreeze
from pytesseract import pytesseract
import time
import pathlib

from human_benchmark.Solver import Solver
from human_benchmark.Controller import Controller


class VerbalMemorySolver(Solver):
    delay_start: float
    delay_click: float
    screenshot_x: float
    screenshot_y: float
    screenshot_width: int
    screenshot_height: int
    confidence: float
    max_score: int
    path_to_tesseract: str
    PATH_START_BUTTON: str = str(pathlib.Path(__file__).parent / 'assets' / 'verbal_memory' / 'button_start.png')
    PATH_NEW_BUTTON: str = str(pathlib.Path(__file__).parent / 'assets' / 'verbal_memory' / 'button_new.png')
    PATH_SEEN_BUTTON: str = str(pathlib.Path(__file__).parent / 'assets' / 'verbal_memory' / 'button_seen.png')

    def __init__(self,
                 delay_start: float,
                 delay_click: float,
                 screenshot_x: float,
                 screenshot_y: float,
                 screenshot_width: int,
                 screenshot_height: int,
                 confidence: float,
                 max_score: int,
                 path_to_tesseract: str):
        self.delay_start = delay_start
        self.delay_click = delay_click
        self.screenshot_x = screenshot_x
        self.screenshot_y = screenshot_y
        self.screenshot_width = screenshot_width
        self.screenshot_height = screenshot_height
        self.confidence = confidence
        self.max_score = max_score
        self.path_to_tesseract = path_to_tesseract

    def solve(self, controller: Controller, benchmark_region: pyscreeze.Box) -> None:

        # Set the start time
        start_time = time.time()

        # Define where the text is
        screenshot_center_x = benchmark_region.left + benchmark_region.width * self.screenshot_x
        screenshot_center_y = benchmark_region.top + benchmark_region.height * self.screenshot_y
        screenshot_region = (
            int(screenshot_center_x - self.screenshot_width // 2),
            int(screenshot_center_y - self.screenshot_height // 2),
            self.screenshot_width,
            self.screenshot_height
        )

        # Find the location of the start button
        start_button = pyautogui.locateCenterOnScreen(self.PATH_START_BUTTON, confidence=self.confidence, minSearchTime=1)

        # Remaining time before starting
        time.sleep(max([0, self.delay_start - (time.time() - start_time)]))

        # Press the start button
        pyautogui.click(*start_button)

        # Locate the new and seen buttons
        # For some reason, the new button must be searched twice
        _ = pyautogui.locateCenterOnScreen(self.PATH_NEW_BUTTON, confidence=self.confidence, minSearchTime=1)
        new_button = pyautogui.locateCenterOnScreen(self.PATH_NEW_BUTTON, confidence=self.confidence, minSearchTime=1)
        seen_button = pyautogui.locateCenterOnScreen(self.PATH_SEEN_BUTTON, confidence=self.confidence, minSearchTime=1)

        # Set the location of the tesseract.exe
        pytesseract.tesseract_cmd = self.path_to_tesseract

        # Variables to keep track of
        seen_words = set()
        score = 0

        # Loop until a stop command is called
        while not controller.should_stop() and score < max(self.max_score, 1):

            # Opening the image & storing it in an image object
            image = pyautogui.screenshot(region=screenshot_region)

            # Extract the text from the image
            word = pytesseract.image_to_string(image)

            # If there are no lives left, then the score is shown, which has a space
            if ' ' in word:
                print('Reached', word)
                break

            # Check if the word is seen, and do the correct action
            if word in seen_words:
                pyautogui.click(*seen_button)
            else:
                pyautogui.click(*new_button)
                seen_words.add(word)

            # Increment the score
            if self.max_score != -1:
                score += 1

            # Wait a moment
            time.sleep(self.delay_click)
