import requests

from .api import GitHubAPI


class DefaultGitHubAPI(GitHubAPI):

    def get(self, url: str, params=None):
        if params is None:
            params = {}

        response = requests.get(url, params=params, headers=self.headers)
        assert response.status_code == 200, f"{response.json()['message']}"

        return response.json()
