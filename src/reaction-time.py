
import toml
import pyautogui
import pymsgbox
import keyboard
import cv2
import numpy as np
import time


def main(root: str):

    # Config
    config = toml.load(f'{root}/config.toml')

    # Set th delay
    pause_cached = pyautogui.PAUSE
    pyautogui.PAUSE = config['general']['delay']

    # Start
    keyboard.wait(config['general']['start-key'])

    # Check if the start screen is found
    try:
        start_screen_region = pyautogui.locateOnScreen(f'{root}/assets/reaction-time/start-screen.png', confidence=0.9)
    except pyautogui.ImageNotFoundException:
        pymsgbox.alert(text='Start screen not found!', title='ERROR')
        return

    # Define the region for the screenshot
    screenshot_region = (
        int(pyautogui.center(start_screen_region).x) - config['reaction-time']['screenshot-width'] // 2,
        int(start_screen_region.top),
        config['reaction-time']['screenshot-width'],
        config['reaction-time']['screenshot-height']
    )
    click_position = pyautogui.center(screenshot_region)

    # Do a first click if auto clicking is on
    if config['reaction-time']['auto-continue']:
        pyautogui.click(*click_position)

    # Do the benchmark
    nb_clicks = 0
    while not keyboard.is_pressed(config['general']['end-key']):

        # Fail safe
        pyautogui.failSafeCheck()

        # Take screenshot and convert to numpy array
        image = pyautogui.screenshot(region=screenshot_region)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Get the mean rgb values from the image
        (blue, green, red) = [np.mean(image[:, :, i]) for i in range(3)]

        # Click if the screen is green
        if green > red and green > blue:
            pyautogui.click(*click_position)
            nb_clicks += 1
            time.sleep(config['reaction-time']['click-pause'])

            # Check if all clicks have been done
            if nb_clicks >= config['reaction-time']['nb-clicks']:
                return

            # Check if automatic continue is on
            if config['reaction-time']['auto-continue']:
                pyautogui.click(*click_position)

    # Reset the pause to avoid side effects
    pyautogui.PAUSE = pause_cached


if __name__ == '__main__':
    main(root='..')
