from asyncio import shield
from typing import List, Any

import aiohttp
import asyncio

from bs4 import BeautifulSoup


async def fetch(session, url):
    async with session.get(url) as response:
        try:
            return await response.text()
        except Exception as ex:
            return ""


class LinksCollection:
    not_processed: List[Any]
    processed: List[Any]

    def __init__(self):
        self.root = ""
        self.processed = []
        self.not_processed = []

    async def process(self, link):
        self.processed.append(link)

        async with aiohttp.ClientSession() as session:
            # skip jpeg and video files which downloading a while
            if not link.endswith("/"):
                return;
            print("Try to process: ", link)
            self.not_processed += get_all_links(await fetch(session, link), self.root)

    async def sem_process(self, sem, link):
        async with sem:
            await self.process(link)

    async def crawl(self):
        self.not_processed.append(self.root)

        limit = 3
        sem = asyncio.Semaphore(limit)
        tasks = []
        responses = []
        done = []
        #while self.not_processed or tasks:
        while True:
            if not self.not_processed:
                try:
                    done = await asyncio.wait_for(shield(responses), timeout=1.0)
                except asyncio.TimeoutError:
                    pass

                if not self.not_processed and len(tasks) == len(done):
                    break

                continue

            link = self.not_processed.pop()

            # stay at main site
            if not link.startswith(self.root):
                continue

            if link not in self.processed:
                task = asyncio.ensure_future(self.sem_process(sem, link))
                tasks.append(task)
                responses = asyncio.gather(*tasks)

        print("Done")
        print(self.processed)

async def main():
    links = LinksCollection()
    links.root = 'http://mysmallwebpage.com/'
    #links.root = 'https://www.python.org/'

    print(links.not_processed)
    await links.crawl()
    print("Finished")
    print(links.processed)


def get_all_links(html, parrent_link):
    soup = BeautifulSoup(html)
    links = []
    for node in soup.findAll("a"):
        link = node.get("href")
        if link is None:
            continue

        if parrent_link.endswith(link):
            continue
        else:
            print("New link", link)
        if not link.startswith("http"):
            link = parrent_link + link

        links.append(link)

    return links


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
