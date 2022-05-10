from abc import ABC, abstractmethod
from functools import reduce
from multiprocessing import cpu_count

from .worker_wrapper import WorkerWrapper


class ParallelRepositoryWorkerWrapper(WorkerWrapper, ABC):

    def exec(self, repository_urls: list[str]) -> list[dict]:
        with self.get_pool_executor(max_workers=cpu_count() * 2) as executor:
            result = executor.map(self.worker.exec, repository_urls)

        return reduce(lambda a, b: a + b, list(result))

    @abstractmethod
    def get_pool_executor(self, max_workers):
        pass
