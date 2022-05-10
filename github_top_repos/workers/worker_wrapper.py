from .worker import Worker


class WorkerWrapper(Worker):

    def __init__(self, worker: Worker):
        self.worker = worker
