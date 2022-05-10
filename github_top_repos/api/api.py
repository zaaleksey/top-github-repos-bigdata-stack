from abc import ABC, abstractmethod
from configparser import ConfigParser


class GitHubAPI(ABC):

    def __init__(self, config: ConfigParser):
        self.headers = {"Authorization": f"token {config['GitHub']['access_token']}"}

    @abstractmethod
    def get(self, *args, **kwargs):
        pass
