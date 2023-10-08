from typing import Iterable
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
from urllib.parse import urlparse, quote, urljoin


class MyHTMLParser(HTMLParser):
    def __init__(self, url: str):
        # Нужно добавить проверку на коректность ссылки
        super().__init__()
        self.links = []
        self.url = url
        self.domain = self.create_domain(url)

        resp = None
        req = Request(quote(url, safe=":/?=#"), headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        })
        try:
            resp = urlopen(req, timeout=10)
        except HTTPError as e:
            if e.code == 404:
                print("Страница не найдена - ", url)
                return None
        except TimeoutError as e:
            print(f"Долгое ожидание - {url}\n{e.msg}")
            return None
        except URLError as e:
            print(e.reason)
            return None
            # пропустить парсинг страницы
        # resp = urlopen(quote(url,safe=":/"),timeout=5)
        if resp is None:
            return None

        content_type = resp.info().get_content_type()

        if 'text/html' in content_type:
            encoding = resp.info().get_param('charset', 'utf8')
            # print(encoding)
            try:
                html = resp.read().decode(encoding)
            except LookupError as e:
                html = resp.read().decode('utf-8')
            # print(html)

            self.feed(html)

        # print(self.links)
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            if "href" in attrs_dict:
                link = attrs_dict["href"]
                if link.startswith("http"):
                    self.links.append(link)
                elif link.startswith("/"):
                    self.links.append(urljoin(self.domain, link))
                else:
                    self.links.append(urljoin(self.url, link))

    @property
    def get_links(self) -> Iterable[str]:
        return (link for link in self.links)

    def create_domain(self, url: str) -> str:
        parsed_url = urlparse(url)
        return "".join([parsed_url.scheme, "://", parsed_url.netloc])
