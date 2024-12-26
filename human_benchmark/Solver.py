
import abc
from human_benchmark.Controller import Controller


class Solver(abc.ABC):

    @abc.abstractmethod
    def solve(self, controller: Controller, benchmark_region: tuple) -> None:
        """
        Solve the benchmark.

        Parameters
        ----------
        controller: Controller
            The Controller object used to control the game and handle
            stop events.
        benchmark_region: tuple TODO is this actually a tuple? (if no change doc)
            The region on the screen where the benchmark is being
            projected on the screen. This is a tuple with values
            `(<left>, <top>, <width>, <height>)
        """