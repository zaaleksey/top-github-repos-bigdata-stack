from configparser import ConfigParser

from .api import GitHubAPI


class AsyncGitHubAPI(GitHubAPI):

    def __init__(self, config: ConfigParser):
        super().__init__(config)

    async def get(self, url: str, session, params=None):
        if params is None:
            params = {}

        async with session.get(url, headers=self.headers, params=params) as response:
            data = await response.json()

        return data
