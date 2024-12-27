
import abc
import pyscreeze
from human_benchmark.Controller import Controller


class Solver(abc.ABC):

    @abc.abstractmethod
    def solve(self, controller: Controller, benchmark_region: pyscreeze.Box) -> None:
        raise NotImplementedError()
