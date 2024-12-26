
import toml
import pathlib
import pyautogui
import keyboard

from human_benchmark.ReactionTimeSolver import ReactionTimeSolver
from human_benchmark.Controller import Controller

__all__ = [
    'run'
]

solvers = {
    'reaction_time': ReactionTimeSolver
}


def run(custom_config_path: str = None):
    # Config
    config_path = pathlib.Path(__file__).parent / 'config.toml' if custom_config_path is None else custom_config_path
    config = toml.load(config_path)
    print(f"Press '{config['general']['start_key']}' when the application is open.")
    print(f"Press '{config['general']['stop_key']}' to quit.")

    # Set th delay
    pause_cached = pyautogui.PAUSE
    pyautogui.PAUSE = config['general']['delay']

    # Start the application when requested
    keyboard.wait(config['general']['start_key'])

    # TODO automatically infer the game based on which is open?
    #  Probably based on the 'start_screen' image in the assets
    benchmark = 'reaction_time'
    print(f"Solving benchmark '{benchmark}'")

    # Check if the start screen is found
    try:
        game_region = pyautogui.locateOnScreen(f'{pathlib.Path(__file__).parent}/assets/{benchmark}/start_screen.png', confidence=0.9)
    except pyautogui.ImageNotFoundException:
        print('Start screen not found!')
        return

    # Initialize the controller and the solver
    controller = Controller(config['general']['stop_key'])
    # TODO initialize/start controller
    solver = solvers[benchmark](**config[benchmark])

    # Solve the task
    solver.solve(controller=controller, game_region=game_region)

    # Reset the pause to avoid side effects
    pyautogui.PAUSE = pause_cached
