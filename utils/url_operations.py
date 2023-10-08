from urllib.parse import urlparse

def get_domain_name(url:str) -> str:
    parsed_url = urlparse(url)

    domain = parsed_url.netloc

    domain_parts = domain.split(".")

    domain_name = domain_parts[-2] if len(domain_parts) > 1 else domain_parts[-1]
    return domain_name

def get_url(self,url):
    parsed_url = urlparse(url)
    return "".join([parsed_url.netloc,parsed_url.path])