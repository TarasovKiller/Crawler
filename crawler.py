import string
from typing import Iterable
from urllib.parse import urlparse
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from queue import Empty
from multiprocessing.managers import SyncManager
import multiprocessing
import threading
from sitemap_writer import SitemapWriter
from html_parser import MyHTMLParser
from utils.url_operations import get_domain_name


class Crawler():
    def __init__(self, base_url: str, max_processes=5, max_threads=10, filepath='sitemap.xml'):
        self.filepath = filepath

        self.base_url = base_url
        self.domain = get_domain_name(base_url)

        m = multiprocessing.Manager()
        self.urls_on_visit = m.dict()
        self.m_lock = m.Lock()
        self.urls_dict = m.dict()
        self.counter_getter = m.Value('i', 0)
        self.counter_setter = m.Value('i', 1)
        self.delete_index = 0

        self.sitemap_writer = self.create_sitemap_writer()

        self.max_processes = max_processes
        self.max_threads = max_threads
        self.urls_dict[0] = base_url

    def sitemap_thread(self, event: threading.Event, timeout: int = 120) -> None:
        print("sitemap_thread started")
        start = time.time()
        while not event.is_set():
            time.sleep(timeout)
            self.sitemap_writer.save(self.filepath)
            with open('log.txt', 'a+') as f:
                f.write(str(time.time() - start)+" " + str(self.counter_getter.value) +
                        " " + str(self.counter_setter.value)+"\n")
            event.wait(1)

    def process_links(self, links: Iterable[str]) -> None:
        for url in links:
            if not url.startswith('http'):
                continue

            changed_url = url.partition('://')[2]
            changed_url = changed_url.split(
                "#")[0] if "#" in changed_url else changed_url

            domain = get_domain_name(url)
            if (domain != self.domain):
                continue

            if changed_url in self.urls_on_visit:
                continue
            self.urls_on_visit[changed_url] = True
            # self.sitemap_writer.add_url(url) ---------Right here!
            with self.m_lock:
                self.urls_dict[self.counter_setter.value] = url
                self.counter_setter.value += 1

    def parse_links(self, url) -> Iterable[str] | None:

        self.sitemap_writer.add_url(url)

        next_links = []
        try:
            parser = MyHTMLParser(url)
            next_links = parser.get_links
            del parser
            self.process_links(next_links)
        except:
            return []

        return next_links

    def thread_worker(self) -> None:

        while True:

            try:
                with self.m_lock:
                    url = self.urls_dict.get(self.counter_getter.value)
                    if url is None:
                        raise KeyError
                    self.counter_getter.value += 1

            except KeyError:
                print("Key Error self.counter =", self.counter_getter.value)
                break

            links = self.parse_links(url)

    def process_worker(self) -> None:
        print(f"Run process with {self.max_threads} threads...")
        delay = self.max_threads/2
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []

            for _ in range(self.max_threads):
                futures.append(executor.submit(self.thread_worker))

                time.sleep(delay)
                delay -= 0.5

            for future in as_completed(futures):
                print(future.result())

    def run(self) -> None:
        print(f"Run with {self.max_processes} processes...")

        event = threading.Event()
        thread = threading.Thread(target=self.sitemap_thread, args=(event,))
        thread.start()

        delay = self.max_processes//2

        with ProcessPoolExecutor(max_workers=self.max_processes) as executor:
            futures = []
            for _ in range(self.max_processes):
                futures.append(executor.submit(self.process_worker))

                time.sleep(delay)
                delay -= 0.3

            for future in as_completed(futures):
                try:
                    result = future.result()
                    print(result)
                except Exception as e:
                    print(f"An error occurred: {e}")
            event.set()
            # self.sitemap_writer.save(self.filepath)

    def create_sitemap_writer(self) -> SitemapWriter:
        manager = SyncManager()
        manager.register('SitemapWriter', SitemapWriter)
        manager.start()

        sitemap_writer = manager.SitemapWriter()
        return sitemap_writer
