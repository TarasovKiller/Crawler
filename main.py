import time
from crawling.crawler import Crawler


def main():
    url = "https://crawler-test.com/"
    num_processes = 3
    num_threads = 8
    crawler = Crawler(url, num_processes, num_threads, "crawler-test.xml")
    crawler.run()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end-start)
