
import toml
import pathlib
import pyautogui

from human_benchmark.Controller import Controller
from human_benchmark.ReactionTimeSolver import ReactionTimeSolver
from human_benchmark.TargetAimerSolver import TargetAimerSolver

__all__ = [
    'run'
]

solvers = {
    'reaction_time': ReactionTimeSolver,
    'target_aimer': TargetAimerSolver
}


def run(custom_config_path: str = None):

    # Config
    config_path = pathlib.Path(__file__).parent / 'assets' / 'config.toml' if custom_config_path is None else custom_config_path
    config = toml.load(config_path)
    print(f"Press '{config['general']['start_key']}' when the application is open.")
    print(f"Press '{config['general']['stop_key']}' to quit.")

    # Set th delay
    pause_cached = pyautogui.PAUSE
    pyautogui.PAUSE = config['general']['delay']

    # Initialize and start the controller
    controller = Controller(config['general']['start_key'], config['general']['stop_key'])
    controller.start()

    # Check if there has already been a stop event
    if controller.should_stop():
        return

    # Automatically infer the benchmark
    selected_benchmark = None
    game_region = None
    for benchmark in solvers:
        try:
            selected_benchmark = benchmark
            game_region = pyautogui.locateOnScreen(f'{pathlib.Path(__file__).parent}/assets/{benchmark}/start_screen.png', confidence=0.9)
            break
        except pyautogui.ImageNotFoundException:
            pass
    if selected_benchmark is None:
        print('Benchmark not recognized!')
        return
    print(f"Solving benchmark '{selected_benchmark}'")

    # Solve the task
    solver = solvers[selected_benchmark](**config[selected_benchmark])
    solver.solve(controller=controller, benchmark_region=game_region)

    # Reset the pause to avoid side effects
    pyautogui.PAUSE = pause_cached
