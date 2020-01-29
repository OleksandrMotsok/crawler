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
        async with aiohttp.ClientSession() as session:
            # skip jpeg and video files which downloading a while
            if not link.endswith("/"):
                return;
            print("Try to process: ", link)
            self.not_processed += getAllLinks(await fetch(session, link), self.root)
            print(self.not_processed)

    async def crawl(self):
        self.not_processed.append(self.root)
        while self.not_processed:
            link = self.not_processed.pop()

            # stay at main site
            if not link.startswith(self.root):
                continue

            print("------------------------------------------------------------------------------------------")
            if link not in self.processed:
                ret = await self.process(link)
                self.processed.append(link)


async def main():
    links = LinksCollection()
    #links.root = 'http://mysmallwebpage.com/'
    links.root = 'https://www.python.org/'

    print(links.not_processed)
    await links.crawl()
    print("Finished")
    print(links.processed)


def getAllLinks(html, parrentLink):
    soup = BeautifulSoup(html)
    links = []
    for node in soup.findAll("a"):
        link = node.get("href")
        if link is None:
            continue

        # link = link[:link.find("#")]

        if parrentLink.endswith(link):
            continue
        else:
            print("New link", link)
        if not link.startswith("http"):
            link = parrentLink + link

        links.append(link)

    print(links)
    return links


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
