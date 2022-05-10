from .worker import Worker


class TopFilterWorker(Worker):

    def __init__(self, top_count: int):
        self.top_count = top_count

    def exec(self, repos_data: list[dict]) -> list[dict]:
        return sorted(repos_data, key=lambda repo: repo["stars_count"], reverse=True)[:self.top_count]
