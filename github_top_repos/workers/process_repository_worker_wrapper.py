from concurrent.futures import ProcessPoolExecutor

from .parallel_repository_worker_wrapper import ParallelRepositoryWorkerWrapper


class ProcessRepositoryWorkerWrapper(ParallelRepositoryWorkerWrapper):

    def get_pool_executor(self, max_workers):
        return ProcessPoolExecutor(max_workers=max_workers)
