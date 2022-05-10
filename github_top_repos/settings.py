from api import AsyncGitHubAPI
from api import DefaultGitHubAPI
from workers import AsyncRepositoryWorker
from workers import DatabaseWorker
from workers import DefaultRepositoryWorkerWrapper
from workers import OrganizationWorker
from workers import ProcessRepositoryWorkerWrapper
from workers import RepositoryWorker
from workers import ThreadRepositoryWorkerWrapper
from workers import TopFilterWorker
from workers import Worker


def get_workers(config) -> list[Worker]:
    mode = config["Build"]["mode"]
    number_of_organization = int(config["GitHub"]["number_of_organization"])
    top_number = int(config["GitHub"]["top_number"])

    api = DefaultGitHubAPI(config)
    async_api = AsyncGitHubAPI(config)

    repos_worker = RepositoryWorker(api)
    org_worker = OrganizationWorker(number_of_organization, api)
    filter_worker = TopFilterWorker(top_number)
    db_worker = DatabaseWorker()

    define_repository_worker: dict[str, Worker] = {
        "default": DefaultRepositoryWorkerWrapper(repos_worker),
        "thread": ThreadRepositoryWorkerWrapper(repos_worker),
        "process": ProcessRepositoryWorkerWrapper(repos_worker),
        "async": AsyncRepositoryWorker(async_api)
    }

    workers = [org_worker, define_repository_worker[mode], filter_worker, db_worker]

    return workers
