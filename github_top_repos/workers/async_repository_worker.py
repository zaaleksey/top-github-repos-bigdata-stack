import asyncio
from functools import reduce

import aiohttp

from .request_worker import RequestWorker
from .utils import mapping_repo


class AsyncRepositoryWorker(RequestWorker):

    def exec(self, *args, **kwargs) -> dict[int, str]:
        return asyncio.run(self.get_data(*args, **kwargs))

    async def get_data(self, repository_urls: list[str]) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.get_repository(url, session)) for url in repository_urls]
            data = await asyncio.gather(*tasks)

        return reduce(lambda a, b: a + b, data)

    async def get_repository(self, url: str, session) -> list[dict]:
        params = {"page": 1}
        repository_data: list[dict] = list()
        response = await self.api.get(url, session)
        while response:
            params["page"] += 1
            repository_data.extend(map(mapping_repo, response))
            response = await self.api.get(url, session, params=params)

        return repository_data
