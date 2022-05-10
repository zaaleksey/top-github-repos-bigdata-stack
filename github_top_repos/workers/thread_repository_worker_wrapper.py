from concurrent.futures import ThreadPoolExecutor

from .parallel_repository_worker_wrapper import ParallelRepositoryWorkerWrapper


class ThreadRepositoryWorkerWrapper(ParallelRepositoryWorkerWrapper):

    def get_pool_executor(self, max_workers):
        return ThreadPoolExecutor(max_workers=max_workers)
