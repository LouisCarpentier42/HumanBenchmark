
import abc
from human_benchmark.Controller import Controller


class Solver(abc.ABC):

    @abc.abstractmethod
    def solve(self, controller: Controller, benchmark_region: tuple) -> None:
        raise NotImplementedError()
