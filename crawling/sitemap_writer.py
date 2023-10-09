import xml.etree.ElementTree as ET
import os
import sys


class SitemapWriter():
    def __init__(self):
        venv_path = sys.prefix
        project_path = os.path.dirname(venv_path)
        self.path = os.path.join(project_path, "sitemaps")
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.urlset = ET.Element("urlset")
        self.urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    def add_url(self, url: str) -> None:
        url_element = ET.SubElement(self.urlset, "url")
        loc = ET.SubElement(url_element, "loc")
        loc.text = url

    def save(self, file_name: str = 'sitemap.xml') -> None:
        filepath = os.path.join(self.path, file_name)
        tree = ET.ElementTree(self.urlset)
        tree.write(filepath, encoding="UTF-8", xml_declaration=True)
