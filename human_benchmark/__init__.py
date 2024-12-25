
import toml
import pyautogui
import keyboard

from human_benchmark.reaction_time import ReactionTimeSolver
from human_benchmark.Controller import Controller

__all__ = [
    'run'
]

solvers = {
    'reaction_time': ReactionTimeSolver
}


def run(path_to_config: str):

    # Config
    config = toml.load(f'{path_to_config}/config.toml')
    print(f"Press '{config['general']['start_key']}' when the application is open.")
    print(f"Press '{config['general']['stop_key']}' to quit.")

    # Set th delay
    pause_cached = pyautogui.PAUSE
    pyautogui.PAUSE = config['general']['delay']

    # Start the application when requested
    keyboard.wait(config['general']['start_key'])

    # TODO automatically infer the game based on that is open?
    #  Probably based on the 'start-screen' image in the assets
    benchmark = 'reaction_time'
    print(f"Solving benchmark '{benchmark}'")

    # Check if the start screen is found
    # TODO the assets maybe fixed location?
    try:
        start_screen_region = pyautogui.locateOnScreen(f'{path_to_config}/assets/{benchmark}/start_screen.png', confidence=0.9)
    except pyautogui.ImageNotFoundException:
        print('Start screen not found!')
        return

    # Initialize the controller and the solver
    controller = Controller(config['general']['stop_key'])
    solver = solvers[benchmark](**config[benchmark])

    # Solve the task
    solver.solve(controller=controller, start_screen_region=start_screen_region)

    # Reset the pause to avoid side effects
    pyautogui.PAUSE = pause_cached
