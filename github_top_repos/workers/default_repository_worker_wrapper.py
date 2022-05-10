from .worker_wrapper import WorkerWrapper


class DefaultRepositoryWorkerWrapper(WorkerWrapper):

    def exec(self, repository_urls: list[str]) -> list[dict]:
        repository_data = []
        for url in repository_urls:
            repository_data.extend(self.worker.exec(url))

        return repository_data
