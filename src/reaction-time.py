
import toml
import pyautogui
import pymsgbox
import keyboard
import numpy as np
import time
import mss


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
    screenshot_region = {
        'left': int(pyautogui.center(start_screen_region).x) - config['reaction-time']['screenshot-width'] // 2,
        'top': int(start_screen_region.top),
        'width': config['reaction-time']['screenshot-width'],
        'height': config['reaction-time']['screenshot-height']
    }
    click_position = pyautogui.center(tuple(screenshot_region.values()))

    # Do a first click if auto clicking is on
    if config['reaction-time']['auto-continue']:
        pyautogui.click(*click_position)

    # Initialize an object to take screenshots
    with mss.mss() as sct:

        # Do the benchmark
        nb_clicks = 0
        while not keyboard.is_pressed(config['general']['end-key']):

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
